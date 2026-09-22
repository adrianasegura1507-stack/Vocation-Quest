from flask import Flask, render_template, session, redirect, url_for
from routes.auth import auth
from routes.pruebas import pruebas
from database import obtener_conexion

app = Flask(__name__)

app.secret_key = "vocation_quest_clave_secreta"

app.register_blueprint(auth)
app.register_blueprint(pruebas)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/inicio-estudiante")
def inicio_estudiante():

    # Verificar que el estudiante haya iniciado sesión
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    id_usuario = session["id_usuario"]

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        # ---------------------------------------------------------
        # 1. Buscar el estudiante relacionado con el usuario
        # ---------------------------------------------------------
        cursor.execute(
            """
            SELECT id_estudiante
            FROM estudiantes
            WHERE id_usuario = %s
            """,
            (id_usuario,)
        )

        estudiante = cursor.fetchone()

        if not estudiante:
            return render_template(
                "inicio_estudiante.html",
                progreso_general=0,
                preguntas_respondidas=0,
                preguntas_totales=0,
                niveles={}
            )

        id_estudiante = estudiante["id_estudiante"]

        # ---------------------------------------------------------
        # 2. Obtener los 5 niveles/pruebas
        # ---------------------------------------------------------
        cursor.execute(
            """
            SELECT id_prueba, nombre, numero_nivel
            FROM pruebas
            WHERE estado = 1
            ORDER BY numero_nivel
            """
        )

        pruebas = cursor.fetchall()

        niveles = {}

        preguntas_respondidas_total = 0
        preguntas_totales_total = 0

        # ---------------------------------------------------------
        # 3. Revisar el progreso de cada nivel
        # ---------------------------------------------------------
        for prueba in pruebas:

            id_prueba = prueba["id_prueba"]
            numero_nivel = prueba["numero_nivel"]

            # Cantidad total de preguntas del nivel
            cursor.execute(
                """
                SELECT COUNT(*) AS total
                FROM preguntas
                WHERE id_prueba = %s
                AND estado = 1
                """,
                (id_prueba,)
            )

            resultado_total = cursor.fetchone()

            total_preguntas = resultado_total["total"] or 0

            # -----------------------------------------------------
            # Buscar el último intento del estudiante
            # -----------------------------------------------------
            cursor.execute(
                """
                SELECT id_intento, completado
                FROM intentos_prueba
                WHERE id_estudiante = %s
                AND id_prueba = %s
                ORDER BY id_intento DESC
                LIMIT 1
                """,
                (id_estudiante, id_prueba)
            )

            intento = cursor.fetchone()

            respondidas = 0
            completado = False

            if intento:

                id_intento = intento["id_intento"]
                completado = bool(intento["completado"])

                # -------------------------------------------------
                # Contar las preguntas respondidas
                # -------------------------------------------------
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
                    (id_intento, id_prueba)
                )

                resultado_respondidas = cursor.fetchone()

                respondidas = resultado_respondidas["respondidas"] or 0

            # -----------------------------------------------------
            # Calcular porcentaje del nivel
            # -----------------------------------------------------
            if total_preguntas > 0:
                porcentaje = round(
                    (respondidas / total_preguntas) * 100
                )
            else:
                porcentaje = 0

            # Si terminó el nivel, aseguramos 100%
            if completado:
                porcentaje = 100

            # Estado del nivel
            if completado:
                estado = "completado"
            elif respondidas > 0:
                estado = "progreso"
            else:
                estado = "disponible"

            niveles[numero_nivel] = {
                "id_prueba": id_prueba,
                "nombre": prueba["nombre"],
                "respondidas": respondidas,
                "total": total_preguntas,
                "porcentaje": porcentaje,
                "completado": completado,
                "estado": estado
            }

            # Acumular para el progreso general
            preguntas_respondidas_total += respondidas
            preguntas_totales_total += total_preguntas

        # ---------------------------------------------------------
        # 4. Calcular progreso general
        # ---------------------------------------------------------
        if preguntas_totales_total > 0:
            progreso_general = round(
                (preguntas_respondidas_total / preguntas_totales_total) * 100
            )
        else:
            progreso_general = 0

        return render_template(
            "inicio_estudiante.html",
            progreso_general=progreso_general,
            preguntas_respondidas=preguntas_respondidas_total,
            preguntas_totales=preguntas_totales_total,
            niveles=niveles
        )

    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    app.run(debug=True)