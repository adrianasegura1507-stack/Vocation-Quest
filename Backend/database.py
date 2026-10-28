import os
import mysql.connector


def obtener_conexion():
    """
    Abre la conexión con MySQL.
    En tu computador usa XAMPP (los valores por defecto de abajo).
    En internet, esos valores se cambian con variables de entorno,
    sin tocar el código.
    """
    config = {
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": int(os.environ.get("DB_PORT", "3306")),
        "user": os.environ.get("DB_USER", "root"),
        "password": os.environ.get("DB_PASSWORD", ""),
        "database": os.environ.get("DB_NAME", "vocation_quest2"),
    }

    # Los servicios en la nube (como Aiven) exigen conexión cifrada
    certificado = os.environ.get("DB_SSL_CA")

    if certificado:
        config["ssl_ca"] = certificado

    return mysql.connector.connect(**config)