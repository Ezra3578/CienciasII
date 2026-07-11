"""
grafo_adapter.py
----------------
Reemplaza a Grafo.py: en vez de descargar su propia red vial con OSMnx,
usa el grafo compartido y cacheado de graph_service.py (Kamppi, Helsinki).

Expone exactamente la misma interfaz de "negocio" que Dijkstra.py espera
(getMatriz, getNodos, existeNodo), pero:
  - la red vial real es compartida (un solo grafo cacheado, no uno nuevo
    por instancia)
  - cada nodo lógico que se agrega queda además marcado en el grafo real
    con su node_type (depot/deploy), vía graph_service.set_node_role
  - las distancias entre nodos lógicos se calculan sobre el grafo real
    con el Dijkstra de networkx (graph_service.shortest_path), usando el
    atributo 'weight' (metros)

Cada request HTTP crea una instancia nueva de GrafoLogico (no se
persiste entre llamadas): es el "grafo de negocio" temporal sobre el que
corre el Dijkstra manual de Dijkstra.py.
"""

import networkx as nx
import graph_service


class GrafoLogico:
    """Grafo de negocio (nodos depot/delivery) apoyado en graph_service.py."""

    def __init__(self, network_type: str = "drive"):
        self.red_vial = graph_service.get_graph(network_type)
        self.aristas = {}       # nodo_logico -> {vecino: peso}
        self.coordenadas = {}   # nodo_logico -> (lat, lon)
        self.nodo_osmnx = {}    # nodo_logico -> id del nodo más cercano en red_vial
        self.roles = {}         # nodo_logico -> "depot" | "deploy" | "normal"

    # --- interfaz que espera Dijkstra.py ---

    def existeNodo(self, nodo):
        return nodo in self.aristas

    def existeArista(self, nodo1, nodo2):
        return nodo1 in self.aristas and nodo2 in self.aristas[nodo1]

    def getMatriz(self):
        return list(self.aristas.keys())

    def getNodos(self):
        return self.aristas

    # --- construcción del grafo de negocio ---

    def agregarNodo(self, nombre_nodo, lat, lon, role="normal"):
        """
        Agrega un nodo lógico (depot o delivery) y lo ancla al nodo más
        cercano de la red vial real. El rol se guarda en self.roles,
        SIN tocar self.red_vial (ver nota del módulo).
        """
        if nombre_nodo in self.aristas:
            return

        nodo_cercano = graph_service.nearest_node(self.red_vial, lat, lon)

        self.aristas[nombre_nodo] = {}
        self.coordenadas[nombre_nodo] = (lat, lon)
        self.nodo_osmnx[nombre_nodo] = nodo_cercano
        self.roles[nombre_nodo] = role

    def agregarArista(self, nodo1, nodo2, peso, bidireccional=True):
        if not self.existeNodo(nodo1) or not self.existeNodo(nodo2):
            return
        self.aristas[nodo1][nodo2] = peso
        if bidireccional:
            self.aristas[nodo2][nodo1] = peso

    def distancia_red_vial(self, nodo1, nodo2):
        """Distancia real (metros) entre dos nodos lógicos, por la red vial."""
        origen = self.nodo_osmnx[nodo1]
        destino = self.nodo_osmnx[nodo2]
        try:
            _, costo = graph_service.shortest_path(self.red_vial, origen, destino, weight="weight")
            return costo
        except nx.NetworkXNoPath:
            return None

    def ruta_real(self, nodo1, nodo2):
        """Lista de ids de la red vial que forman el camino real (por calles)."""
        origen = self.nodo_osmnx[nodo1]
        destino = self.nodo_osmnx[nodo2]
        try:
            ruta, _ = graph_service.shortest_path(self.red_vial, origen, destino, weight="weight")
            return ruta
        except nx.NetworkXNoPath:
            return []

    def agregarAristaAutomatica(self, nodo1, nodo2, bidireccional=True):
        """Igual que agregarArista, pero con peso = distancia real por la red vial."""
        peso = self.distancia_red_vial(nodo1, nodo2)
        if peso is None:
            return
        self.agregarArista(nodo1, nodo2, peso, bidireccional=bidireccional)

    def conectar_depots_con_entregas(self, nombres_depots, nombres_deliveries):
        """
        Conecta cada depot con cada punto de entrega (grafo bipartito),
        con peso = distancia real por la red vial.
        """
        for depot in nombres_depots:
            for entrega in nombres_deliveries:
                self.agregarAristaAutomatica(depot, entrega, bidireccional=True)