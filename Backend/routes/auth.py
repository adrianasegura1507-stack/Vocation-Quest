import re
from datetime import date, datetime, timedelta

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash
)
from werkzeug.security import generate_password_hash, check_password_hash
from database import obtener_conexion
from correo import (
    validar_dominio_correo,
    enviar_correo_bienvenida,
    enviar_codigo_recuperacion
)

from recuperacion import (
    generar_codigo_recuperacion,
    guardar_codigo_recuperacion,
    registrar_intento_fallido
)

auth = Blueprint("auth", __name__)


# =========================================
# REGLAS DEL REGISTRO
# =========================================
# Si el stakeholder define otra edad mínima o máxima,
# solo hay que cambiar estos dos números.

EDAD_MINIMA = 13
EDAD_MAXIMA = 100

PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+$")
PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# =========================================
# FECHAS Y EDAD
# =========================================

def restar_anios(fecha, anios):
    """
    Devuelve la misma fecha, pero "anios" años antes.
    Si la fecha es 29 de febrero y ese año no es bisiesto,
    usa el 28 de febrero.
    """
    try:
        return fecha.replace(year=fecha.year - anios)
    except ValueError:
        return fecha.replace(year=fecha.year - anios, day=28)


def calcular_edad(fecha_nacimiento, hoy=None):
    """
    Calcula cuántos años cumplidos tiene una persona.
    """
    hoy = hoy or date.today()

    edad = hoy.year - fecha_nacimiento.year

    # Si todavía no ha cumplido años este año, se resta uno
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1

    return edad


def limites_fecha_nacimiento(hoy=None):
    """
    Devuelve (fecha_minima, fecha_maxima) que se pueden elegir
    en el calendario, según EDAD_MINIMA y EDAD_MAXIMA.
    """
    hoy = hoy or date.today()

    fecha_max = restar_anios(hoy, EDAD_MINIMA)
    fecha_min = restar_anios(hoy, EDAD_MAXIMA + 1) + timedelta(days=1)

    return fecha_min, fecha_max


# =========================================
# VALIDACIONES REUTILIZABLES
# (las usan el registro y el perfil)
# Cada una devuelve un mensaje de error, o None si todo está bien.
# =========================================

def validar_nombre(nombre):
    if len(nombre) < 2 or len(nombre) > 100 \
            or not PATRON_NOMBRE.match(nombre):
        return (
            "El nombre debe tener entre 2 y 100 caracteres, "
            "solo letras y espacios."
        )
    return None


def validar_correo(correo):
    if len(correo) > 150 or not PATRON_CORREO.match(correo):
        return (
            "Escribe un correo electrónico válido "
            "(por ejemplo, nombre@correo.com)."
        )
    return None


def validar_contrasena(contrasena):
    if len(contrasena) < 8 or len(contrasena) > 255:
        return "La contraseña debe tener mínimo 8 caracteres."
    return None


def validar_fecha_nacimiento(texto):
    """
    Revisa la fecha que llegó del calendario (formato AAAA-MM-DD).
    Devuelve (fecha, edad, error). Si hay error, fecha y edad son None.
    """
    try:
        fecha = datetime.strptime(texto, "%Y-%m-%d").date()
    except ValueError:
        return None, None, "Elige tu fecha de nacimiento en el calendario."

    if fecha > date.today():
        return None, None, "La fecha de nacimiento no puede ser futura."

    edad = calcular_edad(fecha)

    if edad < EDAD_MINIMA or edad > EDAD_MAXIMA:
        return None, None, (
            f"Debes tener entre {EDAD_MINIMA} y {EDAD_MAXIMA} años."
        )

    return fecha, edad, None


# =========================================
# REGISTRO
# =========================================

def mostrar_registro(error=None, datos=None):
    """
    Muestra el formulario de registro. Si hubo un error,
    lo muestra arriba y conserva lo que la persona ya escribió.
    """
    fecha_min, fecha_max = limites_fecha_nacimiento()

    return render_template(
        "registro.html",
        error=error,
        datos=datos or {},
        fecha_min=fecha_min.isoformat(),
        fecha_max=fecha_max.isoformat(),
        edad_minima=EDAD_MINIMA,
        edad_maxima=EDAD_MAXIMA
    )


@auth.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip()
        contrasena = request.form.get("contrasena", "")
        fecha_texto = request.form.get("fecha_nacimiento", "").strip()

        # Lo que escribió, para volver a mostrarlo si hay un error
        # (la contraseña nunca se vuelve a mostrar)
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
            return mostrar_registro(error, datos)

        # Comprobar que el dominio del correo exista
        error = validar_dominio_correo(correo)

        if error:
            return mostrar_registro(error, datos)

        fecha_nacimiento, edad, error = validar_fecha_nacimiento(fecha_texto)

        if error:
            return mostrar_registro(error, datos)

        # -----------------------------------------
        # Guardar en la base de datos
        # -----------------------------------------

        # Encriptar la contraseña
        contrasena_segura = generate_password_hash(contrasena)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:

            # Revisar que el correo no esté ya registrado
            cursor.execute(
                "SELECT id_usuario FROM usuarios WHERE correo = %s",
                (correo,)
            )

            if cursor.fetchone() is not None:
                return mostrar_registro(
                    "Ese correo ya tiene una cuenta. "
                    "Inicia sesión o usa otro correo.",
                    datos
                )

            # Crear usuario
            sql_usuario = """
                INSERT INTO usuarios
                (nombre, correo, contrasena, rol)
                VALUES (%s, %s, %s, 'estudiante')
            """

            cursor.execute(
                sql_usuario,
                (nombre, correo, contrasena_segura)
            )

            # Obtener el ID del usuario recién creado
            id_usuario = cursor.lastrowid

            # Crear estudiante (la edad se calcula con la fecha)
            sql_estudiante = """
                INSERT INTO estudiantes
                (id_usuario, edad, fecha_nacimiento)
                VALUES (%s, %s, %s)
            """

            cursor.execute(
                sql_estudiante,
                (id_usuario, edad, fecha_nacimiento)
            )

            conexion.commit()
            # Enviar correo de bienvenida después de crear la cuenta
            enviar_correo_bienvenida(nombre, correo)

            # Iniciar sesión automáticamente después del registro
            session["id_usuario"] = id_usuario
            session["nombre"] = nombre
            session["rol"] = "estudiante"

            # Enviar al estudiante a su página personal
            return redirect(url_for("inicio_estudiante"))

        except Exception as error:
            conexion.rollback()
            print(f"Error en el registro: {error}")
            return mostrar_registro(
                "No pudimos crear tu cuenta. Inténtalo de nuevo.",
                datos
            )

        finally:
            cursor.close()
            conexion.close()

    return mostrar_registro()


# =========================================
# INICIO DE SESIÓN
# =========================================

def mostrar_login(error=None, correo=""):
    """
    Muestra el formulario de inicio de sesión. Si hubo un error,
    lo muestra arriba y conserva el correo que ya escribió
    (la contraseña nunca se vuelve a mostrar).
    """
    return render_template("login.html", error=error, correo=correo)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        correo = request.form.get("correo", "").strip()
        contrasena = request.form.get("contrasena", "")

        if not correo or not contrasena:
            return mostrar_login(
                "Escribe tu correo y tu contraseña.",
                correo
            )

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:

            sql = """
                SELECT id_usuario, nombre, correo, contrasena, rol, estado
                FROM usuarios
                WHERE correo = %s
            """

            cursor.execute(sql, (correo,))

            usuario = cursor.fetchone()

            # Un solo mensaje para correo o contraseña incorrectos:
            # así nadie puede averiguar qué correos tienen cuenta.
            if usuario is None or not check_password_hash(
                usuario["contrasena"],
                contrasena
            ):
                return mostrar_login(
                    "Correo o contraseña incorrectos.",
                    correo
                )

            # La contraseña es correcta, pero la cuenta fue desactivada
            if not usuario["estado"]:
                return mostrar_login(
                    "Tu cuenta está desactivada. "
                    "Habla con tu orientador o con un administrador.",
                    correo
                )

            session["id_usuario"] = usuario["id_usuario"]
            session["nombre"] = usuario["nombre"]
            session["rol"] = usuario["rol"]

            # Cada rol va a su página
            if usuario["rol"] == "administrador":
                return redirect(url_for("admin.panel"))

            return redirect(url_for("inicio_estudiante"))

        except Exception as error:
            print(f"Error al iniciar sesión: {error}")
            return mostrar_login(
                "No pudimos iniciar sesión. Inténtalo de nuevo.",
                correo
            )

        finally:

            cursor.close()
            conexion.close()

    return mostrar_login()


@auth.route("/logout")
def logout():
    """
    Cierra la sesión del usuario y vuelve a la página principal.
    """
    session.clear()
    return redirect(url_for("inicio"))

# =========================================
# SOLICITAR RECUPERACION DE CONTRASENA
# =========================================

@auth.route("/recuperar-contrasena", methods=["GET", "POST"])
def recuperar_contrasena():

    if request.method == "POST":

        correo = request.form.get("correo", "").strip()

        mensaje = (
            "Si el correo pertenece a una cuenta activa, "
            "recibirás instrucciones para recuperar tu contraseña."
        )

        if not correo or validar_correo(correo):
            flash(mensaje)
            return redirect(url_for("auth.recuperar_contrasena"))

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT id_usuario
                FROM usuarios
                WHERE correo = %s
                AND estado = 1
                AND rol = 'estudiante'
                """,
                (correo,)
            )

            usuario = cursor.fetchone()

            if usuario:
                codigo, codigo_hash = generar_codigo_recuperacion()

                cursor.execute(
                    """
                    UPDATE recuperacion_contrasena
                    SET usado = 1
                    WHERE id_usuario = %s
                    AND usado = 0
                    """,
                    (usuario["id_usuario"],)
                )

                conexion.commit()

                id_recuperacion = guardar_codigo_recuperacion(
                    usuario["id_usuario"],
                    codigo_hash
                )

                if id_recuperacion:
                    enviado = enviar_codigo_recuperacion(
                        correo,
                        codigo
                    )

                    if not enviado:
                        cursor.execute(
                            """
                            UPDATE recuperacion_contrasena
                            SET usado = 1
                            WHERE id_recuperacion = %s
                            """,
                            (id_recuperacion,)
                        )
                        conexion.commit()

            flash(mensaje)

        except Exception as error:
            if conexion:
                conexion.rollback()

            print(f"Error al solicitar recuperacion: {error}")
            flash(mensaje)

        finally:
            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

        return redirect(url_for("auth.verificar_codigo"))

    return render_template("recuperar_contrasena.html")

# =========================================
# VERIFICAR CODIGO DE RECUPERACION
# =========================================

@auth.route("/verificar-codigo", methods=["GET", "POST"])
def verificar_codigo():

    if request.method == "POST":
        correo = request.form.get("correo", "").strip()
        codigo = request.form.get("codigo", "").strip()

        if not re.fullmatch(r"\d{6}", codigo):
            flash("El código no es válido o ha vencido.")
            return redirect(url_for("auth.verificar_codigo"))

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT r.id_recuperacion, r.codigo_hash, r.id_usuario
                FROM recuperacion_contrasena r
                INNER JOIN usuarios u
                    ON r.id_usuario = u.id_usuario
                WHERE u.correo = %s
                AND u.estado = 1
                AND u.rol = 'estudiante'
                AND r.usado = 0
                AND r.expira_en > NOW()
                AND r.intentos < 5
                ORDER BY r.creado_en DESC
                LIMIT 1
                """,
                (correo,)
            )

            recuperacion = cursor.fetchone()

            if recuperacion is None or not check_password_hash(
                recuperacion["codigo_hash"], codigo
            ):
                if recuperacion:
                    registrar_intento_fallido(
                        recuperacion["id_recuperacion"]
                    )

                flash("El código no es válido o ha vencido.")
                return redirect(url_for("auth.verificar_codigo"))

            session["id_recuperacion"] = recuperacion["id_recuperacion"]

            flash("Código verificado correctamente.")
            return redirect(url_for("auth.restablecer_contrasena"))

        except Exception as error:
            print(f"Error al verificar el código: {error}")
            flash("No fue posible verificar el código.")

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    return render_template("verificar_codigo.html")


# =========================================
# RESTABLECER CONTRASEÑA
# =========================================

@auth.route("/restablecer-contrasena", methods=["GET", "POST"])
def restablecer_contrasena():

    id_recuperacion = session.get("id_recuperacion")

    if not id_recuperacion:
        flash("Primero debes verificar tu código.")
        return redirect(url_for("auth.recuperar_contrasena"))

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id_usuario
            FROM recuperacion_contrasena
            WHERE id_recuperacion = %s
            AND usado = 0
            AND expira_en > NOW()
            AND intentos < 5
            """,
            (id_recuperacion,)
        )

        recuperacion = cursor.fetchone()

        if recuperacion is None:
            session.pop("id_recuperacion", None)
            flash("El código ha vencido o ya fue utilizado.")
            return redirect(url_for("auth.recuperar_contrasena"))

        if request.method == "POST":
            contrasena = request.form.get("contrasena", "")
            confirmar = request.form.get("confirmar", "")

            error = validar_contrasena(contrasena)

            if error:
                flash(error)
            elif contrasena != confirmar:
                flash("Las contraseñas no coinciden.")
            else:
                contrasena_segura = generate_password_hash(contrasena)

                cursor.execute(
                    """
                    UPDATE usuarios
                    SET contrasena = %s
                    WHERE id_usuario = %s
                    """,
                    (contrasena_segura, recuperacion["id_usuario"])
                )

                cursor.execute(
                    """
                    UPDATE recuperacion_contrasena
                    SET usado = 1
                    WHERE id_recuperacion = %s
                    """,
                    (id_recuperacion,)
                )

                conexion.commit()

                session.pop("id_recuperacion", None)

                flash("Tu contraseña fue actualizada correctamente.")
                return redirect(url_for("auth.login"))

    except Exception as error:
        if conexion:
            conexion.rollback()

        print(f"Error al restablecer la contraseña: {error}")
        flash("No fue posible actualizar la contraseña.")

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

    return render_template("restablecer_contrasena.html")

# =========================================
# REVISAR QUE LA CUENTA SIGA ACTIVA
# =========================================

@auth.before_app_request
def revisar_cuenta_activa():
    """
    Antes de mostrar cualquier página, revisa que la cuenta de quien
    tiene la sesión iniciada siga existiendo y esté activa. Si un
    administrador la desactivó o la eliminó, se cierra la sesión.
    """
    if request.endpoint in (None, "static"):
        return None

    id_usuario = session.get("id_usuario")

    if id_usuario is None:
        return None

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT estado FROM usuarios WHERE id_usuario = %s",
            (id_usuario,)
        )

        fila = cursor.fetchone()

    finally:
        cursor.close()
        conexion.close()

    if fila is None:
        session.clear()
        return redirect(url_for("auth.login"))

    if not fila["estado"]:
        session.clear()
        flash(
            "Tu cuenta está desactivada. "
            "Habla con tu orientador o con un administrador.",
            "error"
        )
        return redirect(url_for("auth.login"))

    return None