import networkx as nx
import matplotlib.pyplot as plt

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

    # funcion para buscar palabras en el mensaje ingresado
    def buscar_lexico(self, mensaje):
        # validación de entrada
        if not isinstance(mensaje, str) or not mensaje.strip():
            return []

        palabras = []
        palabra = ""
        # se recorre el mensaje y se valida si es una letra
        for letra in mensaje:
            if letra.isalpha():
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
        # validación de entrada
        texto = mensaje["texto"]
        # se valida si el texto es una cadena de texto y si no esta vacio
        if not isinstance(texto, str) or not texto.strip():
            return "Texto no válido", []

        palabras = self.buscar_lexico(texto)
        coincidencias_semanticas = self.buscar_semantica(palabras)
        es_sintacticamente_spam = self.buscar_sintactica(palabras)

        if coincidencias_semanticas or es_sintacticamente_spam:
            return "Spam", coincidencias_semanticas
        else:
            return "No Spam", []
