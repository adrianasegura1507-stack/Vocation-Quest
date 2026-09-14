from flask import Flask, render_template
from routes.auth import auth

app = Flask(__name__)

app.secret_key = "vocation_quest_clave_secreta"

app.register_blueprint(auth)


@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/inicio-estudiante")
def inicio_estudiante():
    return render_template("inicio_estudiante.html")


if __name__ == "__main__":
    app.run(debug=True)