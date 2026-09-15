from flask import Blueprint, render_template, request, redirect, url_for, session
from database import obtener_conexion

pruebas = Blueprint("pruebas", __name__)


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

        # Buscar la prueba
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

        # Buscar todas las preguntas de la prueba
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

        # Número de pregunta actual
        numero = request.args.get("pregunta", 1, type=int)

        # Evitar números inválidos
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

            # Guardamos temporalmente la respuesta en la sesión
            respuestas = session.get("respuestas_prueba", {})

            respuestas[str(pregunta_actual["id_pregunta"])] = int(id_opcion)

            session["respuestas_prueba"] = respuestas

            # =========================================
            # PASAR A LA SIGUIENTE PREGUNTA
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
            # TERMINÓ TODAS LAS PREGUNTAS
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
            total=len(preguntas)
        )

    finally:
        cursor.close()
        conexion.close()


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

        # Buscar qué nivel acaba de terminar
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
        # SI NO ES EL ÚLTIMO NIVEL
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
        # SI TERMINÓ EL NIVEL 5
        # =========================================

        respuestas = session.get("respuestas_prueba", {})

        return render_template(
            "prueba_finalizada.html",
            respuestas=respuestas,
            id_prueba=id_prueba,
            prueba=prueba
        )

    finally:
        cursor.close()
        conexion.close()