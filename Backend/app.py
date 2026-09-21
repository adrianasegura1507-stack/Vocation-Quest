from flask import Flask, render_template
from routes.auth import auth
from routes.pruebas import pruebas

app = Flask(__name__)

app.secret_key = "vocation_quest_clave_secreta"

app.register_blueprint(auth)
app.register_blueprint(pruebas)


@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/inicio-estudiante")
def inicio_estudiante():
    return render_template("inicio_estudiante.html")

@app.route("/instrucciones-prueba")
def instrucciones_prueba():
    return render_template("instrucciones_prueba.html")

if __name__ == "__main__":
    app.run(debug=True)