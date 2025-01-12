import networkx as nx
import spacy

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

    # funcion para buscar palabras en el mensaje ingresado
    def buscar_lexico(self, mensaje):
        palabras = []
        palabra = ""
        # se recorre el mensaje y se valida si es una letra o un numero
        for letra in mensaje:
            if letra.isalnum():
                palabra += letra.lower()
            else:
                if palabra:
                    palabras.append(palabra)
                    palabra = ""
        if palabra:
            palabras.append(palabra)
        return palabras

    # funcion para buscar palabras en el grafo
    def buscar_semantica(self, palabras):
        coincidencias = [palabra for palabra in palabras if palabra in lista_palabras]
        return coincidencias

    # funcion para buscar si hay una estructura sintactica en el mensaje
    def buscar_sintactica(self, palabras):
        # se recorre el mensaje y se valida si hay una estructura sintactica
        for i in range(len(palabras) - 1):
            if self.grafo_spam.has_edge(palabras[i], palabras[i + 1]):
                return True
        return False

    # funcion para clasificar si el mensaje es spam o no
    def es_spam(self, mensaje):
        porcentaje = 0.4  # 40%
        # validación de entrada
        texto = mensaje["texto"]
        es_valido, mensaje = self.validar_texto(texto)
        if not es_valido:
            return mensaje, []

        palabras = self.buscar_lexico(texto)
        coincidencias_semanticas = self.buscar_semantica(palabras)
        es_sintacticamente_spam = self.buscar_sintactica(palabras)
        
        if (
            len(coincidencias_semanticas) > int(len(palabras) * porcentaje)
            and es_sintacticamente_spam
        ):
            return "El texto es SPAM", coincidencias_semanticas
        else:
            return "El texto no es SPAM", []
