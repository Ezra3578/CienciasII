"""
Dijkstra.py
-----------
Adaptación a Python del algoritmo de Dijkstra (implementado originalmente en
Java sobre una MatrizAdyacencia) para trabajar con el objeto `Grafo` de
Grafo.py.

El objeto `grafo` recibido debe exponer:
    - grafo.getMatriz()        -> lista/iterable con los nombres de todos los nodos
    - grafo.getNodos()         -> dict {nodo: {vecino: peso, ...}, ...}
    - grafo.existeNodo(nombre) -> bool

(el Integer.MAX_VALUE de Java se reemplaza aquí por math.inf)
"""

import math


class Dijkstra:

    def __init__(self, grafo):
        self.grafo = grafo
        self.distancias_por_origen = {}
        self.predecesores_por_origen = {}
        self.pasos = 0

    def calcularDistanciaMasCorta(self, nodo_inicial):
        distancias = {}
        visitados = {}
        predecesores = {}
        self.pasos = 0

        for nodo in self.grafo.getMatriz():
            distancias[nodo] = math.inf
            visitados[nodo] = False
            predecesores[nodo] = None

        distancias[nodo_inicial] = 0

        tamano = len(self.grafo.getMatriz())

        # seleccionar en cada iteración el nodo no visitado con distancia menor
        for _ in range(tamano):
            distancia_min = math.inf
            nodo_menor = None
            for nodo in self.grafo.getMatriz():
                if not visitados[nodo] and distancias[nodo] < distancia_min:
                    distancia_min = distancias[nodo]
                    nodo_menor = nodo
                self.pasos += 1

            if nodo_menor is None:
                break

            visitados[nodo_menor] = True

            # relajar las aristas salientes del nodo elegido
            for nodo_comparacion, peso in self.grafo.getNodos().get(nodo_menor, {}).items():
                if not visitados.get(nodo_comparacion, False):
                    temp = distancias[nodo_menor] + peso
                    if temp < distancias[nodo_comparacion]:
                        distancias[nodo_comparacion] = temp
                        predecesores[nodo_comparacion] = nodo_menor

        self.distancias_por_origen[nodo_inicial] = distancias
        self.predecesores_por_origen[nodo_inicial] = predecesores

    def getDistancia(self, nodo_inicial, nodo_destino=None):
        """
        Equivalente a los dos getDistancia(...) sobrecargados en Java:
        - getDistancia(nodo_inicial)                -> todas las distancias
        - getDistancia(nodo_inicial, nodo_destino)   -> una distancia puntual
        """
        if not self.grafo.existeNodo(nodo_inicial):
            return "Error: El nodo de inicio no existe en el grafo."
        if nodo_destino is not None and not self.grafo.existeNodo(nodo_destino):
            return "Error: Al menos uno de sus nodos no existe en el grafo."

        self.calcularDistanciaMasCorta(nodo_inicial)
        distancias = self.distancias_por_origen[nodo_inicial]

        if nodo_destino is None:
            resultado = f"Distancias desde el nodo {nodo_inicial}:\n"
            for nodo in self.grafo.getMatriz():
                dist = distancias[nodo]
                if dist == math.inf:
                    resultado += f"{nodo}: INFINITO (no alcanzable)\n"
                else:
                    resultado += f"{nodo}: {dist}\n"
            return resultado

        dist = distancias[nodo_destino]
        if dist == math.inf:
            return f"No existe camino entre {nodo_inicial} y {nodo_destino}."
        return f"Distancia entre {nodo_inicial} y {nodo_destino}: {dist}"

    def getCamino(self, nodo_inicial, nodo_destino=None):
        """
        Equivalente a los dos getCamino(...) sobrecargados en Java:
        - getCamino(nodo_inicial)                -> todos los caminos desde nodo_inicial
        - getCamino(nodo_inicial, nodo_destino)   -> un camino puntual
        """
        if not self.grafo.existeNodo(nodo_inicial):
            return "Error: El nodo de inicio no existe en el grafo."
        if nodo_destino is not None and not self.grafo.existeNodo(nodo_destino):
            return "Error: Al menos uno de sus nodos no existe en el grafo."

        self.calcularDistanciaMasCorta(nodo_inicial)

        if nodo_destino is None:
            resultado = ""
            for nodo in self.grafo.getMatriz():
                if nodo == nodo_inicial:
                    continue
                resultado += f"{nodo_inicial} -> {nodo}: {self._reconstruirCamino(nodo_inicial, nodo)}\n"
            return resultado

        return self._reconstruirCamino(nodo_inicial, nodo_destino)

    def getCaminoLista(self, nodo_inicial, nodo_destino):
        """
        Extra (no está en la versión Java): igual que getCamino, pero devuelve
        la ruta como lista de nombres ['A', 'B', 'C'] en vez de un string
        'A -> B -> C'. Sirve para pasarla directo a Grafo.dibujar_camino().
        """
        if not self.grafo.existeNodo(nodo_inicial) or not self.grafo.existeNodo(nodo_destino):
            return []

        self.calcularDistanciaMasCorta(nodo_inicial)
        distancias = self.distancias_por_origen[nodo_inicial]
        predecesores = self.predecesores_por_origen[nodo_inicial]

        if distancias[nodo_destino] == math.inf:
            return []

        camino = []
        actual = nodo_destino
        while actual is not None:
            camino.insert(0, actual)
            actual = predecesores[actual]
        return camino

    def getPasos(self):
        return self.pasos

    def _reconstruirCamino(self, nodo_inicial, nodo_destino):
        distancias = self.distancias_por_origen[nodo_inicial]
        predecesores = self.predecesores_por_origen[nodo_inicial]

        if distancias[nodo_destino] == math.inf:
            return "No existe camino"

        camino = []
        actual = nodo_destino
        while actual is not None:
            camino.insert(0, actual)
            actual = predecesores[actual]

        return " -> ".join(camino)
