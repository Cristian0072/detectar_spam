import networkx as nx
import nltk
from nltk.tokenize import word_tokenize
import spacy

# Verificar y descargar recursos necesarios
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")
    nltk.download("punkt_tab")

# Lista de palabras de spam
lista_palabras = [
    "gratis",
    "oferta",
    "promoción",
    "gana dinero",
    "descuento",
    "limitado",
    "excepcional",
    "único",
    "compra ahora",
    "prueba gratis",
    "increíble",
    "haz clic aquí",
    "imperdible",
    "gana dinero",
    "exclusivo",
    "urgente",
    "felicitaciones",
    "mejor precio",
    "solicítalo ahora",
    "no te lo pierdas",
    "oportunidad",
    "exclusivo",
]


class Automata:
    def __init__(self):
        self.grafo_spam = self._crear_grafo()
        self.nlp = spacy.load("es_core_news_md")  # cargar modelo de lenguaje en español

    # funcion para crear el grafo
    def _crear_grafo(self):
        grafo = nx.DiGraph()
        # agregar nodos al grafo
        grafo.add_nodes_from(lista_palabras)

        # Conectar palabras relacionadas
        relaciones = [
            ("gratis", "oferta"),
            ("oferta", "descuento"),
            ("descuento", "promoción"),
            ("promoción", "compra ahora"),
            ("compra ahora", "exclusivo"),
            ("prueba gratis", "increíble"),
            ("único", "oportunidad"),
            ("urgente", "haz clic aquí"),
            ("mejor precio", "solicítalo ahora"),
            ("felicitaciones", "no te lo pierdas"),
            ("imperdible", "gana dinero"),
            ("limitado", "único"),
            ("exclusivo", "increíble"),
            ("increíble", "haz clic aquí"),
            ("haz clic aquí", "gana dinero"),
            ("gana dinero", "excepcional"),
            ("excepcional", "urgente"),
            ("urgente", "felicitaciones"),
            ("felicitaciones", "mejor precio"),
            ("mejor precio", "solicítalo ahora"),
            ("solicítalo ahora", "no te lo pierdas"),
            ("no te lo pierdas", "oportunidad"),
            ("oportunidad", "gratis"),
            ("gratis", "descuento"),
            ("descuento", "limitado"),
            ("estafa", "gratis"),
            ("no es spam", "gratis"),
            ("expira", "oferta"),
            ("confidencial", "oferta"),
            ("100 '%' gratis", "seguro"),
            ("lotería", "gratis"),
            ("premio", "gratis"),
            ("última oportunidad", "gratis"),
            ("precio especial", "gratis"),
        ]
        grafo.add_edges_from(relaciones)
        return grafo

    # funcion para validar el texto ingresado
    def validar_texto(self, texto):
        p_sentido = 10
        if not isinstance(texto, str) or not texto.strip():
            return False, "El texto ingresado no es válido"
        # se tokeniza el texto ingresado
        palabras = self.nlp(texto)

        # Verificar si hay suficientes palabras con sentido
        palabras_validas = [token for token in palabras if token.is_alpha]
        if len(palabras_validas) <= p_sentido:
            return (
                False,
                "El texto no tiene suficientes palabras para categorizarlo como válido",
            )

        # Verificar coherencia semántica
        frases_con_sujeto = any(token.dep_ == "nsubj" for token in palabras)
        if not frases_con_sujeto:
            return False, "El texto ingresado no es válido"

        return True, "El texto ingresado es válido"

    # funcion para separar las palabras del mensaje ingresado
    def buscar_lexico(self, mensaje):
        palabras = []
        palabra = ""

        for letra in mensaje:
            if palabra and letra == " ":
                palabras.append(palabra)
                palabra = ""
            else:
                palabra += letra
        if palabra:
            palabras.append(palabra)
        return palabras

    # funcion para buscar coincidencias entre las palabras del mensaje y las palabras de spam
    def buscar_semantica(self, palabras):
        coincidencias = [palabra for palabra in palabras if palabra in lista_palabras]
        return coincidencias

    # funcion para buscar si hay una estructura sintactica en el mensaje
    def buscar_sintactica(self, palabras):
        numero = 0
        valido = False
        for i in range(len(palabras) - 1):
            if self.grafo_spam.has_edge(palabras[i], palabras[i + 1]):
                numero += 1
                valido = True
        return valido, numero

    # función para detectar si el mensaje es spam o no mediante el modelo de lenguaje natural de nltk
    def detectar_spam_nltk(self, texto):
        palabras = word_tokenize(texto.lower())
        palabras_clave = set(palabras) & set(lista_palabras)
        return len(palabras_clave) > 0

    # funcion para clasificar si el mensaje es spam o no
    def es_spam(self, mensaje):
        porcentaje = 0.4  # 40%
        umbral_coincidencias = 5  # 5
        # validación de entrada
        texto = mensaje["texto"]
        es_valido, mensaje = self.validar_texto(texto)
        if not es_valido:
            return mensaje, []

        palabras = self.buscar_lexico(texto)
        coincidencias_semanticas = self.buscar_semantica(palabras)
        es_sintacticamente_spam, n_coincidencias = self.buscar_sintactica(palabras)
        spam = self.detectar_spam_nltk(texto)
        print(coincidencias_semanticas)
        if (
            len(coincidencias_semanticas) > int(len(palabras) * porcentaje)
            or (es_sintacticamente_spam and n_coincidencias > umbral_coincidencias)
            or spam
        ):
            return "El texto es SPAM", coincidencias_semanticas
        else:
            return "El texto no es SPAM", []
