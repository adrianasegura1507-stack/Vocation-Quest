from flask import Blueprint, render_template, request, redirect, url_for, session
from database import obtener_conexion

pruebas = Blueprint("pruebas", __name__)


# =========================================
# BUSCAR ESTUDIANTE
# =========================================

def obtener_estudiante(cursor, id_usuario):

    cursor.execute(
        """
        SELECT id_estudiante
        FROM estudiantes
        WHERE id_usuario = %s
        """,
        (id_usuario,)
    )

    estudiante = cursor.fetchone()

    if estudiante is None:
        return None

    return estudiante["id_estudiante"]


# =========================================
# OBTENER / CREAR INTENTO
# =========================================

def obtener_intento(cursor, id_usuario, id_prueba):

    id_estudiante = obtener_estudiante(
        cursor,
        id_usuario
    )

    if id_estudiante is None:
        return None

    # Buscar intento que esté todavía en progreso
    cursor.execute(
        """
        SELECT id_intento
        FROM intentos_prueba
        WHERE id_estudiante = %s
        AND id_prueba = %s
        AND completado = 0
        ORDER BY id_intento DESC
        LIMIT 1
        """,
        (
            id_estudiante,
            id_prueba
        )
    )

    intento = cursor.fetchone()

    # Si ya existe uno en progreso, reutilizarlo
    if intento:
        return intento["id_intento"]

    # Si no existe, crear uno nuevo
    cursor.execute(
        """
        INSERT INTO intentos_prueba
        (id_estudiante, id_prueba, completado)
        VALUES (%s, %s, 0)
        """,
        (
            id_estudiante,
            id_prueba
        )
    )

    return cursor.lastrowid


# =========================================
# VERIFICAR SI EL NIVEL ESTÁ DESBLOQUEADO
# =========================================

def nivel_desbloqueado(cursor, id_estudiante, id_prueba):

    # Buscar número del nivel actual
    cursor.execute(
        """
        SELECT numero_nivel
        FROM pruebas
        WHERE id_prueba = %s
        AND estado = 1
        """,
        (id_prueba,)
    )

    prueba = cursor.fetchone()

    if prueba is None:
        return False

    numero_nivel = prueba["numero_nivel"]

    # El nivel 1 siempre está disponible
    if numero_nivel == 1:
        return True

    # Buscar si el nivel anterior está terminado
    cursor.execute(
        """
        SELECT ip.id_intento
        FROM intentos_prueba ip
        INNER JOIN pruebas p
            ON p.id_prueba = ip.id_prueba
        WHERE ip.id_estudiante = %s
        AND p.numero_nivel = %s
        AND ip.completado = 1
        LIMIT 1
        """,
        (
            id_estudiante,
            numero_nivel - 1
        )
    )

    anterior = cursor.fetchone()

    return anterior is not None


# =========================================
# PRESENTACIÓN DE LA PRUEBA
# =========================================

@pruebas.route("/prueba/<int:id_prueba>/inicio")
def inicio_prueba(id_prueba):

    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:

        # =========================================
        # BUSCAR PRUEBA
        # =========================================

        cursor.execute(
            """
            SELECT id_prueba, nombre, descripcion, numero_nivel
            FROM pruebas
            WHERE id_prueba = %s
            AND estado = 1
            """,
            (id_prueba,)
        )

        prueba = cursor.fetchone()

        if prueba is None:
            return "Prueba no encontrada"

        # =========================================
        # BUSCAR ESTUDIANTE
        # =========================================

        id_estudiante = obtener_estudiante(
            cursor,
            session["id_usuario"]
        )

        if id_estudiante is None:
            return "No se encontró el estudiante relacionado con este usuario"

        # =========================================
        # VERIFICAR SI EL NIVEL ESTÁ DESBLOQUEADO
        # =========================================

        if not nivel_desbloqueado(
            cursor,
            id_estudiante,
            id_prueba
        ):
            return redirect(
                url_for("inicio_estudiante")
            )

        # =========================================
        # VERIFICAR SI YA ESTÁ COMPLETADO
        # =========================================

        cursor.execute(
            """
            SELECT id_intento, completado
            FROM intentos_prueba
            WHERE id_estudiante = %s
            AND id_prueba = %s
            ORDER BY id_intento DESC
            LIMIT 1
            """,
            (
                id_estudiante,
                id_prueba
            )
        )

        ultimo_intento = cursor.fetchone()

        if ultimo_intento and ultimo_intento["completado"]:
            return redirect(
                url_for("inicio_estudiante")
            )

        # =========================================
        # OBTENER / CREAR INTENTO
        # =========================================

        id_intento = obtener_intento(
            cursor,
            session["id_usuario"],
            id_prueba
        )

        conexion.commit()

        # =========================================
        # MOSTRAR RESULTADOS SI TERMINÓ EL NIVEL 5
        # =========================================

        if prueba["numero_nivel"] == 5:

            # Buscar los puntos obtenidos por cada área
            cursor.execute(
                """
                SELECT
                    a.id_area,
                    a.nombre,
                    COALESCE(SUM(oa.puntos), 0) AS puntos
                FROM areas a
                LEFT JOIN opcion_area oa
                    ON oa.id_area = a.id_area
                LEFT JOIN respuestas_usuario ru
                    ON ru.id_opcion = oa.id_opcion
                LEFT JOIN intentos_prueba ip
                    ON ip.id_intento = ru.id_intento
                    AND ip.id_estudiante = %s
                    AND ip.completado = 1
                    AND ip.id_intento IN (
                        SELECT MAX(id_intento)
                        FROM intentos_prueba
                        WHERE id_estudiante = %s
                        AND completado = 1
                        GROUP BY id_prueba
                    )
                GROUP BY a.id_area, a.nombre
                ORDER BY a.id_area
                """,
                (
                    id_estudiante,
                    id_estudiante
                )
            )

            resultados = cursor.fetchall()

            return render_template(
                "prueba_finalizada.html",
                prueba=prueba,
                resultados=resultados,
                resultado_final=True
            )

        # =========================================
        # SI NO ES EL NIVEL 5
        # =========================================

        return render_template(
            "prueba_finalizada.html",
            prueba=prueba,
            resultado_final=False
        )

    finally:
        cursor.close()
        conexion.close()


# =========================================
# REALIZAR LA PRUEBA
# =========================================

@pruebas.route("/prueba/<int:id_prueba>", methods=["GET", "POST"])
def realizar_prueba(id_prueba):

    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:

        # =========================================
        # BUSCAR PRUEBA
        # =========================================

        cursor.execute(
            """
            SELECT id_prueba, nombre, descripcion, numero_nivel
            FROM pruebas
            WHERE id_prueba = %s
            AND estado = 1
            """,
            (id_prueba,)
        )

        prueba = cursor.fetchone()

        if prueba is None:
            return "Prueba no encontrada"

        # =========================================
        # BUSCAR ESTUDIANTE
        # =========================================

        id_estudiante = obtener_estudiante(
            cursor,
            session["id_usuario"]
        )

        if id_estudiante is None:
            return "No se encontró el estudiante relacionado con este usuario"

        # =========================================
        # VERIFICAR NIVEL DESBLOQUEADO
        # =========================================

        if not nivel_desbloqueado(
            cursor,
            id_estudiante,
            id_prueba
        ):
            return redirect(
                url_for("inicio_estudiante")
            )

        # =========================================
        # VERIFICAR SI YA ESTÁ COMPLETADO
        # =========================================

        cursor.execute(
            """
            SELECT id_intento, completado
            FROM intentos_prueba
            WHERE id_estudiante = %s
            AND id_prueba = %s
            ORDER BY id_intento DESC
            LIMIT 1
            """,
            (
                id_estudiante,
                id_prueba
            )
        )

        ultimo_intento = cursor.fetchone()

        if ultimo_intento and ultimo_intento["completado"]:
            return redirect(
                url_for("inicio_estudiante")
            )

        # =========================================
        # OBTENER / CREAR INTENTO
        # =========================================

        id_intento = obtener_intento(
            cursor,
            session["id_usuario"],
            id_prueba
        )

        conexion.commit()

        if id_intento is None:
            return "No se pudo crear el intento"

        session["id_intento"] = id_intento

        # =========================================
        # BUSCAR PREGUNTAS
        # =========================================

        cursor.execute(
            """
            SELECT id_pregunta, pregunta, orden
            FROM preguntas
            WHERE id_prueba = %s
            AND estado = 1
            ORDER BY orden
            """,
            (id_prueba,)
        )

        preguntas = cursor.fetchall()

        if not preguntas:
            return "Esta prueba no tiene preguntas"

        # =========================================
        # BUSCAR RESPUESTAS YA GUARDADAS
        # =========================================

        cursor.execute(
            """
            SELECT id_pregunta, id_opcion
            FROM respuestas_usuario
            WHERE id_intento = %s
            """,
            (id_intento,)
        )

        respuestas_guardadas = cursor.fetchall()

        respuestas = {}

        for respuesta in respuestas_guardadas:

            respuestas[
                respuesta["id_pregunta"]
            ] = respuesta["id_opcion"]

        # =========================================
        # DETERMINAR PREGUNTA
        # =========================================

        numero = request.args.get(
            "pregunta",
            type=int
        )

        # Si no se indicó una pregunta,
        # buscar la primera pendiente
        if numero is None:

            numero = 1

            for i, pregunta in enumerate(
                preguntas,
                start=1
            ):

                if pregunta["id_pregunta"] not in respuestas:

                    numero = i
                    break

            else:

                # Todas están respondidas
                return redirect(
                    url_for(
                        "pruebas.finalizar_prueba",
                        id_prueba=id_prueba
                    )
                )

        # Evitar números inválidos
        if numero < 1:
            numero = 1

        if numero > len(preguntas):
            numero = len(preguntas)

        pregunta_actual = preguntas[
            numero - 1
        ]

        # =========================================
        # GUARDAR RESPUESTA
        # =========================================

        if request.method == "POST":

            id_opcion = request.form.get("opcion")

            if not id_opcion:
                return "Debes seleccionar una opción"

            try:
                id_opcion = int(id_opcion)
            except ValueError:
                return "Opción inválida"

            id_pregunta = pregunta_actual[
                "id_pregunta"
            ]

            # =====================================
            # VERIFICAR SI YA EXISTE RESPUESTA
            # =====================================

            cursor.execute(
                """
                SELECT id_respuesta
                FROM respuestas_usuario
                WHERE id_intento = %s
                AND id_pregunta = %s
                """,
                (
                    id_intento,
                    id_pregunta
                )
            )

            existente = cursor.fetchone()

            # =====================================
            # ACTUALIZAR
            # =====================================

            if existente:

                cursor.execute(
                    """
                    UPDATE respuestas_usuario
                    SET id_opcion = %s
                    WHERE id_respuesta = %s
                    """,
                    (
                        id_opcion,
                        existente["id_respuesta"]
                    )
                )

            # =====================================
            # INSERTAR
            # =====================================

            else:

                cursor.execute(
                    """
                    INSERT INTO respuestas_usuario
                    (id_intento, id_pregunta, id_opcion)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        id_intento,
                        id_pregunta,
                        id_opcion
                    )
                )

            conexion.commit()

            # =========================================
            # SIGUIENTE PREGUNTA
            # =========================================

            siguiente = numero + 1

            if siguiente <= len(preguntas):

                return redirect(
                    url_for(
                        "pruebas.realizar_prueba",
                        id_prueba=id_prueba,
                        pregunta=siguiente
                    )
                )

            # =========================================
            # TERMINÓ EL NIVEL
            # =========================================

            return redirect(
                url_for(
                    "pruebas.finalizar_prueba",
                    id_prueba=id_prueba
                )
            )

        # =========================================
        # BUSCAR OPCIONES
        # =========================================

        cursor.execute(
            """
            SELECT id_opcion, texto, orden
            FROM opciones_respuesta
            WHERE id_pregunta = %s
            ORDER BY orden
            """,
            (
                pregunta_actual["id_pregunta"],
            )
        )

        opciones = cursor.fetchall()

        return render_template(
            "prueba.html",
            prueba=prueba,
            pregunta=pregunta_actual,
            opciones=opciones,
            numero=numero,
            total=len(preguntas),
            respuesta_guardada=respuestas.get(
                pregunta_actual["id_pregunta"]
            )
        )

    finally:
        cursor.close()
        conexion.close()


# =========================================
# SALIR DE LA PRUEBA
# =========================================

@pruebas.route("/prueba/<int:id_prueba>/salir")
def salir_prueba(id_prueba):

    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    # No eliminamos el intento.
    # No eliminamos las respuestas.
    # El estudiante simplemente vuelve a su página.

    return redirect(
        url_for("inicio_estudiante")
    )


# =========================================
# FINALIZAR NIVEL
# =========================================

@pruebas.route("/prueba/<int:id_prueba>/finalizar")
def finalizar_prueba(id_prueba):

    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:

        # =========================================
        # BUSCAR PRUEBA
        # =========================================

        cursor.execute(
            """
            SELECT id_prueba, nombre, numero_nivel
            FROM pruebas
            WHERE id_prueba = %s
            AND estado = 1
            """,
            (id_prueba,)
        )

        prueba = cursor.fetchone()

        if prueba is None:
            return "Prueba no encontrada"

        # =========================================
        # BUSCAR ESTUDIANTE
        # =========================================

        id_estudiante = obtener_estudiante(
            cursor,
            session["id_usuario"]
        )

        if id_estudiante is None:
            return "No se encontró el estudiante"

        # =========================================
        # BUSCAR INTENTO ACTIVO
        # =========================================

        cursor.execute(
            """
            SELECT id_intento
            FROM intentos_prueba
            WHERE id_estudiante = %s
            AND id_prueba = %s
            AND completado = 0
            ORDER BY id_intento DESC
            LIMIT 1
            """,
            (
                id_estudiante,
                id_prueba
            )
        )

        intento = cursor.fetchone()

        if intento is None:
            return redirect(
                url_for("inicio_estudiante")
            )

        id_intento = intento["id_intento"]

        # =========================================
        # CONTAR PREGUNTAS TOTALES
        # =========================================

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM preguntas
            WHERE id_prueba = %s
            AND estado = 1
            """,
            (id_prueba,)
        )

        total = cursor.fetchone()["total"]

        # =========================================
        # CONTAR RESPUESTAS
        # =========================================

        cursor.execute(
            """
            SELECT COUNT(DISTINCT ru.id_pregunta) AS respondidas
            FROM respuestas_usuario ru
            INNER JOIN preguntas p
                ON p.id_pregunta = ru.id_pregunta
            WHERE ru.id_intento = %s
            AND p.id_prueba = %s
            AND p.estado = 1
            """,
            (
                id_intento,
                id_prueba
            )
        )

        respondidas = cursor.fetchone()["respondidas"]

        # =========================================
        # NO FINALIZAR SI FALTAN PREGUNTAS
        # =========================================

        if respondidas < total:

            return redirect(
                url_for(
                    "pruebas.realizar_prueba",
                    id_prueba=id_prueba
                )
            )

        # =========================================
        # MARCAR NIVEL COMO COMPLETADO
        # =========================================

        cursor.execute(
            """
            UPDATE intentos_prueba
            SET completado = 1,
                fecha_fin = NOW()
            WHERE id_intento = %s
            """,
            (id_intento,)
        )

        conexion.commit()

        # =========================================
        # SI ES EL NIVEL 5, MOSTRAR RESULTADOS
        # =========================================

        if prueba["numero_nivel"] == 5:

            cursor.execute(
                """
                SELECT
                    a.id_area,
                    a.nombre,
                    COALESCE(SUM(oa.puntos), 0) AS puntos
                FROM areas a
                LEFT JOIN opcion_area oa
                    ON oa.id_area = a.id_area
                LEFT JOIN respuestas_usuario ru
                    ON ru.id_opcion = oa.id_opcion
                LEFT JOIN intentos_prueba ip
                    ON ip.id_intento = ru.id_intento
                    AND ip.id_estudiante = %s
                    AND ip.completado = 1
                    AND ip.id_intento IN (
                        SELECT MAX(id_intento)
                        FROM intentos_prueba
                        WHERE id_estudiante = %s
                        AND completado = 1
                        GROUP BY id_prueba
                    )
                GROUP BY a.id_area, a.nombre
                ORDER BY a.id_area
                """,
                (
                    id_estudiante,
                    id_estudiante
                )
            )

            resultados = cursor.fetchall()

            return render_template(
                "prueba_finalizada.html",
                prueba=prueba,
                resultados=resultados,
                resultado_final=True
            )

        # =========================================
        # SI NO ES EL NIVEL 5
        # =========================================

        return render_template(
            "prueba_finalizada.html",
            prueba=prueba,
            resultado_final=False
        )

    finally:

        cursor.close()
        conexion.close()