from flask import Flask, jsonify, request, make_response
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
                    }
                ),
                400,
            )

        @app.after_request
        def after_request_func(response):
            origin = request.headers.get("Origin")
            if request.method == "OPTIONS":
                response = make_response()
                response.headers.add("Access-Control-Allow-Credentials", "true")
                response.headers.add("Access-Control-Allow-Headers", "Content-Type")
                response.headers.add("Access-Control-Allow-Headers", "x-csrf-token")
                response.headers.add("Access-Control-Allow-Headers", "Accept")
                response.headers.add("Access-Control-Allow-Headers", "X-Access-Tokens")
                response.headers.add(
                    "Access-Control-Allow-Methods",
                    "GET, POST, OPTIONS, PUT, PATCH, DELETE",
                )
                if origin:
                    response.headers.add("Access-Control-Allow-Origin", origin)
            else:
                response.headers.add("Access-Control-Allow-Credentials", "true")
                if origin:
                    response.headers.add("Access-Control-Allow-Origin", origin)
            return response

    return app


if __name__ == "__main__":
    app = crear_app()
    app.run(debug=True, host="0.0.0.0")
