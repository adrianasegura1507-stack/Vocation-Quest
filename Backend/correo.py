
import os
import smtplib
import ssl
from email.message import EmailMessage

from email_validator import validate_email, EmailNotValidError


# =========================================
# VALIDAR DOMINIO DEL CORREO
# =========================================

def validar_dominio_correo(correo):
    try:
        validate_email(
            correo,
            check_deliverability=True
        )
        return None

    except EmailNotValidError:
        return (
            "El dominio del correo no existe o no puede "
            "recibir correos. Verifica la dirección."
        )

    except Exception as error:
        print(f"Error al validar el dominio: {error}")
        return (
            "No pudimos comprobar el dominio del correo. "
            "Inténtalo nuevamente."
        )


# =========================================
# ENVIAR CORREO DE BIENVENIDA
# =========================================

def enviar_correo_bienvenida(nombre, destinatario):

    servidor = os.environ.get("MAIL_SERVER")
    puerto = int(os.environ.get("MAIL_PORT", "587"))
    usuario = os.environ.get("MAIL_USERNAME")
    contrasena = os.environ.get("MAIL_PASSWORD")
    remitente = os.environ.get("MAIL_DEFAULT_SENDER")

    if not all([servidor, usuario, contrasena, remitente]):
        print("Correo de bienvenida no enviado: falta configurar SMTP.")
        return False

    mensaje = EmailMessage()
    mensaje["Subject"] = "¡Bienvenido a Vocation Quest!"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario

    mensaje.set_content(
        f"""
¡Hola, {nombre}!

Tu cuenta en Vocation Quest ha sido creada exitosamente.

Nos alegra que formes parte de esta aventura.
Ahora puedes iniciar sesión, explorar tus intereses
y descubrir nuevas posibilidades para tu futuro.

¡Te deseamos mucho éxito!

Equipo Vocation Quest
"""
    )

    try:
        contexto = ssl.create_default_context()

        with smtplib.SMTP(servidor, puerto, timeout=20) as conexion:
            conexion.starttls(context=contexto)
            conexion.login(usuario, contrasena)
            conexion.send_message(mensaje)

        print(f"Correo de bienvenida enviado a {destinatario}.")
        return True

    except Exception as error:
        print(f"Error al enviar correo de bienvenida: {error}")
        return False

# =========================================
# ENVIAR CODIGO DE RECUPERACION
# =========================================

def enviar_codigo_recuperacion(destinatario, codigo):

    servidor = os.environ.get("MAIL_SERVER")
    puerto = int(os.environ.get("MAIL_PORT", "587"))
    usuario = os.environ.get("MAIL_USERNAME")
    contrasena = os.environ.get("MAIL_PASSWORD")
    remitente = os.environ.get("MAIL_DEFAULT_SENDER")

    if not all([servidor, usuario, contrasena, remitente]):
        print("Codigo no enviado: falta configurar SMTP.")
        return False

    mensaje = EmailMessage()
    mensaje["Subject"] = "Recuperacion de contrasena - Vocation Quest"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario

    mensaje.set_content(
        f"""
Hola.

Recibimos una solicitud para recuperar tu contrasena
de Vocation Quest.

Tu codigo de recuperacion es:

{codigo}

Este codigo vence en 10 minutos y solo puede utilizarse una vez.

Si no solicitaste este cambio, puedes ignorar este mensaje.

Equipo Vocation Quest
"""
    )

    try:
        contexto = ssl.create_default_context()

        with smtplib.SMTP(servidor, puerto, timeout=20) as conexion:
            conexion.starttls(context=contexto)
            conexion.login(usuario, contrasena)
            conexion.send_message(mensaje)

        print(f"Codigo de recuperacion enviado a {destinatario}.")
        return True

    except Exception as error:
        print(f"Error al enviar codigo de recuperacion: {error}")
        return False