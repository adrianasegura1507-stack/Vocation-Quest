from flask import Blueprint, render_template, request
from werkzeug.security import generate_password_hash
from database import obtener_conexion

auth = Blueprint("auth", __name__)


@auth.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        nombre = request.form["nombre"]
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]
        edad = request.form["edad"]
        grado = request.form["grado"]

        # Encriptar la contraseña
        contrasena_segura = generate_password_hash(contrasena)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
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

            # Crear estudiante
            sql_estudiante = """
                INSERT INTO estudiantes
                (id_usuario, edad, grado)
                VALUES (%s, %s, %s)
            """

            cursor.execute(
                sql_estudiante,
                (id_usuario, edad, grado)
            )

            conexion.commit()

            return "Registro exitoso"

        except Exception as error:
            conexion.rollback()
            return f"Error en el registro: {error}"

        finally:
            cursor.close()
            conexion.close()

    return render_template("registro.html")