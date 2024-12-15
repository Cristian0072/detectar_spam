from flask import request, jsonify, Blueprint
from controlador.controlador_automata import Automata
from flask_expects_json import expects_json

api_spam = Blueprint("api_spam", __name__)


automata = Automata()

estructura_mensaje = {
    "type": "object",
    "properties": {
        "texto": {
            "type": "string",
        },
    },
    "required": ["texto"],
}


@api_spam.route("/detectar_spam", methods=["POST"])
@expects_json(estructura_mensaje)
def detectar_spam():
    data = request.json
    # Evaluación de spam
    resultado, coincidencias = automata.es_spam(data)

    return jsonify(
        {
            "msj": "OK",
            "resultado": resultado,
            "palabras_clave": coincidencias,
            "estado": 200,
        }
    )
