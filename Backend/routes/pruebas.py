from flask import Blueprint, render_template, request, redirect, url_for, session
from database import obtener_conexion

pruebas = Blueprint("pruebas", __name__)


# =========================================
# OBTENER / CREAR INTENTO
# =========================================

def obtener_intento(cursor, id_usuario, id_prueba):

    # Buscar el estudiante relacionado con el usuario
    sql_estudiante = """
        SELECT id_estudiante
        FROM estudiantes
        WHERE id_usuario = %s
    """

    cursor.execute(sql_estudiante, (id_usuario,))
    estudiante = cursor.fetchone()

    if estudiante is None:
        return None

    id_estudiante = estudiante["id_estudiante"]

    # Buscar si ya existe un intento para esta prueba
    sql_intento = """
        SELECT id_intento
        FROM intentos_prueba
        WHERE id_estudiante = %s
        AND id_prueba = %s
        AND completado = 0
        ORDER BY id_intento DESC
        LIMIT 1
    """

    cursor.execute(
        sql_intento,
        (id_estudiante, id_prueba)
    )

    intento = cursor.fetchone()

    # Si ya existe, lo reutilizamos
    if intento:
        return intento["id_intento"]

    # Si no existe, creamos uno nuevo
    sql_nuevo = """
        INSERT INTO intentos_prueba
        (id_estudiante, id_prueba, completado)
        VALUES (%s, %s, 0)
    """

    cursor.execute(
        sql_nuevo,
        (id_estudiante, id_prueba)
    )

    return cursor.lastrowid


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

        sql_prueba = """
            SELECT id_prueba, nombre, descripcion, numero_nivel
            FROM pruebas
            WHERE id_prueba = %s
            AND estado = 1
        """

        cursor.execute(sql_prueba, (id_prueba,))
        prueba = cursor.fetchone()

        if prueba is None:
            return "Prueba no encontrada"

        # Crear o recuperar el intento
        id_intento = obtener_intento(
            cursor,
            session["id_usuario"],
            id_prueba
        )

        conexion.commit()

        if id_intento is None:
            return "No se encontró el estudiante relacionado con este usuario"

        # Guardamos el intento en sesión
        session["id_intento"] = id_intento

        return render_template(
            "presentacion_prueba.html",
            prueba=prueba
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

        sql_prueba = """
            SELECT id_prueba, nombre, descripcion, numero_nivel
            FROM pruebas
            WHERE id_prueba = %s
            AND estado = 1
        """

        cursor.execute(sql_prueba, (id_prueba,))
        prueba = cursor.fetchone()

        if prueba is None:
            return "Prueba no encontrada"

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
            return "No se encontró el estudiante relacionado con este usuario"

        session["id_intento"] = id_intento

        # =========================================
        # BUSCAR PREGUNTAS
        # =========================================

        sql_preguntas = """
            SELECT id_pregunta, pregunta, orden
            FROM preguntas
            WHERE id_prueba = %s
            AND estado = 1
            ORDER BY orden
        """

        cursor.execute(sql_preguntas, (id_prueba,))
        preguntas = cursor.fetchall()

        if not preguntas:
            return "Esta prueba no tiene preguntas"

        # =========================================
        # BUSCAR RESPUESTAS YA GUARDADAS
        # =========================================

        sql_respuestas = """
            SELECT id_pregunta, id_opcion
            FROM respuestas_usuario
            WHERE id_intento = %s
        """

        cursor.execute(
            sql_respuestas,
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

        # Si no se indicó pregunta, buscar la primera pendiente
        if numero is None:

            numero = 1

            for i, pregunta in enumerate(preguntas, start=1):

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

        if numero < 1:
            numero = 1

        if numero > len(preguntas):
            numero = len(preguntas)

        pregunta_actual = preguntas[numero - 1]

        # =========================================
        # GUARDAR RESPUESTA
        # =========================================

        if request.method == "POST":

            id_opcion = request.form.get("opcion")

            if not id_opcion:
                return "Debes seleccionar una opción"

            id_opcion = int(id_opcion)

            id_pregunta = pregunta_actual["id_pregunta"]

            # Verificar si ya existe respuesta
            sql_existente = """
                SELECT id_respuesta
                FROM respuestas_usuario
                WHERE id_intento = %s
                AND id_pregunta = %s
            """

            cursor.execute(
                sql_existente,
                (id_intento, id_pregunta)
            )

            existente = cursor.fetchone()

            if existente:

                # Actualizar respuesta
                sql_actualizar = """
                    UPDATE respuestas_usuario
                    SET id_opcion = %s
                    WHERE id_respuesta = %s
                """

                cursor.execute(
                    sql_actualizar,
                    (
                        id_opcion,
                        existente["id_respuesta"]
                    )
                )

            else:

                # Crear respuesta
                sql_insertar = """
                    INSERT INTO respuestas_usuario
                    (id_intento, id_pregunta, id_opcion)
                    VALUES (%s, %s, %s)
                """

                cursor.execute(
                    sql_insertar,
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
            # TERMINÓ LAS PREGUNTAS
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

        sql_opciones = """
            SELECT id_opcion, texto, orden
            FROM opciones_respuesta
            WHERE id_pregunta = %s
            ORDER BY orden
        """

        cursor.execute(
            sql_opciones,
            (pregunta_actual["id_pregunta"],)
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

    # NO borramos el intento
    # NO borramos las respuestas
    # Simplemente regresamos al perfil

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

        sql_prueba = """
            SELECT id_prueba, nombre, numero_nivel
            FROM pruebas
            WHERE id_prueba = %s
            AND estado = 1
        """

        cursor.execute(sql_prueba, (id_prueba,))
        prueba = cursor.fetchone()

        if prueba is None:
            return "Prueba no encontrada"

        # =========================================
        # OBTENER INTENTO
        # =========================================

        id_intento = obtener_intento(
            cursor,
            session["id_usuario"],
            id_prueba
        )

        if id_intento is None:
            return "No se encontró el intento"

        # =========================================
        # MARCAR COMO COMPLETADO
        # =========================================

        sql_completar = """
            UPDATE intentos_prueba
            SET completado = 1,
                fecha_fin = NOW()
            WHERE id_intento = %s
        """

        cursor.execute(
            sql_completar,
            (id_intento,)
        )

        conexion.commit()

        # =========================================
        # SIGUIENTE NIVEL
        # =========================================

        if prueba["numero_nivel"] < 5:

            siguiente_nivel = prueba["numero_nivel"] + 1

            sql_siguiente = """
                SELECT id_prueba
                FROM pruebas
                WHERE numero_nivel = %s
                AND estado = 1
                LIMIT 1
            """

            cursor.execute(
                sql_siguiente,
                (siguiente_nivel,)
            )

            siguiente_prueba = cursor.fetchone()

            if siguiente_prueba:

                return redirect(
                    url_for(
                        "pruebas.inicio_prueba",
                        id_prueba=siguiente_prueba["id_prueba"]
                    )
                )

        # =========================================
        # TERMINÓ NIVEL 5
        # =========================================

        return render_template(
            "prueba_finalizada.html",
            id_prueba=id_prueba,
            prueba=prueba
        )

    finally:
        cursor.close()
        conexion.close()