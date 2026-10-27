from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash
)
from werkzeug.security import generate_password_hash, check_password_hash

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

perfil = Blueprint("perfil", __name__)


# =========================================
# FUNCIONES DE APOYO
# =========================================

def obtener_usuario_actual():
    """
    Busca en la base de datos a la persona que tiene la sesión iniciada.
    Devuelve sus datos, o None si no hay sesión o la cuenta ya no existe.
    """
    id_usuario = session.get("id_usuario")

    if id_usuario is None:
        return None

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT u.id_usuario, u.nombre, u.correo, u.rol,
                   u.fecha_registro, e.fecha_nacimiento
            FROM usuarios u
            LEFT JOIN estudiantes e ON e.id_usuario = u.id_usuario
            WHERE u.id_usuario = %s
            """,
            (id_usuario,)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        conexion.close()


def sin_sesion():
    """
    Se usa cuando no hay sesión válida: limpia lo que quede
    y manda a la persona a iniciar sesión.
    """
    session.clear()
    return redirect(url_for("auth.login"))


def datos_de_enlace_volver(usuario):
    """
    A dónde lleva el botón "Volver" de la parte de arriba.
    """
    if usuario["rol"] == "estudiante":
        return url_for("inicio_estudiante"), "Volver a mi aventura"

    return url_for("inicio"), "Volver al inicio"


def mostrar_perfil(usuario, error_datos=None, error_contrasena=None,
                   datos=None):
    """
    Muestra la página "Mi perfil". Si hubo un error en alguno de los
    formularios, lo muestra en ese formulario y conserva lo escrito.
    """
    fecha_nacimiento = usuario["fecha_nacimiento"]

    edad = calcular_edad(fecha_nacimiento) if fecha_nacimiento else None

    # Lo que aparece escrito en el formulario de datos
    if datos is None:
        datos = {
            "nombre": usuario["nombre"],
            "correo": usuario["correo"],
            "fecha_nacimiento": (
                fecha_nacimiento.isoformat() if fecha_nacimiento else ""
            )
        }

    fecha_min, fecha_max = limites_fecha_nacimiento()
    volver_url, volver_texto = datos_de_enlace_volver(usuario)

    return render_template(
        "perfil.html",
        usuario=usuario,
        edad=edad,
        es_estudiante=(usuario["rol"] == "estudiante"),
        datos=datos,
        error_datos=error_datos,
        error_contrasena=error_contrasena,
        fecha_min=fecha_min.isoformat(),
        fecha_max=fecha_max.isoformat(),
        edad_minima=EDAD_MINIMA,
        edad_maxima=EDAD_MAXIMA,
        volver_url=volver_url,
        volver_texto=volver_texto
    )


def mostrar_eliminar(usuario, error=None):
    """
    Muestra la página de confirmación para eliminar la cuenta.
    """
    return render_template(
        "eliminar_cuenta.html",
        usuario=usuario,
        error=error,
        volver_url=url_for("perfil.ver_perfil"),
        volver_texto="Volver a mi perfil"
    )


# =========================================
# VER EL PERFIL (Read)
# =========================================

@perfil.route("/perfil")
def ver_perfil():

    usuario = obtener_usuario_actual()

    if usuario is None:
        return sin_sesion()

    return mostrar_perfil(usuario)


# =========================================
# EDITAR LOS DATOS (Update)
# =========================================

@perfil.route("/perfil/datos", methods=["POST"])
def editar_datos():

    usuario = obtener_usuario_actual()

    if usuario is None:
        return sin_sesion()

    es_estudiante = usuario["rol"] == "estudiante"

    nombre = request.form.get("nombre", "").strip()
    correo = request.form.get("correo", "").strip()
    fecha_texto = request.form.get("fecha_nacimiento", "").strip()

    datos = {
        "nombre": nombre,
        "correo": correo,
        "fecha_nacimiento": fecha_texto
    }

    # -----------------------------------------
    # Validaciones
    # -----------------------------------------

    error = validar_nombre(nombre) or validar_correo(correo)

    if error:
        return mostrar_perfil(usuario, error_datos=error, datos=datos)

    fecha_nacimiento = None
    edad = None

    # Solo los estudiantes tienen fecha de nacimiento
    if es_estudiante:

        fecha_nacimiento, edad, error = validar_fecha_nacimiento(fecha_texto)

        if error:
            return mostrar_perfil(usuario, error_datos=error, datos=datos)

    # -----------------------------------------
    # Guardar los cambios
    # -----------------------------------------

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        # El correo no puede ser el de otra cuenta
        cursor.execute(
            """
            SELECT id_usuario
            FROM usuarios
            WHERE correo = %s AND id_usuario <> %s
            """,
            (correo, usuario["id_usuario"])
        )

        if cursor.fetchone() is not None:
            return mostrar_perfil(
                usuario,
                error_datos="Ese correo ya lo usa otra cuenta.",
                datos=datos
            )

        cursor.execute(
            """
            UPDATE usuarios
            SET nombre = %s, correo = %s
            WHERE id_usuario = %s
            """,
            (nombre, correo, usuario["id_usuario"])
        )

        if es_estudiante:
            cursor.execute(
                """
                UPDATE estudiantes
                SET fecha_nacimiento = %s, edad = %s
                WHERE id_usuario = %s
                """,
                (fecha_nacimiento, edad, usuario["id_usuario"])
            )

        conexion.commit()

        # La página del estudiante saluda con el nombre de la sesión
        session["nombre"] = nombre

        flash("Tus datos se actualizaron correctamente.", "exito")
        return redirect(url_for("perfil.ver_perfil"))

    except Exception as error:
        conexion.rollback()
        print(f"Error al editar el perfil: {error}")
        return mostrar_perfil(
            usuario,
            error_datos="No pudimos guardar los cambios. Inténtalo de nuevo.",
            datos=datos
        )

    finally:
        cursor.close()
        conexion.close()


# =========================================
# CAMBIAR LA CONTRASEÑA (Update)
# =========================================

@perfil.route("/perfil/contrasena", methods=["POST"])
def cambiar_contrasena():

    usuario = obtener_usuario_actual()

    if usuario is None:
        return sin_sesion()

    actual = request.form.get("contrasena_actual", "")
    nueva = request.form.get("contrasena_nueva", "")
    confirmar = request.form.get("contrasena_confirmar", "")

    # -----------------------------------------
    # Validaciones que no necesitan la base de datos
    # -----------------------------------------

    if not actual:
        return mostrar_perfil(
            usuario,
            error_contrasena="Escribe tu contraseña actual."
        )

    error = validar_contrasena(nueva)

    if error:
        return mostrar_perfil(usuario, error_contrasena=error)

    if nueva != confirmar:
        return mostrar_perfil(
            usuario,
            error_contrasena="Las dos contraseñas nuevas no coinciden."
        )

    if nueva == actual:
        return mostrar_perfil(
            usuario,
            error_contrasena="La contraseña nueva debe ser distinta a la actual."
        )

    # -----------------------------------------
    # Revisar la contraseña actual y guardar la nueva
    # -----------------------------------------

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:

        cursor.execute(
            "SELECT contrasena FROM usuarios WHERE id_usuario = %s",
            (usuario["id_usuario"],)
        )

        fila = cursor.fetchone()

        if fila is None or not check_password_hash(
            fila["contrasena"],
            actual
        ):
            return mostrar_perfil(
                usuario,
                error_contrasena="La contraseña actual no es correcta."
            )

        cursor.execute(
            "UPDATE usuarios SET contrasena = %s WHERE id_usuario = %s",
            (generate_password_hash(nueva), usuario["id_usuario"])
        )

        conexion.commit()

        flash("Tu contraseña se cambió correctamente.", "exito")
        return redirect(url_for("perfil.ver_perfil"))

    except Exception as error:
        conexion.rollback()
        print(f"Error al cambiar la contraseña: {error}")
        return mostrar_perfil(
            usuario,
            error_contrasena="No pudimos cambiar la contraseña. "
                             "Inténtalo de nuevo."
        )

    finally:
        cursor.close()
        conexion.close()


# =========================================
# ELIMINAR LA CUENTA (Delete)
# =========================================

@perfil.route("/perfil/eliminar", methods=["GET", "POST"])
def eliminar_cuenta():

    usuario = obtener_usuario_actual()

    if usuario is None:
        return sin_sesion()

    # Por seguridad, una cuenta de administrador no se borra desde aquí
    # (así nunca nos quedamos sin administradores).
    if usuario["rol"] != "estudiante":
        flash(
            "Las cuentas de administrador no se pueden eliminar desde aquí.",
            "error"
        )
        return redirect(url_for("perfil.ver_perfil"))

    if request.method == "GET":
        return mostrar_eliminar(usuario)

    # -----------------------------------------
    # POST: confirmar con la contraseña y borrar
    # -----------------------------------------

    contrasena = request.form.get("contrasena", "")

    if not contrasena:
        return mostrar_eliminar(usuario, "Escribe tu contraseña para confirmar.")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:

        cursor.execute(
            "SELECT contrasena FROM usuarios WHERE id_usuario = %s",
            (usuario["id_usuario"],)
        )

        fila = cursor.fetchone()

        if fila is None or not check_password_hash(
            fila["contrasena"],
            contrasena
        ):
            return mostrar_eliminar(usuario, "La contraseña no es correcta.")

        # Al borrar el usuario, la base de datos borra sola
        # sus intentos, respuestas, resultados, progreso y logros.
        cursor.execute(
            "DELETE FROM usuarios WHERE id_usuario = %s",
            (usuario["id_usuario"],)
        )

        conexion.commit()

    except Exception as error:
        conexion.rollback()
        print(f"Error al eliminar la cuenta: {error}")
        return mostrar_eliminar(usuario, "No pudimos eliminar la cuenta. Inténtalo de nuevo.")

    finally:
        cursor.close()
        conexion.close()

    # Cerrar la sesión y avisar en la pantalla de inicio de sesión
    session.clear()

    flash(
        "Tu cuenta fue eliminada. Si quieres, puedes crear una nueva.",
        "exito"
    )

    return redirect(url_for("auth.login"))