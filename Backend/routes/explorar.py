from math import ceil

from flask import (
    Blueprint, render_template, request, redirect, url_for, session
)

from database import obtener_conexion
from routes.pruebas import (
    ETIQUETAS_TIPO, ETIQUETAS_MODALIDAD, ETIQUETAS_SECTOR
)

# Página "Explorar": cualquier persona con sesión iniciada puede buscar
# carreras y ver en qué instituciones, ciudades y modalidades se estudian.
#
#   /explorar                    -> lista de carreras con filtros
#   /explorar/carrera/<id>       -> una carrera con todos sus programas

explorar = Blueprint("explorar", __name__)

# Cuántas carreras se muestran por página
POR_PAGINA = 12


# =========================================
# FUNCIONES DE APOYO
# =========================================

def a_donde_volver():
    """El botón "Volver" lleva a la página principal de cada rol."""
    if session.get("rol") == "administrador":
        return url_for("admin.panel"), "Volver al panel"

    return url_for("inicio_estudiante"), "Volver a mi aventura"


def valor_valido(valor, permitidos):
    """Solo acepta valores conocidos; si no, ignora el filtro."""
    return valor if valor in permitidos else ""


def enlaces_de_pagina(endpoint, filtros, pagina, total_paginas, **fijos):
    """Enlaces a la página anterior y siguiente, conservando los filtros."""
    activos = {k: v for k, v in filtros.items() if v not in (None, "")}

    anterior = None
    siguiente = None

    if pagina > 1:
        anterior = url_for(endpoint, **fijos, **activos, pagina=pagina - 1)

    if pagina < total_paginas:
        siguiente = url_for(endpoint, **fijos, **activos, pagina=pagina + 1)

    return anterior, siguiente


def texto_sede(ciudad, modalidad):
    """Ejemplo: "Ibagué · Presencial"."""
    return " · ".join(
        parte for parte in (
            ciudad, ETIQUETAS_MODALIDAD.get(modalidad)
        ) if parte
    )


# =========================================
# LISTA DE CARRERAS
# =========================================

@explorar.route("/explorar")
def lista():

    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    # ----- Filtros que llegan en la dirección -----

    busqueda = request.args.get("q", "").strip()
    id_area = request.args.get("area", type=int)
    id_institucion = request.args.get("institucion", type=int)
    ciudad = request.args.get("ciudad", "").strip()
    tipo = valor_valido(request.args.get("tipo", ""), ETIQUETAS_TIPO)
    modalidad = valor_valido(
        request.args.get("modalidad", ""), ETIQUETAS_MODALIDAD
    )
    sector = valor_valido(request.args.get("sector", ""), ETIQUETAS_SECTOR)
    pagina = max(request.args.get("pagina", 1, type=int) or 1, 1)

    # ----- Filtros sobre los programas (van dentro de la subconsulta) -----

    condiciones_programa = ["p.estado = 1", "i.estado = 1"]
    parametros_programa = []

    if tipo:
        condiciones_programa.append("p.tipo = %s")
        parametros_programa.append(tipo)

    if ciudad:
        condiciones_programa.append("p.ciudad = %s")
        parametros_programa.append(ciudad)

    if modalidad:
        condiciones_programa.append("p.modalidad = %s")
        parametros_programa.append(modalidad)

    if sector:
        condiciones_programa.append("i.sector = %s")
        parametros_programa.append(sector)

    if id_institucion:
        condiciones_programa.append("p.id_institucion = %s")
        parametros_programa.append(id_institucion)

    filtra_programas = len(condiciones_programa) > 2

    subconsulta = f"""
        LEFT JOIN (
            SELECT pc.id_carrera, p.id_programa, p.id_institucion,
                   p.nombre AS programa
            FROM programa_carrera pc
            INNER JOIN programas p ON p.id_programa = pc.id_programa
            INNER JOIN instituciones i
                ON i.id_institucion = p.id_institucion
            WHERE {" AND ".join(condiciones_programa)}
        ) x ON x.id_carrera = c.id_carrera
    """

    # ----- Filtros sobre la carrera -----

    condiciones = ["c.estado = 1"]
    parametros = []

    if busqueda:
        condiciones.append("(c.nombre LIKE %s OR x.programa LIKE %s)")
        parametros.extend([f"%{busqueda}%", f"%{busqueda}%"])

    if id_area:
        condiciones.append(
            "EXISTS (SELECT 1 FROM carrera_area ca "
            "WHERE ca.id_carrera = c.id_carrera AND ca.id_area = %s)"
        )
        parametros.append(id_area)

    # Si se filtra por algo de los programas, solo carreras que tengan alguno
    if filtra_programas:
        condiciones.append("x.id_programa IS NOT NULL")

    donde = " AND ".join(condiciones)

    # Los parámetros van en el mismo orden en que aparecen en el texto SQL:
    # primero los de la subconsulta y después los de la carrera.
    todos = tuple(parametros_programa + parametros)

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:

        cursor.execute(
            f"""
            SELECT COUNT(DISTINCT c.id_carrera) AS total
            FROM carreras c
            {subconsulta}
            WHERE {donde}
            """,
            todos
        )

        total = cursor.fetchone()["total"]

        total_paginas = max(1, ceil(total / POR_PAGINA))
        pagina = min(pagina, total_paginas)
        desde = (pagina - 1) * POR_PAGINA

        cursor.execute(
            f"""
            SELECT c.id_carrera, c.nombre, c.descripcion,
                   COUNT(DISTINCT x.id_programa) AS programas,
                   COUNT(DISTINCT x.id_institucion) AS instituciones
            FROM carreras c
            {subconsulta}
            WHERE {donde}
            GROUP BY c.id_carrera, c.nombre, c.descripcion
            ORDER BY c.nombre
            LIMIT %s OFFSET %s
            """,
            todos + (POR_PAGINA, desde)
        )

        carreras = cursor.fetchall()

        # ----- Áreas y ciudades de las carreras de esta página -----

        areas_de = {}
        ciudades_de = {}

        if carreras:

            marcadores = ", ".join(["%s"] * len(carreras))
            ids = tuple(c["id_carrera"] for c in carreras)

            cursor.execute(
                f"""
                SELECT ca.id_carrera, a.nombre
                FROM carrera_area ca
                INNER JOIN areas a ON a.id_area = ca.id_area
                WHERE ca.id_carrera IN ({marcadores})
                ORDER BY a.nombre
                """,
                ids
            )

            for fila in cursor.fetchall():
                areas_de.setdefault(fila["id_carrera"], []).append(
                    fila["nombre"]
                )

            cursor.execute(
                f"""
                SELECT DISTINCT pc.id_carrera, p.ciudad
                FROM programa_carrera pc
                INNER JOIN programas p ON p.id_programa = pc.id_programa
                INNER JOIN instituciones i
                    ON i.id_institucion = p.id_institucion
                WHERE pc.id_carrera IN ({marcadores})
                AND p.estado = 1 AND i.estado = 1
                AND p.ciudad IS NOT NULL AND p.ciudad <> ''
                ORDER BY p.ciudad
                """,
                ids
            )

            for fila in cursor.fetchall():
                ciudades_de.setdefault(fila["id_carrera"], []).append(
                    fila["ciudad"]
                )

        # ----- Opciones de los filtros -----

        cursor.execute("SELECT id_area, nombre FROM areas ORDER BY nombre")
        areas = cursor.fetchall()

        cursor.execute(
            """
            SELECT DISTINCT p.ciudad
            FROM programas p
            INNER JOIN instituciones i ON i.id_institucion = p.id_institucion
            WHERE p.estado = 1 AND i.estado = 1
            AND p.ciudad IS NOT NULL AND p.ciudad <> ''
            ORDER BY p.ciudad
            """
        )
        ciudades = [f["ciudad"] for f in cursor.fetchall()]

        cursor.execute(
            """
            SELECT DISTINCT i.id_institucion, i.nombre
            FROM instituciones i
            INNER JOIN programas p ON p.id_institucion = i.id_institucion
            WHERE i.estado = 1 AND p.estado = 1
            ORDER BY i.nombre
            """
        )
        instituciones = cursor.fetchall()

    finally:
        cursor.close()
        conexion.close()

    tarjetas = []

    for c in carreras:

        descripcion = c["descripcion"] or ""

        if len(descripcion) > 170:
            descripcion = descripcion[:170].rsplit(" ", 1)[0] + "…"

        tarjetas.append({
            "id_carrera": c["id_carrera"],
            "nombre": c["nombre"],
            "descripcion": descripcion,
            "areas": areas_de.get(c["id_carrera"], []),
            "ciudades": ciudades_de.get(c["id_carrera"], []),
            "programas": c["programas"],
            "instituciones": c["instituciones"],
        })

    filtros = {
        "q": busqueda, "area": id_area, "tipo": tipo, "ciudad": ciudad,
        "institucion": id_institucion, "modalidad": modalidad,
        "sector": sector
    }

    anterior, siguiente = enlaces_de_pagina(
        "explorar.lista", filtros, pagina, total_paginas
    )

    volver_url, volver_texto = a_donde_volver()

    return render_template(
        "explorar.html",
        tarjetas=tarjetas,
        total=total,
        pagina=pagina,
        total_paginas=total_paginas,
        url_anterior=anterior,
        url_siguiente=siguiente,
        busqueda=busqueda,
        areas=areas,
        ciudades=ciudades,
        instituciones=instituciones,
        tipos=list(ETIQUETAS_TIPO.items()),
        modalidades=list(ETIQUETAS_MODALIDAD.items()),
        sectores=list(ETIQUETAS_SECTOR.items()),
        activos={
            "area": str(id_area or ""), "tipo": tipo, "ciudad": ciudad,
            "institucion": str(id_institucion or ""),
            "modalidad": modalidad, "sector": sector
        },
        hay_filtros=bool(
            busqueda or id_area or tipo or ciudad or id_institucion
            or modalidad or sector
        ),
        volver_url=volver_url,
        volver_texto=volver_texto
    )


# =========================================
# UNA CARRERA Y DÓNDE ESTUDIARLA
# =========================================

@explorar.route("/explorar/carrera/<int:id_carrera>")
def ver_carrera(id_carrera):

    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    ciudad = request.args.get("ciudad", "").strip()
    tipo = valor_valido(request.args.get("tipo", ""), ETIQUETAS_TIPO)
    modalidad = valor_valido(
        request.args.get("modalidad", ""), ETIQUETAS_MODALIDAD
    )
    sector = valor_valido(request.args.get("sector", ""), ETIQUETAS_SECTOR)

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT id_carrera, nombre, descripcion, perfil_profesional,
                   campo_laboral
            FROM carreras
            WHERE id_carrera = %s AND estado = 1
            """,
            (id_carrera,)
        )

        carrera = cursor.fetchone()

        if carrera is None:
            return redirect(url_for("explorar.lista"))

        cursor.execute(
            """
            SELECT a.nombre
            FROM carrera_area ca
            INNER JOIN areas a ON a.id_area = ca.id_area
            WHERE ca.id_carrera = %s
            ORDER BY a.nombre
            """,
            (id_carrera,)
        )

        areas = [f["nombre"] for f in cursor.fetchall()]

        # Todos los programas activos de la carrera (sin filtrar), para
        # saber qué opciones ofrecer en los filtros
        base = """
            SELECT p.id_programa, p.nombre, p.tipo, p.descripcion,
                   p.duracion, p.ciudad, p.modalidad,
                   p.sitio_web AS enlace_programa,
                   i.nombre AS institucion, i.sector,
                   i.sitio_web AS enlace_institucion
            FROM programas p
            INNER JOIN programa_carrera pc ON pc.id_programa = p.id_programa
            INNER JOIN instituciones i ON i.id_institucion = p.id_institucion
            WHERE pc.id_carrera = %s
            AND p.estado = 1 AND i.estado = 1
        """

        cursor.execute(
            base + " ORDER BY i.nombre, p.ciudad, p.nombre",
            (id_carrera,)
        )

        todos = cursor.fetchall()

    finally:
        cursor.close()
        conexion.close()

    # Opciones de los filtros: solo lo que esta carrera realmente tiene
    ciudades = sorted({p["ciudad"] for p in todos if p["ciudad"]})
    tipos = [
        (k, v) for k, v in ETIQUETAS_TIPO.items()
        if any(p["tipo"] == k for p in todos)
    ]
    modalidades = [
        (k, v) for k, v in ETIQUETAS_MODALIDAD.items()
        if any(p["modalidad"] == k for p in todos)
    ]
    sectores = [
        (k, v) for k, v in ETIQUETAS_SECTOR.items()
        if any(p["sector"] == k for p in todos)
    ]

    # Aplicar los filtros
    programas = [
        p for p in todos
        if (not ciudad or p["ciudad"] == ciudad)
        and (not tipo or p["tipo"] == tipo)
        and (not modalidad or p["modalidad"] == modalidad)
        and (not sector or p["sector"] == sector)
    ]

    for p in programas:
        p["tipo_texto"] = ETIQUETAS_TIPO.get(p["tipo"], p["tipo"])
        p["sede"] = texto_sede(p["ciudad"], p["modalidad"])
        p["sector_texto"] = ETIQUETAS_SECTOR.get(p["sector"], "")
        p["enlace"] = p["enlace_programa"] or p["enlace_institucion"]

    inicio_url, inicio_texto = a_donde_volver()

    return render_template(
        "explorar_carrera.html",
        carrera=carrera,
        areas=areas,
        programas=programas,
        total_programas=len(todos),
        ciudades=ciudades,
        tipos=tipos,
        modalidades=modalidades,
        sectores=sectores,
        activos={
            "ciudad": ciudad, "tipo": tipo, "modalidad": modalidad,
            "sector": sector
        },
        hay_filtros=bool(ciudad or tipo or modalidad or sector),
        volver_url=url_for("explorar.lista"),
        volver_texto="Volver a explorar",
        inicio_url=inicio_url,
        inicio_texto=inicio_texto
    )