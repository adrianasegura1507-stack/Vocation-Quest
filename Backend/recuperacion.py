import secrets
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from database import obtener_conexion


# =========================================
# GENERAR CODIGO DE RECUPERACION
# =========================================

def generar_codigo_recuperacion():
    """
    Genera un codigo aleatorio de seis digitos
    y devuelve el codigo junto con su hash.
    """

    codigo = str(secrets.randbelow(900000) + 100000)

    codigo_hash = generate_password_hash(codigo)

    return codigo, codigo_hash

# =========================================
# CALCULAR VENCIMIENTO DEL CODIGO
# =========================================

def calcular_vencimiento_codigo():
    """
    Calcula la fecha y hora en que vence el codigo.
    """
    return datetime.now() + timedelta(minutes=10)

# =========================================
# GUARDAR CODIGO Y FECHA DE VENCIMIENTO
# =========================================

def guardar_codigo_recuperacion(id_usuario, codigo_hash):
    """
    Guarda el codigo cifrado y su fecha de vencimiento
    en la base de datos.
    """

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        expira_en = calcular_vencimiento_codigo()

        cursor.execute(
            """
            INSERT INTO recuperacion_contrasena
            (id_usuario, codigo_hash, expira_en)
            VALUES (%s, %s, %s)
            """,
            (id_usuario, codigo_hash, expira_en)
        )

        conexion.commit()

        return cursor.lastrowid

    except Exception as error:
        if conexion:
            conexion.rollback()

        print(f"Error al guardar el codigo: {error}")
        return None

    finally:
        if cursor:
            cursor.close()

        if conexion:
            conexion.close()

# =========================================
# REGISTRAR INTENTO FALLIDO
# =========================================

def registrar_intento_fallido(id_recuperacion):
    """
    Aumenta en uno el contador de intentos fallidos.
    """

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE recuperacion_contrasena
            SET intentos = intentos + 1
            WHERE id_recuperacion = %s
            """,
            (id_recuperacion,)
        )

        conexion.commit()

        return cursor.rowcount > 0

    except Exception as error:
        if conexion:
            conexion.rollback()

        print(f"Error al registrar el intento: {error}")
        return False

    finally:
        if cursor:
            cursor.close()

        if conexion:
            conexion.close()