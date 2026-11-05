import secrets
from werkzeug.security import generate_password_hash


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