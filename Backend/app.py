from flask import Flask, render_template, session, redirect, url_for
from routes.auth import auth
from routes.pruebas import pruebas, NIVELES_PRUEBA
from database import obtener_conexion

app = Flask(__name__)

app.secret_key = "vocation_quest_clave_secreta"

app.register_blueprint(auth)
app.register_blueprint(pruebas)


# =========================================
# ICONOS DE LOS LOGROS
# =========================================
# La tabla "logros" no tiene columna de icono, así que
# lo elegimos según el campo "tipo" del logro.

ICONOS_LOGROS = {
    "preguntas_1": "👣",
    "niveles_1": "🌟",
    "preguntas_10": "🔍",
    "niveles_3": "🧭",
    "preguntas_20": "💪",
    "niveles_5": "🏅",
}


def logro_cumplido(tipo, niveles_completados, preguntas_respondidas):
    """
    El campo "tipo" de cada logro tiene este formato:
        niveles_3    -> completar 3 niveles
        preguntas_10 -> responder 10 preguntas
    """

    if not tipo or "_" not in tipo:
        return False

    clase, cantidad = tipo.split("_", 1)

    try:
        cantidad = int(cantidad)
    except ValueError:
        return False

    if clase == "niveles":
        return niveles_completados >= cantidad

    if clase == "preguntas":
        return preguntas_respondidas >= cantidad

    return False


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
                niveles={},
                mision=None,
                aventura_completa=False,
                logros=[],
                logros_desbloqueados=0
            )

        id_estudiante = estudiante["id_estudiante"]

        # ---------------------------------------------------------
        # 2. Obtener los niveles/pruebas
        # ---------------------------------------------------------

        cursor.execute(
            """
            SELECT id_prueba, nombre, descripcion, numero_nivel
            FROM pruebas
            WHERE estado = 1
            AND numero_nivel <= %s
            ORDER BY numero_nivel
            """,
            (NIVELES_PRUEBA,)
        )

        lista_pruebas = cursor.fetchall()

        niveles = {}

        preguntas_respondidas_total = 0
        preguntas_totales_total = 0

        # ---------------------------------------------------------
        # 3. Revisar el progreso de cada nivel
        # ---------------------------------------------------------

        for prueba in lista_pruebas:

            id_prueba = prueba["id_prueba"]
            numero_nivel = prueba["numero_nivel"]

            # -----------------------------------------------------
            # Cantidad total de preguntas del nivel
            # -----------------------------------------------------

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
            # Buscar el intento más relevante del estudiante.
            # Si existe uno completado, se usa ese; si no,
            # el más reciente. (Así coincide con la regla de
            # desbloqueo de Backend/routes/pruebas.py)
            # -----------------------------------------------------

            cursor.execute(
                """
                SELECT id_intento, completado
                FROM intentos_prueba
                WHERE id_estudiante = %s
                AND id_prueba = %s
                ORDER BY completado DESC, id_intento DESC
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

            # -----------------------------------------------------
            # Estado del nivel
            # -----------------------------------------------------

            if completado:

                estado = "completado"

            else:

                # El nivel 1 siempre está disponible
                if numero_nivel == 1:

                    desbloqueado = True

                else:

                    # Revisar si el nivel anterior está completado
                    nivel_anterior = niveles.get(
                        numero_nivel - 1
                    )

                    desbloqueado = bool(
                        nivel_anterior
                        and nivel_anterior["completado"]
                    )

                if not desbloqueado:
                    estado = "bloqueado"
                elif respondidas > 0:
                    estado = "progreso"
                else:
                    estado = "disponible"

            # -----------------------------------------------------
            # Guardar información del nivel
            # -----------------------------------------------------

            niveles[numero_nivel] = {
                "id_prueba": id_prueba,
                "numero": numero_nivel,
                "nombre": prueba["nombre"],
                "descripcion": prueba["descripcion"],
                "respondidas": respondidas,
                "total": total_preguntas,
                "porcentaje": porcentaje,
                "completado": completado,
                "estado": estado
            }

            # -----------------------------------------------------
            # Acumular para el progreso general
            # -----------------------------------------------------

            preguntas_respondidas_total += respondidas
            preguntas_totales_total += total_preguntas

        # ---------------------------------------------------------
        # 4. Calcular progreso general
        # ---------------------------------------------------------

        if preguntas_totales_total > 0:

            progreso_general = round(
                (
                    preguntas_respondidas_total
                    / preguntas_totales_total
                ) * 100
            )

        else:

            progreso_general = 0

        # ---------------------------------------------------------
        # 5. Nivel 5: los resultados. No tiene preguntas.
        #    - Se desbloquea al completar los niveles 1 al 4.
        #    - Queda "completado" cuando la estudiante ya vio
        #      sus resultados (se guardan en la tabla "resultados").
        # ---------------------------------------------------------

        pruebas_completas = (
            len(niveles) == NIVELES_PRUEBA
            and all(n["completado"] for n in niveles.values())
        )

        cursor.execute(
            """
            SELECT r.id_resultado
            FROM resultados r
            INNER JOIN intentos_prueba ip
                ON ip.id_intento = r.id_intento
            WHERE ip.id_estudiante = %s
            LIMIT 1
            """,
            (id_estudiante,)
        )

        # Siempre se lee el resultado de la consulta (aunque no se use),
        # para que MySQL no se queje en la siguiente consulta
        fila_resultado = cursor.fetchone()

        resultado_visto = (
            pruebas_completas and fila_resultado is not None
        )

        if resultado_visto:
            estado_resultado = "completado"
        elif pruebas_completas:
            estado_resultado = "disponible"
        else:
            estado_resultado = "bloqueado"

        niveles[NIVELES_PRUEBA + 1] = {
            "id_prueba": None,
            "numero": NIVELES_PRUEBA + 1,
            "nombre": "Mi resultado",
            "descripcion": (
                "¡Terminaste todas las pruebas! Entra para descubrir "
                "las áreas que más se parecen a ti."
            ),
            "respondidas": 0,
            "total": 0,
            "porcentaje": 100 if resultado_visto else 0,
            "completado": resultado_visto,
            "estado": estado_resultado
        }

        # La aventura termina cuando ya vio sus resultados
        aventura_completa = resultado_visto

        # ---------------------------------------------------------
        # Misión actual: el primer nivel (del 1 al 5) que se puede
        # jugar y todavía no está completado
        # ---------------------------------------------------------

        mision = None

        for numero in sorted(niveles):

            nivel = niveles[numero]

            if nivel["estado"] in ("disponible", "progreso"):
                mision = nivel
                break

        niveles_completados = sum(
            1 for n in niveles.values() if n["completado"]
        )

        # ---------------------------------------------------------
        # 6. Logros: revisar cuáles cumple el estudiante
        #    y guardar los nuevos en estudiante_logro
        # ---------------------------------------------------------

        cursor.execute(
            """
            SELECT id_logro, nombre, descripcion, puntos, tipo
            FROM logros
            ORDER BY id_logro
            """
        )

        catalogo_logros = cursor.fetchall()

        cursor.execute(
            """
            SELECT id_logro
            FROM estudiante_logro
            WHERE id_estudiante = %s
            """,
            (id_estudiante,)
        )

        logros_ya_obtenidos = {
            fila["id_logro"] for fila in cursor.fetchall()
        }

        hay_logros_nuevos = False

        for logro in catalogo_logros:

            cumplido = logro_cumplido(
                logro["tipo"],
                niveles_completados,
                preguntas_respondidas_total
            )

            if cumplido and logro["id_logro"] not in logros_ya_obtenidos:

                cursor.execute(
                    """
                    INSERT IGNORE INTO estudiante_logro
                    (id_estudiante, id_logro)
                    VALUES (%s, %s)
                    """,
                    (id_estudiante, logro["id_logro"])
                )

                logros_ya_obtenidos.add(logro["id_logro"])
                hay_logros_nuevos = True

        if hay_logros_nuevos:
            conexion.commit()

        logros = []

        for logro in catalogo_logros:

            logros.append({
                "nombre": logro["nombre"],
                "descripcion": logro["descripcion"],
                "icono": ICONOS_LOGROS.get(logro["tipo"], "🏅"),
                "desbloqueado": logro["id_logro"] in logros_ya_obtenidos
            })

        logros_desbloqueados = sum(
            1 for l in logros if l["desbloqueado"]
        )

        # ---------------------------------------------------------
        # 7. Mostrar página del estudiante
        # ---------------------------------------------------------

        return render_template(
            "inicio_estudiante.html",
            progreso_general=progreso_general,
            preguntas_respondidas=preguntas_respondidas_total,
            preguntas_totales=preguntas_totales_total,
            niveles=niveles,
            mision=mision,
            aventura_completa=aventura_completa,
            logros=logros,
            logros_desbloqueados=logros_desbloqueados
        )

    finally:

        cursor.close()
        conexion.close()


if __name__ == "__main__":
    app.run(debug=True)