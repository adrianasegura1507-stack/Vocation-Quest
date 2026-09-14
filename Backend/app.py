from flask import Flask
from routes.auth import auth
from routes.pruebas import pruebas

app = Flask(__name__)

app.secret_key = "vocation_quest_clave_secreta"

app.register_blueprint(auth)
app.register_blueprint(pruebas)


@app.route("/")
def inicio():
    return "Vocation Quest funcionando"


if __name__ == "__main__":
    app.run(debug=True)