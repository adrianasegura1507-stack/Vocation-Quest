from functools import wraps
from math import ceil

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, g
)

from database import obtener_conexion
from routes.admin import obtener_admin_actual, acceso_denegado

# Este archivo administra el "catálogo" de Vocation Quest:
#   - Carreras      (y a qué áreas vocacionales pertenecen)
#   - Instituciones (universidades, SENA, institutos...)
#   - Programas     (lo que ofrece cada institución, ligado a una carrera)
#
# Las tres secciones funcionan igual que la de estudiantes:
# listar, crear, editar, activar/desactivar y eliminar.

catalogo = Blueprint("catalogo", __name__)

# Cuántos registros se muestran por página
POR_PAGINA = 15

TIPOS_PROGRAMA = [
    ("universitario", "Universitario"),
    ("tecnologico", "Tecnólogo"),
    ("tecnico", "Técnico"),
    ("curso", "Curso"),
]

MODALIDADES = [
    ("presencial", "Presencial"),
    ("distancia", "A distancia"),
    ("virtual", "Virtual"),
    ("mixta", "Mixta"),
]

# Sugerencias para el tipo de institución (se puede escribir otra cosa)
TIPOS_INSTITUCION = [
    "Universidad",
    "Institución universitaria",
    "Institución tecnológica",
    "SENA",
    "Instituto técnico",
]

SECTORES = [
    ("publica", "Pública"),
    ("privada", "Privada"),
]

ETIQUETA_TIPO = dict(TIPOS_PROGRAMA)
ETIQUETA_SECTOR = dict(SECTORES)


# =========================================
# FUNCIONES DE APOYO
# =========================================

def solo_admin(vista):
    """
    Decorador: deja pasar solo a administradores activos.
    Si no lo son, los manda a iniciar sesión o a su página.
    """
    @wraps(vista)
    def envoltura(*args, **kwargs):

        admin_actual = obtener_admin_actual()

        if admin_actual is None:
            return acceso_denegado()

        g.admin_actual = admin_actual

        return vista(*args, **kwargs)

    return envoltura


def leer(nombre):
    """Lee un campo del formulario, sin espacios sobrantes."""
    return request.form.get(nombre, "").strip()


def es_enlace_valido(texto):
    return texto.startswith("http://") or texto.startswith("https://")


def calcular_paginas(total, pagina):
    total_paginas = max(1, ceil(total / POR_PAGINA))
    pagina = max(1, min(pagina, total_paginas))
    desde = (pagina - 1) * POR_PAGINA
    return pagina, total_paginas, desde


def direccion_actual():
    """Dirección actual (con búsqueda y página), para volver aquí."""
    if request.query_string:
        return request.full_path
    return request.path


def volver_a_lista(endpoint):
    """
    Vuelve a la lista, en la misma página y con los mismos filtros
    donde estaba la persona.
    """
    volver = request.form.get("volver", "")

    if volver.startswith("/admin/") and not volver.startswith("//"):
        return redirect(volver)

    return redirect(url_for(endpoint))


def enlaces_de_pagina(endpoint, filtros, pagina, total_paginas):
    """Devuelve (enlace_anterior, enlace_siguiente) conservando los filtros."""
    activos = {k: v for k, v in filtros.items() if v not in (None, "")}

    anterior = None
    siguiente = None

    if pagina > 1:
        anterior = url_for(endpoint, **activos, pagina=pagina - 1)

    if pagina < total_paginas:
        siguiente = url_for(endpoint, **activos, pagina=pagina + 1)

    return anterior, siguiente


def mostrar_lista(**datos):
    return render_template(
        "admin_catalogo_lista.html",
        admin=g.admin_actual,
        **datos
    )


def mostrar_formulario(seccion, titulo, url_lista, campos, error=None,
                       texto_boton="Guardar"):
    return render_template(
        "admin_catalogo_form.html",
        admin=g.admin_actual,
        seccion=seccion,
        titulo=titulo,
        url_lista=url_lista,
        campos=campos,
        error=error,
        texto_boton=texto_boton
    )


def cambiar_estado(tabla, columna_id, endpoint_lista, id_item):
    """
    Activa o desactiva un registro. Desactivar lo oculta de los
    resultados, pero conserva sus datos.
    (tabla y columna_id vienen del código, nunca del usuario.)
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:

        cursor.execute(
            f"SELECT nombre, estado FROM {tabla} WHERE {columna_id} = %s",
            (id_item,)
        )

        fila = cursor.fetchone()

        if fila is None:
            flash("No encontramos ese registro.", "error")
            return volver_a_lista(endpoint_lista)

        nuevo_estado = 0 if fila["estado"] else 1

        cursor.execute(
            f"UPDATE {tabla} SET estado = %s WHERE {columna_id} = %s",
            (nuevo_estado, id_item)
        )

        conexion.commit()

        if nuevo_estado:
            flash(f"«{fila['nombre']}» se activó.", "exito")
        else:
            flash(
                f"«{fila['nombre']}» se desactivó. Ya no aparece en los "
                "resultados, pero sus datos se conservan.",
                "exito"
            )

    except Exception as error:
        conexion.rollback()
        print(f"Error al cambiar el estado: {error}")
        flash("No pudimos cambiar el estado.", "error")

    finally:
        cursor.close()
        conexion.close()

    return volver_a_lista(endpoint_lista)


def eliminar_registro(tabla, columna_id, singular, seccion,
                      endpoint_lista, id_item, consulta_efecto, texto_efecto):
    """
    Muestra la página de confirmación (GET) y elimina (POST).
    consulta_efecto cuenta cuántos registros relacionados se verán
    afectados; texto_efecto arma el aviso con ese número.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:

        cursor.execute(
            f"SELECT nombre FROM {tabla} WHERE {columna_id} = %s",
            (id_item,)
        )

        fila = cursor.fetchone()

        if fila is None:
            flash("No encontramos ese registro.", "error")
            return redirect(url_for(endpoint_lista))

        if request.method == "GET":

            cursor.execute(consulta_efecto, (id_item,))
            cantidad = cursor.fetchone()["n"]

            return render_template(
                "admin_catalogo_eliminar.html",
                admin=g.admin_actual,
                seccion=seccion,
                singular=singular,
                nombre=fila["nombre"],
                aviso=texto_efecto(cantidad),
                url_lista=url_for(endpoint_lista)
            )

        cursor.execute(
            f"DELETE FROM {tabla} WHERE {columna_id} = %s",
            (id_item,)
        )

        conexion.commit()

        flash(f"Se eliminó «{fila['nombre']}».", "exito")
        return redirect(url_for(endpoint_lista))

    except Exception as error:
        conexion.rollback()
        print(f"Error al eliminar: {error}")
        flash("No pudimos eliminar el registro. Inténtalo de nuevo.", "error")
        return redirect(url_for(endpoint_lista))

    finally:
        cursor.close()
        conexion.close()


# =========================================
# CARRERAS
# =========================================

def campos_carrera(datos, areas, marcadas):
    return [
        {
            "nombre": "nombre", "etiqueta": "Nombre de la carrera",
            "tipo": "texto", "valor": datos.get("nombre", ""),
            "requerido": True, "maximo": 150,
            "ayuda": "Ejemplo: Ingeniería de Sistemas."
        },
        {
            "nombre": "descripcion", "etiqueta": "Descripción",
            "tipo": "area", "valor": datos.get("descripcion", ""),
            "ayuda": "De qué trata la carrera, en pocas líneas."
        },
        {
            "nombre": "perfil_profesional", "etiqueta": "Perfil profesional",
            "tipo": "area", "valor": datos.get("perfil_profesional", ""),
            "ayuda": "Qué sabe hacer quien se gradúa."
        },
        {
            "nombre": "campo_laboral", "etiqueta": "Campo laboral",
            "tipo": "area", "valor": datos.get("campo_laboral", ""),
            "ayuda": "Dónde puede trabajar."
        },
        {
            "nombre": "areas", "etiqueta": "Áreas vocacionales",
            "tipo": "casillas", "requerido": True,
            "opciones": [(str(a["id_area"]), a["nombre"]) for a in areas],
            "marcadas": marcadas,
            "ayuda": "Marca al menos un área. Así la carrera aparece en "
                     "los resultados de esa área."
        },
    ]


@catalogo.route("/admin/carreras")
@solo_admin
def lista_carreras():

    busqueda = request.args.get("q", "").strip()
    id_area = request.args.get("area", type=int)
    estado = request.args.get("estado", "")
    pagina = request.args.get("pagina", 1, type=int) or 1

    condiciones = ["c.nombre LIKE %s"]
    parametros = [f"%{busqueda}%"]

    if id_area:
        condiciones.append(
            "EXISTS (SELECT 1 FROM carrera_area ca "
            "WHERE ca.id_carrera = c.id_carrera AND ca.id_area = %s)"
        )
        parametros.append(id_area)

    if estado in ("0", "1"):
        condiciones.append("c.estado = %s")
        parametros.append(int(estado))

    donde = " AND ".join(condiciones)

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:

        cursor.execute(
            f"SELECT COUNT(*) AS total FROM carreras c WHERE {donde}",
            tuple(parametros)
        )

        total = cursor.fetchone()["total"]

        pagina, total_paginas, desde = calcular_paginas(total, pagina)

        cursor.execute(
            f"""
            SELECT c.id_carrera, c.nombre, c.estado,
                   (
                       SELECT COUNT(*)
                       FROM programa_carrera pc
                       WHERE pc.id_carrera = c.id_carrera
                   ) AS programas
            FROM carreras c
            WHERE {donde}
            ORDER BY c.nombre
            LIMIT %s OFFSET %s
            """,
            tuple(parametros) + (POR_PAGINA, desde)
        )

        filas = cursor.fetchall()

        # Áreas de cada carrera de esta página
        areas_de = {}

        if filas:

            marcadores = ", ".join(["%s"] * len(filas))

            cursor.execute(
                f"""
                SELECT ca.id_carrera, a.nombre
                FROM carrera_area ca
                INNER JOIN areas a ON a.id_area = ca.id_area
                WHERE ca.id_carrera IN ({marcadores})
                ORDER BY a.nombre
                """,
                tuple(f["id_carrera"] for f in filas)
            )

            for r in cursor.fetchall():
                areas_de.setdefault(r["id_carrera"], []).append(r["nombre"])

        cursor.execute("SELECT id_area, nombre FROM areas ORDER BY nombre")
        areas = cursor.fetchall()

    finally:
        cursor.close()
        conexion.close()

    filas_vista = []

    for f in filas:

        i = f["id_carrera"]

        filas_vista.append({
            "celdas": [
                f["nombre"],
                ", ".join(areas_de.get(i, [])) or "—",
                f["programas"]
            ],
            "activo": bool(f["estado"]),
            "url_editar": url_for("catalogo.editar_carrera", id_item=i),
            "url_estado": url_for("catalogo.estado_carrera", id_item=i),
            "url_eliminar": url_for("catalogo.eliminar_carrera", id_item=i),
        })

    anterior, siguiente = enlaces_de_pagina(
        "catalogo.lista_carreras",
        {"q": busqueda, "area": id_area, "estado": estado},
        pagina, total_paginas
    )

    return mostrar_lista(
        seccion="carreras",
        plural="Carreras",
        singular="carrera",
        nuevo_url=url_for("catalogo.nueva_carrera"),
        nuevo_texto="+ Crear carrera",
        url_lista=url_for("catalogo.lista_carreras"),
        columnas=["Carrera", "Áreas", "Programas"],
        filas=filas_vista,
        filtros=[
            {
                "nombre": "area", "etiqueta": "Todas las áreas",
                "opciones": [(str(a["id_area"]), a["nombre"]) for a in areas],
                "valor": str(id_area or "")
            },
            {
                "nombre": "estado", "etiqueta": "Cualquier estado",
                "opciones": [("1", "Activas"), ("0", "Inactivas")],
                "valor": estado
            },
        ],
        busqueda=busqueda,
        texto_busqueda="Buscar carrera por nombre",
        pagina=pagina,
        total_paginas=total_paginas,
        total=total,
        url_anterior=anterior,
        url_siguiente=siguiente,
        volver=direccion_actual()
    )


def formulario_carrera(id_carrera=None):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    editando = id_carrera is not None
    url_lista = url_for("catalogo.lista_carreras")

    try:

        cursor.execute("SELECT id_area, nombre FROM areas ORDER BY id_area")
        areas = cursor.fetchall()

        validas = {str(a["id_area"]) for a in areas}

        existente = None

        if editando:

            cursor.execute(
                """
                SELECT id_carrera, nombre, descripcion,
                       perfil_profesional, campo_laboral
                FROM carreras
                WHERE id_carrera = %s
                """,
                (id_carrera,)
            )

            existente = cursor.fetchone()

            if existente is None:
                flash("No encontramos esa carrera.", "error")
                return redirect(url_lista)

        titulo = "Editar carrera" if editando else "Crear carrera"

        # ---------- Mostrar el formulario ----------

        if request.method == "GET":

            marcadas = set()

            if editando:

                cursor.execute(
                    "SELECT id_area FROM carrera_area WHERE id_carrera = %s",
                    (id_carrera,)
                )

                marcadas = {str(r["id_area"]) for r in cursor.fetchall()}

            return mostrar_formulario(
                "carreras", titulo, url_lista,
                campos_carrera(existente or {}, areas, marcadas)
            )

        # ---------- Guardar ----------

        datos = {
            "nombre": leer("nombre"),
            "descripcion": leer("descripcion"),
            "perfil_profesional": leer("perfil_profesional"),
            "campo_laboral": leer("campo_laboral"),
        }

        marcadas = {a for a in request.form.getlist("areas") if a in validas}

        error = None

        if len(datos["nombre"]) < 3 or len(datos["nombre"]) > 150:
            error = "El nombre debe tener entre 3 y 150 caracteres."
        elif not marcadas:
            error = "Marca al menos un área vocacional."
        else:

            cursor.execute(
                """
                SELECT id_carrera FROM carreras
                WHERE nombre = %s AND id_carrera <> %s
                """,
                (datos["nombre"], id_carrera or 0)
            )

            if cursor.fetchone() is not None:
                error = "Ya existe una carrera con ese nombre."

        if error:
            return mostrar_formulario(
                "carreras", titulo, url_lista,
                campos_carrera(datos, areas, marcadas), error
            )

        try:

            if editando:

                cursor.execute(
                    """
                    UPDATE carreras
                    SET nombre = %s, descripcion = %s,
                        perfil_profesional = %s, campo_laboral = %s
                    WHERE id_carrera = %s
                    """,
                    (
                        datos["nombre"], datos["descripcion"] or None,
                        datos["perfil_profesional"] or None,
                        datos["campo_laboral"] or None, id_carrera
                    )
                )

                cursor.execute(
                    "DELETE FROM carrera_area WHERE id_carrera = %s",
                    (id_carrera,)
                )

                id_guardado = id_carrera

            else:

                cursor.execute(
                    """
                    INSERT INTO carreras
                    (nombre, descripcion, perfil_profesional, campo_laboral)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        datos["nombre"], datos["descripcion"] or None,
                        datos["perfil_profesional"] or None,
                        datos["campo_laboral"] or None
                    )
                )

                id_guardado = cursor.lastrowid

            for id_area in marcadas:
                cursor.execute(
                    "INSERT INTO carrera_area (id_carrera, id_area) "
                    "VALUES (%s, %s)",
                    (id_guardado, int(id_area))
                )

            conexion.commit()

        except Exception as fallo:
            conexion.rollback()
            print(f"Error al guardar la carrera: {fallo}")
            return mostrar_formulario(
                "carreras", titulo, url_lista,
                campos_carrera(datos, areas, marcadas),
                "No pudimos guardar los cambios. Inténtalo de nuevo."
            )

        flash(f"Se guardó la carrera «{datos['nombre']}».", "exito")
        return redirect(url_lista)

    finally:
        cursor.close()
        conexion.close()


@catalogo.route("/admin/carreras/nueva", methods=["GET", "POST"])
@solo_admin
def nueva_carrera():
    return formulario_carrera()


@catalogo.route("/admin/carreras/<int:id_item>/editar", methods=["GET", "POST"])
@solo_admin
def editar_carrera(id_item):
    return formulario_carrera(id_item)


@catalogo.route("/admin/carreras/<int:id_item>/estado", methods=["POST"])
@solo_admin
def estado_carrera(id_item):
    return cambiar_estado(
        "carreras", "id_carrera", "catalogo.lista_carreras", id_item
    )


@catalogo.route(
    "/admin/carreras/<int:id_item>/eliminar", methods=["GET", "POST"]
)
@solo_admin
def eliminar_carrera(id_item):
    return eliminar_registro(
        "carreras", "id_carrera", "la carrera", "carreras",
        "catalogo.lista_carreras", id_item,
        "SELECT COUNT(*) AS n FROM programa_carrera WHERE id_carrera = %s",
        lambda n: (
            f"Se quitará de {n} programa(s) y de sus áreas. Los programas "
            "no se borran, pero dejarán de mostrarse con esta carrera."
        )
    )


# =========================================
# INSTITUCIONES
# =========================================

def campos_institucion(datos):
    return [
        {
            "nombre": "nombre", "etiqueta": "Nombre de la institución",
            "tipo": "texto", "valor": datos.get("nombre", ""),
            "requerido": True, "maximo": 200,
            "ayuda": "Ejemplo: Universidad del Tolima."
        },
        {
            "nombre": "tipo", "etiqueta": "Tipo de institución",
            "tipo": "sugerido", "valor": datos.get("tipo") or "",
            "maximo": 100, "sugerencias": TIPOS_INSTITUCION,
            "ayuda": "Elige una sugerencia o escribe otra."
        },
        {
            "nombre": "sector", "etiqueta": "¿Pública o privada?",
            "tipo": "seleccion", "valor": datos.get("sector") or "",
            "opciones": SECTORES, "marcador": "Sin especificar",
            "ayuda": "Confírmalo en la fuente de la institución."
        },
        {
            "nombre": "sitio_web", "etiqueta": "Sitio web oficial",
            "tipo": "url", "valor": datos.get("sitio_web") or "",
            "maximo": 255,
            "ayuda": "Debe empezar por https://  (por ejemplo, https://www.ut.edu.co)."
        },
        {
            "nombre": "descripcion", "etiqueta": "Descripción",
            "tipo": "area", "valor": datos.get("descripcion") or "",
        },
    ]


@catalogo.route("/admin/instituciones")
@solo_admin
def lista_instituciones():

    busqueda = request.args.get("q", "").strip()
    sector = request.args.get("sector", "")
    estado = request.args.get("estado", "")
    pagina = request.args.get("pagina", 1, type=int) or 1

    condiciones = ["i.nombre LIKE %s"]
    parametros = [f"%{busqueda}%"]

    if sector in ETIQUETA_SECTOR:
        condiciones.append("i.sector = %s")
        parametros.append(sector)

    if estado in ("0", "1"):
        condiciones.append("i.estado = %s")
        parametros.append(int(estado))

    donde = " AND ".join(condiciones)

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:

        cursor.execute(
            f"SELECT COUNT(*) AS total FROM instituciones i WHERE {donde}",
            tuple(parametros)
        )

        total = cursor.fetchone()["total"]

        pagina, total_paginas, desde = calcular_paginas(total, pagina)

        cursor.execute(
            f"""
            SELECT i.id_institucion, i.nombre, i.tipo, i.sector,
                   i.sitio_web, i.estado,
                   (
                       SELECT COUNT(*)
                       FROM programas p
                       WHERE p.id_institucion = i.id_institucion
                   ) AS programas
            FROM instituciones i
            WHERE {donde}
            ORDER BY i.nombre
            LIMIT %s OFFSET %s
            """,
            tuple(parametros) + (POR_PAGINA, desde)
        )

        filas = cursor.fetchall()

    finally:
        cursor.close()
        conexion.close()

    filas_vista = []

    for f in filas:

        i = f["id_institucion"]

        filas_vista.append({
            "celdas": [
                (
                    f["nombre"],
                    " · ".join(
                        parte for parte in (
                            f["tipo"], ETIQUETA_SECTOR.get(f["sector"])
                        ) if parte
                    ) or "Sin tipo"
                ),
                f["programas"],
                f["sitio_web"] or "—"
            ],
            "activo": bool(f["estado"]),
            "url_editar": url_for("catalogo.editar_institucion", id_item=i),
            "url_estado": url_for("catalogo.estado_institucion", id_item=i),
            "url_eliminar": url_for("catalogo.eliminar_institucion", id_item=i),
        })

    anterior, siguiente = enlaces_de_pagina(
        "catalogo.lista_instituciones",
        {"q": busqueda, "sector": sector, "estado": estado},
        pagina, total_paginas
    )

    return mostrar_lista(
        seccion="instituciones",
        plural="Instituciones",
        singular="institución",
        nuevo_url=url_for("catalogo.nueva_institucion"),
        nuevo_texto="+ Crear institución",
        url_lista=url_for("catalogo.lista_instituciones"),
        columnas=["Institución", "Programas", "Sitio web"],
        filas=filas_vista,
        filtros=[
            {
                "nombre": "sector", "etiqueta": "Pública y privada",
                "opciones": SECTORES, "valor": sector
            },
            {
                "nombre": "estado", "etiqueta": "Cualquier estado",
                "opciones": [("1", "Activas"), ("0", "Inactivas")],
                "valor": estado
            },
        ],
        busqueda=busqueda,
        texto_busqueda="Buscar institución por nombre",
        pagina=pagina,
        total_paginas=total_paginas,
        total=total,
        url_anterior=anterior,
        url_siguiente=siguiente,
        volver=direccion_actual()
    )


def formulario_institucion(id_institucion=None):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    editando = id_institucion is not None
    url_lista = url_for("catalogo.lista_instituciones")

    try:

        existente = None

        if editando:

            cursor.execute(
                """
                SELECT id_institucion, nombre, tipo, sector, sitio_web,
                       descripcion
                FROM instituciones
                WHERE id_institucion = %s
                """,
                (id_institucion,)
            )

            existente = cursor.fetchone()

            if existente is None:
                flash("No encontramos esa institución.", "error")
                return redirect(url_lista)

        titulo = "Editar institución" if editando else "Crear institución"

        if request.method == "GET":
            return mostrar_formulario(
                "instituciones", titulo, url_lista,
                campos_institucion(existente or {})
            )

        datos = {
            "nombre": leer("nombre"),
            "tipo": leer("tipo"),
            "sector": leer("sector"),
            "sitio_web": leer("sitio_web"),
            "descripcion": leer("descripcion"),
        }

        error = None

        if len(datos["nombre"]) < 3 or len(datos["nombre"]) > 200:
            error = "El nombre debe tener entre 3 y 200 caracteres."
        elif len(datos["tipo"]) > 100:
            error = "El tipo no puede pasar de 100 caracteres."
        elif datos["sector"] and datos["sector"] not in ETIQUETA_SECTOR:
            error = "El sector elegido no es válido."
        elif datos["sitio_web"] and (
            not es_enlace_valido(datos["sitio_web"])
            or len(datos["sitio_web"]) > 255
        ):
            error = ("El sitio web debe empezar por http:// o https:// "
                     "y tener máximo 255 caracteres.")
        else:

            cursor.execute(
                """
                SELECT id_institucion FROM instituciones
                WHERE nombre = %s AND id_institucion <> %s
                """,
                (datos["nombre"], id_institucion or 0)
            )

            if cursor.fetchone() is not None:
                error = "Ya existe una institución con ese nombre."

        if error:
            return mostrar_formulario(
                "instituciones", titulo, url_lista,
                campos_institucion(datos), error
            )

        try:

            valores = (
                datos["nombre"], datos["tipo"] or None,
                datos["sector"] or None,
                datos["sitio_web"] or None, datos["descripcion"] or None
            )

            if editando:
                cursor.execute(
                    """
                    UPDATE instituciones
                    SET nombre = %s, tipo = %s, sector = %s,
                        sitio_web = %s, descripcion = %s
                    WHERE id_institucion = %s
                    """,
                    valores + (id_institucion,)
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO instituciones
                    (nombre, tipo, sector, sitio_web, descripcion)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    valores
                )

            conexion.commit()

        except Exception as fallo:
            conexion.rollback()
            print(f"Error al guardar la institución: {fallo}")
            return mostrar_formulario(
                "instituciones", titulo, url_lista,
                campos_institucion(datos),
                "No pudimos guardar los cambios. Inténtalo de nuevo."
            )

        flash(f"Se guardó la institución «{datos['nombre']}».", "exito")
        return redirect(url_lista)

    finally:
        cursor.close()
        conexion.close()


@catalogo.route("/admin/instituciones/nueva", methods=["GET", "POST"])
@solo_admin
def nueva_institucion():
    return formulario_institucion()


@catalogo.route(
    "/admin/instituciones/<int:id_item>/editar", methods=["GET", "POST"]
)
@solo_admin
def editar_institucion(id_item):
    return formulario_institucion(id_item)


@catalogo.route("/admin/instituciones/<int:id_item>/estado", methods=["POST"])
@solo_admin
def estado_institucion(id_item):
    return cambiar_estado(
        "instituciones", "id_institucion",
        "catalogo.lista_instituciones", id_item
    )


@catalogo.route(
    "/admin/instituciones/<int:id_item>/eliminar", methods=["GET", "POST"]
)
@solo_admin
def eliminar_institucion(id_item):
    return eliminar_registro(
        "instituciones", "id_institucion", "la institución", "instituciones",
        "catalogo.lista_instituciones", id_item,
        "SELECT COUNT(*) AS n FROM programas WHERE id_institucion = %s",
        lambda n: (
            f"También se eliminarán sus {n} programa(s). Si solo quieres "
            "que deje de aparecer en los resultados, es mejor desactivarla."
        )
    )


# =========================================
# PROGRAMAS
# =========================================

def campos_programa(datos, instituciones, carreras, marcadas):
    return [
        {
            "nombre": "id_institucion", "etiqueta": "Institución",
            "tipo": "seleccion", "requerido": True,
            "valor": str(datos.get("id_institucion") or ""),
            "opciones": [
                (str(i["id_institucion"]),
                 i["nombre"] + ("" if i["estado"] else " (inactiva)"))
                for i in instituciones
            ],
            "marcador": "Elige la institución",
            "ayuda": "Si no está en la lista, créala primero en Instituciones."
        },
        {
            "nombre": "nombre", "etiqueta": "Nombre del programa",
            "tipo": "texto", "valor": datos.get("nombre", ""),
            "requerido": True, "maximo": 200,
            "ayuda": "Tal como lo escribe la institución. "
                     "Ejemplo: Ingeniería de Sistemas."
        },
        {
            "nombre": "tipo", "etiqueta": "Tipo de programa",
            "tipo": "seleccion", "requerido": True,
            "valor": datos.get("tipo") or "",
            "opciones": TIPOS_PROGRAMA, "marcador": "Elige el tipo",
        },
        {
            "nombre": "modalidad", "etiqueta": "Modalidad",
            "tipo": "seleccion", "valor": datos.get("modalidad") or "",
            "opciones": MODALIDADES, "marcador": "Sin especificar",
        },
        {
            "nombre": "ciudad", "etiqueta": "Ciudad o sede",
            "tipo": "texto", "valor": datos.get("ciudad") or "",
            "maximo": 100,
            "ayuda": "Si el programa se ofrece en dos ciudades, créalo una "
                     "vez por cada ciudad."
        },
        {
            "nombre": "duracion", "etiqueta": "Duración",
            "tipo": "texto", "valor": datos.get("duracion") or "",
            "maximo": 100,
            "ayuda": "Opcional. Escríbela solo si la conoces con certeza "
                     "(por ejemplo, 10 semestres)."
        },
        {
            "nombre": "sitio_web", "etiqueta": "Enlace del programa",
            "tipo": "url", "valor": datos.get("sitio_web") or "",
            "maximo": 255,
            "ayuda": "Opcional. Si lo dejas vacío, se usa el sitio de la "
                     "institución."
        },
        {
            "nombre": "descripcion", "etiqueta": "Descripción",
            "tipo": "area", "valor": datos.get("descripcion") or "",
        },
        {
            "nombre": "carreras", "etiqueta": "Carrera(s) a la que pertenece",
            "tipo": "casillas", "requerido": True,
            "opciones": [
                (str(c["id_carrera"]),
                 c["nombre"] + ("" if c["estado"] else " (inactiva)"))
                for c in carreras
            ],
            "marcadas": marcadas,
            "ayuda": "Marca al menos una. Si la carrera no existe, créala "
                     "primero en Carreras."
        },
    ]


@catalogo.route("/admin/programas")
@solo_admin
def lista_programas():

    busqueda = request.args.get("q", "").strip()
    id_institucion = request.args.get("institucion", type=int)
    tipo = request.args.get("tipo", "")
    estado = request.args.get("estado", "")
    pagina = request.args.get("pagina", 1, type=int) or 1

    condiciones = ["(p.nombre LIKE %s OR i.nombre LIKE %s)"]
    parametros = [f"%{busqueda}%", f"%{busqueda}%"]

    if id_institucion:
        condiciones.append("p.id_institucion = %s")
        parametros.append(id_institucion)

    if tipo in ETIQUETA_TIPO:
        condiciones.append("p.tipo = %s")
        parametros.append(tipo)

    if estado in ("0", "1"):
        condiciones.append("p.estado = %s")
        parametros.append(int(estado))

    donde = " AND ".join(condiciones)

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:

        cursor.execute(
            f"""
            SELECT COUNT(*) AS total
            FROM programas p
            INNER JOIN instituciones i ON i.id_institucion = p.id_institucion
            WHERE {donde}
            """,
            tuple(parametros)
        )

        total = cursor.fetchone()["total"]

        pagina, total_paginas, desde = calcular_paginas(total, pagina)

        cursor.execute(
            f"""
            SELECT p.id_programa, p.nombre, p.tipo, p.ciudad, p.modalidad,
                   p.estado, i.nombre AS institucion
            FROM programas p
            INNER JOIN instituciones i ON i.id_institucion = p.id_institucion
            WHERE {donde}
            ORDER BY i.nombre, p.nombre, p.ciudad
            LIMIT %s OFFSET %s
            """,
            tuple(parametros) + (POR_PAGINA, desde)
        )

        filas = cursor.fetchall()

        # Carreras de cada programa de esta página
        carreras_de = {}

        if filas:

            marcadores = ", ".join(["%s"] * len(filas))

            cursor.execute(
                f"""
                SELECT pc.id_programa, c.nombre
                FROM programa_carrera pc
                INNER JOIN carreras c ON c.id_carrera = pc.id_carrera
                WHERE pc.id_programa IN ({marcadores})
                ORDER BY c.nombre
                """,
                tuple(f["id_programa"] for f in filas)
            )

            for r in cursor.fetchall():
                carreras_de.setdefault(r["id_programa"], []).append(r["nombre"])

        cursor.execute(
            "SELECT id_institucion, nombre FROM instituciones ORDER BY nombre"
        )

        instituciones = cursor.fetchall()

    finally:
        cursor.close()
        conexion.close()

    etiqueta_modalidad = dict(MODALIDADES)

    filas_vista = []

    for f in filas:

        i = f["id_programa"]

        sede = " · ".join(
            parte for parte in (
                f["ciudad"], etiqueta_modalidad.get(f["modalidad"])
            ) if parte
        ) or "—"

        filas_vista.append({
            "celdas": [
                (f["nombre"], f["institucion"]),
                ETIQUETA_TIPO.get(f["tipo"], f["tipo"]),
                sede,
                ", ".join(carreras_de.get(i, [])) or "Sin carrera",
            ],
            "activo": bool(f["estado"]),
            "url_editar": url_for("catalogo.editar_programa", id_item=i),
            "url_estado": url_for("catalogo.estado_programa", id_item=i),
            "url_eliminar": url_for("catalogo.eliminar_programa", id_item=i),
        })

    anterior, siguiente = enlaces_de_pagina(
        "catalogo.lista_programas",
        {
            "q": busqueda, "institucion": id_institucion,
            "tipo": tipo, "estado": estado
        },
        pagina, total_paginas
    )

    return mostrar_lista(
        seccion="programas",
        plural="Programas",
        singular="programa",
        nuevo_url=url_for("catalogo.nuevo_programa"),
        nuevo_texto="+ Crear programa",
        url_lista=url_for("catalogo.lista_programas"),
        columnas=["Programa", "Tipo", "Sede", "Carrera(s)"],
        filas=filas_vista,
        filtros=[
            {
                "nombre": "institucion", "etiqueta": "Todas las instituciones",
                "opciones": [
                    (str(x["id_institucion"]), x["nombre"])
                    for x in instituciones
                ],
                "valor": str(id_institucion or "")
            },
            {
                "nombre": "tipo", "etiqueta": "Todos los tipos",
                "opciones": TIPOS_PROGRAMA, "valor": tipo
            },
            {
                "nombre": "estado", "etiqueta": "Cualquier estado",
                "opciones": [("1", "Activos"), ("0", "Inactivos")],
                "valor": estado
            },
        ],
        busqueda=busqueda,
        texto_busqueda="Buscar por programa o institución",
        pagina=pagina,
        total_paginas=total_paginas,
        total=total,
        url_anterior=anterior,
        url_siguiente=siguiente,
        volver=direccion_actual()
    )


def formulario_programa(id_programa=None):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    editando = id_programa is not None
    url_lista = url_for("catalogo.lista_programas")

    try:

        cursor.execute(
            "SELECT id_institucion, nombre, estado FROM instituciones "
            "ORDER BY nombre"
        )
        instituciones = cursor.fetchall()

        cursor.execute(
            "SELECT id_carrera, nombre, estado FROM carreras ORDER BY nombre"
        )
        carreras = cursor.fetchall()

        ids_instituciones = {str(i["id_institucion"]) for i in instituciones}
        ids_carreras = {str(c["id_carrera"]) for c in carreras}

        existente = None

        if editando:

            cursor.execute(
                """
                SELECT id_programa, id_institucion, nombre, tipo, modalidad,
                       ciudad, duracion, sitio_web, descripcion
                FROM programas
                WHERE id_programa = %s
                """,
                (id_programa,)
            )

            existente = cursor.fetchone()

            if existente is None:
                flash("No encontramos ese programa.", "error")
                return redirect(url_lista)

        titulo = "Editar programa" if editando else "Crear programa"

        # ---------- Mostrar el formulario ----------

        if request.method == "GET":

            marcadas = set()

            if editando:

                cursor.execute(
                    "SELECT id_carrera FROM programa_carrera "
                    "WHERE id_programa = %s",
                    (id_programa,)
                )

                marcadas = {str(r["id_carrera"]) for r in cursor.fetchall()}

            return mostrar_formulario(
                "programas", titulo, url_lista,
                campos_programa(
                    existente or {}, instituciones, carreras, marcadas
                )
            )

        # ---------- Guardar ----------

        datos = {
            "id_institucion": leer("id_institucion"),
            "nombre": leer("nombre"),
            "tipo": leer("tipo"),
            "modalidad": leer("modalidad"),
            "ciudad": leer("ciudad"),
            "duracion": leer("duracion"),
            "sitio_web": leer("sitio_web"),
            "descripcion": leer("descripcion"),
        }

        marcadas = {
            c for c in request.form.getlist("carreras") if c in ids_carreras
        }

        def campos():
            return campos_programa(datos, instituciones, carreras, marcadas)

        error = None

        if datos["id_institucion"] not in ids_instituciones:
            error = "Elige la institución."
        elif len(datos["nombre"]) < 3 or len(datos["nombre"]) > 200:
            error = "El nombre debe tener entre 3 y 200 caracteres."
        elif datos["tipo"] not in ETIQUETA_TIPO:
            error = "Elige el tipo de programa."
        elif datos["modalidad"] and datos["modalidad"] not in dict(MODALIDADES):
            error = "La modalidad elegida no es válida."
        elif len(datos["ciudad"]) > 100 or len(datos["duracion"]) > 100:
            error = "La ciudad y la duración no pueden pasar de 100 caracteres."
        elif datos["sitio_web"] and (
            not es_enlace_valido(datos["sitio_web"])
            or len(datos["sitio_web"]) > 255
        ):
            error = ("El enlace debe empezar por http:// o https:// "
                     "y tener máximo 255 caracteres.")
        elif not marcadas:
            error = "Marca al menos una carrera."
        else:

            # Mismo programa, en la misma institución y la misma ciudad
            cursor.execute(
                """
                SELECT id_programa FROM programas
                WHERE id_institucion = %s
                AND nombre = %s
                AND ((%s = '' AND ciudad IS NULL) OR ciudad = %s)
                AND id_programa <> %s
                """,
                (
                    int(datos["id_institucion"]), datos["nombre"],
                    datos["ciudad"], datos["ciudad"], id_programa or 0
                )
            )

            if cursor.fetchone() is not None:
                error = ("Ese programa ya existe en esa institución y esa "
                         "ciudad.")

        if error:
            return mostrar_formulario(
                "programas", titulo, url_lista, campos(), error
            )

        try:

            valores = (
                int(datos["id_institucion"]), datos["nombre"], datos["tipo"],
                datos["descripcion"] or None, datos["duracion"] or None,
                datos["sitio_web"] or None, datos["ciudad"] or None,
                datos["modalidad"] or None
            )

            if editando:

                cursor.execute(
                    """
                    UPDATE programas
                    SET id_institucion = %s, nombre = %s, tipo = %s,
                        descripcion = %s, duracion = %s, sitio_web = %s,
                        ciudad = %s, modalidad = %s
                    WHERE id_programa = %s
                    """,
                    valores + (id_programa,)
                )

                cursor.execute(
                    "DELETE FROM programa_carrera WHERE id_programa = %s",
                    (id_programa,)
                )

                id_guardado = id_programa

            else:

                cursor.execute(
                    """
                    INSERT INTO programas
                    (id_institucion, nombre, tipo, descripcion, duracion,
                     sitio_web, ciudad, modalidad)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    valores
                )

                id_guardado = cursor.lastrowid

            for id_carrera in marcadas:
                cursor.execute(
                    "INSERT INTO programa_carrera (id_programa, id_carrera) "
                    "VALUES (%s, %s)",
                    (id_guardado, int(id_carrera))
                )

            conexion.commit()

        except Exception as fallo:
            conexion.rollback()
            print(f"Error al guardar el programa: {fallo}")
            return mostrar_formulario(
                "programas", titulo, url_lista, campos(),
                "No pudimos guardar los cambios. Inténtalo de nuevo."
            )

        flash(f"Se guardó el programa «{datos['nombre']}».", "exito")
        return redirect(url_lista)

    finally:
        cursor.close()
        conexion.close()


@catalogo.route("/admin/programas/nuevo", methods=["GET", "POST"])
@solo_admin
def nuevo_programa():
    return formulario_programa()


@catalogo.route(
    "/admin/programas/<int:id_item>/editar", methods=["GET", "POST"]
)
@solo_admin
def editar_programa(id_item):
    return formulario_programa(id_item)


@catalogo.route("/admin/programas/<int:id_item>/estado", methods=["POST"])
@solo_admin
def estado_programa(id_item):
    return cambiar_estado(
        "programas", "id_programa", "catalogo.lista_programas", id_item
    )


@catalogo.route(
    "/admin/programas/<int:id_item>/eliminar", methods=["GET", "POST"]
)
@solo_admin
def eliminar_programa(id_item):
    return eliminar_registro(
        "programas", "id_programa", "el programa", "programas",
        "catalogo.lista_programas", id_item,
        "SELECT COUNT(*) AS n FROM programa_carrera WHERE id_programa = %s",
        lambda n: (
            f"Se quitará su relación con {n} carrera(s). Si solo quieres "
            "que deje de aparecer en los resultados, es mejor desactivarlo."
        )
    )