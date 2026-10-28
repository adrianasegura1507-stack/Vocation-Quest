from math import ceil

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash
)
from werkzeug.security import generate_password_hash

from database import obtener_conexion
from routes.auth import (
    EDAD_MINIMA,
    EDAD_MAXIMA,
    calcular_edad,
    limites_fecha_nacimiento,
    validar_nombre,
    validar_correo,
    validar_contrasena,
    validar_fecha_nacimiento
)
from routes.pruebas import NIVELES_PRUEBA

admin = Blueprint("admin", __name__)

# Cuántos estudiantes se muestran por página en la lista
POR_PAGINA = 15


# =========================================
# FUNCIONES DE APOYO
# =========================================

def obtener_admin_actual():
    """
    Devuelve los datos del administrador que tiene la sesión iniciada,
    o None si no hay sesión o la persona no es administradora activa.
    """
    id_usuario = session.get("id_usuario")

    if id_usuario is None:
        return None

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id_usuario, nombre, correo, rol
            FROM usuarios
            WHERE id_usuario = %s
            AND rol = 'administrador'
            AND estado = 1
            """,
            (id_usuario,)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        conexion.close()


def acceso_denegado():
    """
    Se usa cuando alguien entra a una página de administración
    sin ser administrador.
    """
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    return redirect(url_for("inicio_estudiante"))


def destino_lista():
    """
    Vuelve a la lista de estudiantes, en la misma página
    y con la misma búsqueda donde estaba la persona.
    """
    volver = request.form.get("volver", "")

    if volver.startswith("/admin/estudiantes"):
        return redirect(volver)

    return redirect(url_for("admin.lista_estudiantes"))


def cargar_estudiante(cursor, id_usuario):
    """
    Busca a un estudiante por su id de usuario.
    Solo devuelve cuentas con rol de estudiante.
    """
    cursor.execute(
        """
        SELECT u.id_usuario, u.nombre, u.correo, u.estado,
               u.fecha_registro, e.fecha_nacimiento
        FROM usuarios u
        LEFT JOIN estudiantes e ON e.id_usuario = u.id_usuario
        WHERE u.id_usuario = %s
        AND u.rol = 'estudiante'
        """,
        (id_usuario,)
    )

    return cursor.fetchone()


def mostrar_formulario(modo, admin_actual, datos, error=None,
                       estudiante=None):
    """
    Muestra el formulario para crear o editar un estudiante.
    """
    fecha_min, fecha_max = limites_fecha_nacimiento()

    return render_template(
        "admin_estudiante_form.html",
        modo=modo,
        admin=admin_actual,
        seccion="estudiantes",
        datos=datos,
        error=error,
        estudiante=estudiante,
        fecha_min=fecha_min.isoformat(),
        fecha_max=fecha_max.isoformat(),
        edad_minima=EDAD_MINIMA,
        edad_maxima=EDAD_MAXIMA
    )


# =========================================
# PANEL DE INICIO
# =========================================

@admin.route("/admin")
def panel():

    admin_actual = obtener_admin_actual()

    if admin_actual is None:
        return acceso_denegado()

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:

        # Estudiantes registrados y cuántos tienen la cuenta activa
        cursor.execute(
            """
            SELECT COUNT(*) AS total,
                   COALESCE(SUM(CASE WHEN estado = 1 THEN 1 ELSE 0 END), 0)
                       AS activos
            FROM usuarios
            WHERE rol = 'estudiante'
            """
        )

        fila = cursor.fetchone()

        total = fila["total"]
        activos = int(fila["activos"])

        # Estudiantes que ya empezaron alguna prueba
        cursor.execute(
            """
            SELECT COUNT(DISTINCT id_estudiante) AS empezaron
            FROM intentos_prueba
            """
        )

        empezaron = cursor.fetchone()["empezaron"]

        # Estudiantes que ya vieron su resultado final
        cursor.execute(
            """
            SELECT COUNT(DISTINCT ip.id_estudiante) AS terminaron
            FROM resultados r
            INNER JOIN intentos_prueba ip
                ON ip.id_intento = r.id_intento
            """
        )

        terminaron = cursor.fetchone()["terminaron"]

        # Áreas principales de quienes ya terminaron
        cursor.execute(
            """
            SELECT a.nombre, COUNT(*) AS cantidad
            FROM resultados r
            INNER JOIN areas a
                ON a.id_area = r.id_area_principal
            GROUP BY a.id_area, a.nombre
            ORDER BY cantidad DESC, a.nombre
            """
        )

        filas_areas = cursor.fetchall()

    finally:
        cursor.close()
        conexion.close()

    total_resultados = sum(f["cantidad"] for f in filas_areas)

    areas = []

    for f in filas_areas:

        porcentaje = (
            round((f["cantidad"] / total_resultados) * 100)
            if total_resultados else 0
        )

        areas.append({
            "nombre": f["nombre"],
            "cantidad": f["cantidad"],
            "porcentaje": porcentaje
        })

    return render_template(
        "admin_panel.html",
        admin=admin_actual,
        seccion="panel",
        total=total,
        activos=activos,
        desactivados=total - activos,
        empezaron=empezaron,
        terminaron=terminaron,
        areas=areas
    )


# =========================================
# LISTA DE ESTUDIANTES (Read)
# =========================================

@admin.route("/admin/estudiantes")
def lista_estudiantes():

    admin_actual = obtener_admin_actual()

    if admin_actual is None:
        return acceso_denegado()

    busqueda = request.args.get("q", "").strip()

    pagina = request.args.get("pagina", 1, type=int) or 1

    if pagina < 1:
        pagina = 1

    patron = f"%{busqueda}%"

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM usuarios
            WHERE rol = 'estudiante'
            AND (nombre LIKE %s OR correo LIKE %s)
            """,
            (patron, patron)
        )

        total = cursor.fetchone()["total"]

        total_paginas = max(1, ceil(total / POR_PAGINA))

        if pagina > total_paginas:
            pagina = total_paginas

        desde = (pagina - 1) * POR_PAGINA

        cursor.execute(
            """
            SELECT u.id_usuario, u.nombre, u.correo, u.estado,
                   u.fecha_registro,
                   e.edad, e.fecha_nacimiento,
                   (
                       SELECT COUNT(DISTINCT ip.id_prueba)
                       FROM intentos_prueba ip
                       WHERE ip.id_estudiante = e.id_estudiante
                       AND ip.completado = 1
                   ) AS niveles,
                   (
                       SELECT COUNT(*)
                       FROM resultados r
                       INNER JOIN intentos_prueba ip2
                           ON ip2.id_intento = r.id_intento
                       WHERE ip2.id_estudiante = e.id_estudiante
                   ) AS con_resultado
            FROM usuarios u
            LEFT JOIN estudiantes e ON e.id_usuario = u.id_usuario
            WHERE u.rol = 'estudiante'
            AND (u.nombre LIKE %s OR u.correo LIKE %s)
            ORDER BY u.fecha_registro DESC, u.id_usuario DESC
            LIMIT %s OFFSET %s
            """,
            (patron, patron, POR_PAGINA, desde)
        )

        filas = cursor.fetchall()

    finally:
        cursor.close()
        conexion.close()

    estudiantes = []

    for fila in filas:

        # La edad se calcula con la fecha de nacimiento, si existe
        if fila["fecha_nacimiento"]:
            edad = calcular_edad(fila["fecha_nacimiento"])
        else:
            edad = fila["edad"]

        if fila["con_resultado"]:
            progreso = "✅ Terminó"
            progreso_clase = "fin"
        else:
            progreso = f"{fila['niveles'] or 0} de {NIVELES_PRUEBA} niveles"
            progreso_clase = "medio"

        estudiantes.append({
            "id_usuario": fila["id_usuario"],
            "nombre": fila["nombre"],
            "correo": fila["correo"],
            "activo": bool(fila["estado"]),
            "edad": edad,
            "fecha_registro": fila["fecha_registro"],
            "progreso": progreso,
            "progreso_clase": progreso_clase
        })

    # Dirección actual (con búsqueda y página), para volver aquí
    # después de activar, desactivar o eliminar
    if request.query_string:
        volver = request.full_path
    else:
        volver = request.path

    return render_template(
        "admin_estudiantes.html",
        admin=admin_actual,
        seccion="estudiantes",
        estudiantes=estudiantes,
        busqueda=busqueda,
        pagina=pagina,
        total_paginas=total_paginas,
        total=total,
        volver=volver
    )


# =========================================
# CREAR ESTUDIANTE (Create)
# =========================================

@admin.route("/admin/estudiantes/nuevo", methods=["GET", "POST"])
def nuevo_estudiante():

    admin_actual = obtener_admin_actual()

    if admin_actual is None:
        return acceso_denegado()

    if request.method == "GET":
        return mostrar_formulario("crear", admin_actual, {})

    nombre = request.form.get("nombre", "").strip()
    correo = request.form.get("correo", "").strip()
    contrasena = request.form.get("contrasena", "")
    fecha_texto = request.form.get("fecha_nacimiento", "").strip()

    datos = {
        "nombre": nombre,
        "correo": correo,
        "fecha_nacimiento": fecha_texto
    }

    # -----------------------------------------
    # Validaciones
    # -----------------------------------------

    error = (
        validar_nombre(nombre)
        or validar_correo(correo)
        or validar_contrasena(contrasena)
    )

    if error:
        return mostrar_formulario("crear", admin_actual, datos, error)

    fecha_nacimiento, edad, error = validar_fecha_nacimiento(fecha_texto)

    if error:
        return mostrar_formulario("crear", admin_actual, datos, error)

    # -----------------------------------------
    # Guardar
    # -----------------------------------------

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute(
            "SELECT id_usuario FROM usuarios WHERE correo = %s",
            (correo,)
        )

        if cursor.fetchone() is not None:
            return mostrar_formulario(
                "crear", admin_actual, datos,
                "Ese correo ya tiene una cuenta."
            )

        cursor.execute(
            """
            INSERT INTO usuarios
            (nombre, correo, contrasena, rol)
            VALUES (%s, %s, %s, 'estudiante')
            """,
            (nombre, correo, generate_password_hash(contrasena))
        )

        id_usuario = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO estudiantes
            (id_usuario, edad, fecha_nacimiento)
            VALUES (%s, %s, %s)
            """,
            (id_usuario, edad, fecha_nacimiento)
        )

        conexion.commit()

        flash(f"Se creó la cuenta de {nombre}.", "exito")
        return redirect(url_for("admin.lista_estudiantes"))

    except Exception as error:
        conexion.rollback()
        print(f"Error al crear el estudiante: {error}")
        return mostrar_formulario(
            "crear", admin_actual, datos,
            "No pudimos crear la cuenta. Inténtalo de nuevo."
        )

    finally:
        cursor.close()
        conexion.close()


# =========================================
# EDITAR ESTUDIANTE (Update)
# =========================================

@admin.route(
    "/admin/estudiantes/<int:id_usuario>/editar",
    methods=["GET", "POST"]
)
def editar_estudiante(id_usuario):

    admin_actual = obtener_admin_actual()

    if admin_actual is None:
        return acceso_denegado()

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        estudiante = cargar_estudiante(cursor, id_usuario)
    finally:
        cursor.close()
        conexion.close()

    if estudiante is None:
        flash("No encontramos a ese estudiante.", "error")
        return redirect(url_for("admin.lista_estudiantes"))

    if request.method == "GET":

        fecha = estudiante["fecha_nacimiento"]

        datos = {
            "nombre": estudiante["nombre"],
            "correo": estudiante["correo"],
            "fecha_nacimiento": fecha.isoformat() if fecha else ""
        }

        return mostrar_formulario(
            "editar", admin_actual, datos, estudiante=estudiante
        )

    nombre = request.form.get("nombre", "").strip()
    correo = request.form.get("correo", "").strip()
    contrasena = request.form.get("contrasena", "")
    fecha_texto = request.form.get("fecha_nacimiento", "").strip()

    datos = {
        "nombre": nombre,
        "correo": correo,
        "fecha_nacimiento": fecha_texto
    }

    # -----------------------------------------
    # Validaciones
    # (la contraseña es opcional: vacía = no cambia)
    # -----------------------------------------

    error = validar_nombre(nombre) or validar_correo(correo)

    if not error and contrasena:
        error = validar_contrasena(contrasena)

    if error:
        return mostrar_formulario(
            "editar", admin_actual, datos, error, estudiante
        )

    fecha_nacimiento, edad, error = validar_fecha_nacimiento(fecha_texto)

    if error:
        return mostrar_formulario(
            "editar", admin_actual, datos, error, estudiante
        )

    # -----------------------------------------
    # Guardar
    # -----------------------------------------

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute(
            """
            SELECT id_usuario
            FROM usuarios
            WHERE correo = %s AND id_usuario <> %s
            """,
            (correo, id_usuario)
        )

        if cursor.fetchone() is not None:
            return mostrar_formulario(
                "editar", admin_actual, datos,
                "Ese correo ya lo usa otra cuenta.", estudiante
            )

        cursor.execute(
            """
            UPDATE usuarios
            SET nombre = %s, correo = %s
            WHERE id_usuario = %s
            """,
            (nombre, correo, id_usuario)
        )

        if contrasena:
            cursor.execute(
                "UPDATE usuarios SET contrasena = %s WHERE id_usuario = %s",
                (generate_password_hash(contrasena), id_usuario)
            )

        cursor.execute(
            """
            UPDATE estudiantes
            SET fecha_nacimiento = %s, edad = %s
            WHERE id_usuario = %s
            """,
            (fecha_nacimiento, edad, id_usuario)
        )

        conexion.commit()

        flash(f"Se guardaron los cambios de {nombre}.", "exito")
        return redirect(url_for("admin.lista_estudiantes"))

    except Exception as error:
        conexion.rollback()
        print(f"Error al editar el estudiante: {error}")
        return mostrar_formulario(
            "editar", admin_actual, datos,
            "No pudimos guardar los cambios. Inténtalo de nuevo.",
            estudiante
        )

    finally:
        cursor.close()
        conexion.close()


# =========================================
# ACTIVAR / DESACTIVAR CUENTA
# =========================================

@admin.route(
    "/admin/estudiantes/<int:id_usuario>/estado",
    methods=["POST"]
)
def cambiar_estado(id_usuario):

    admin_actual = obtener_admin_actual()

    if admin_actual is None:
        return acceso_denegado()

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:

        estudiante = cargar_estudiante(cursor, id_usuario)

        if estudiante is None:
            flash("No encontramos a ese estudiante.", "error")
            return destino_lista()

        nuevo_estado = 0 if estudiante["estado"] else 1

        cursor.execute(
            "UPDATE usuarios SET estado = %s WHERE id_usuario = %s",
            (nuevo_estado, id_usuario)
        )

        conexion.commit()

        if nuevo_estado:
            flash(f"La cuenta de {estudiante['nombre']} se activó.", "exito")
        else:
            flash(
                f"La cuenta de {estudiante['nombre']} se desactivó. "
                "Ya no podrá iniciar sesión, pero sus datos se conservan.",
                "exito"
            )

        return destino_lista()

    except Exception as error:
        conexion.rollback()
        print(f"Error al cambiar el estado: {error}")
        flash("No pudimos cambiar el estado de la cuenta.", "error")
        return destino_lista()

    finally:
        cursor.close()
        conexion.close()


# =========================================
# ELIMINAR ESTUDIANTE (Delete)
# =========================================

@admin.route(
    "/admin/estudiantes/<int:id_usuario>/eliminar",
    methods=["GET", "POST"]
)
def eliminar_estudiante(id_usuario):

    admin_actual = obtener_admin_actual()

    if admin_actual is None:
        return acceso_denegado()

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:

        estudiante = cargar_estudiante(cursor, id_usuario)

        if estudiante is None:
            flash("No encontramos a ese estudiante.", "error")
            return redirect(url_for("admin.lista_estudiantes"))

        if request.method == "GET":
            return render_template(
                "admin_eliminar_estudiante.html",
                admin=admin_actual,
                seccion="estudiantes",
                estudiante=estudiante
            )

        # Al borrar el usuario, la base de datos borra sola
        # sus intentos, respuestas, resultados, progreso y logros.
        cursor.execute(
            "DELETE FROM usuarios WHERE id_usuario = %s AND rol = 'estudiante'",
            (id_usuario,)
        )

        conexion.commit()

        flash(f"Se eliminó la cuenta de {estudiante['nombre']}.", "exito")
        return redirect(url_for("admin.lista_estudiantes"))

    except Exception as error:
        conexion.rollback()
        print(f"Error al eliminar el estudiante: {error}")
        flash("No pudimos eliminar la cuenta. Inténtalo de nuevo.", "error")
        return redirect(url_for("admin.lista_estudiantes"))

    finally:
        cursor.close()
        conexion.close()