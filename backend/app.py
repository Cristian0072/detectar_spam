from flask import Flask, jsonify
from werkzeug.exceptions import BadRequest


def home():
    return "¡Hola, Flask!"


def crear_app():
    # Crear la aplicación Flask y registrar los blueprints
    app = Flask(__name__, instance_relative_config=False)

    with app.app_context():
        from routes.api_automata import api_spam

        app.register_blueprint(api_spam)

        @app.errorhandler(BadRequest)
        def handle_error(e):
            return (
                jsonify(
                    {
                        "codigo": 400,
                        "msj": "El texto debe ser una cadena de caracteres",
                        "error": "Error en los datos enviados",
                    },
                ),
                400,
            )

    return app
