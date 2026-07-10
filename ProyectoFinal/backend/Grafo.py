"""
Grafo.py
--------
Adaptación a Python de la interfaz Java `RepresentacionGrafo`, implementada
como lista de adyacencia y apoyada en la librería OSMnx para ubicar los nodos
sobre la red vial real de Madrid (Cundinamarca, Colombia).

Idea general
------------
- `self.red_vial` es el grafo de calles descargado de OpenStreetMap con OSMnx.
  Se usa como "mapa base" para geolocalizar los nodos lógicos y para dibujar
  el resultado final.
- `self.aristas` es la lista de adyacencia "de negocio" (nodo_logico ->
  {vecino: peso}), la que en verdad usa Dijkstra.py. Es totalmente
  independiente de los miles de nodos internos de `self.red_vial`.
- Cada nodo lógico que se agrega con `agregarNodo` queda "anclado" al nodo
  más cercano de la red vial (`ox.distance.nearest_nodes`), lo que permite
  luego calcular distancias/rutas reales siguiendo las calles.
"""

import osmnx as ox
import networkx as nx


class Grafo:
    """Implementación en Python de RepresentacionGrafo (lista de adyacencia)."""

    def __init__(self, lugar="Madrid, Cundinamarca, Colombia", network_type="drive"):
        print(f"Descargando red vial de '{lugar}' desde OpenStreetMap (osmnx)...")
        self.lugar = lugar
        self.red_vial = ox.graph_from_place(lugar, network_type=network_type)
        self.aristas = {}       # nodo_logico -> {vecino: peso}
        self.coordenadas = {}   # nodo_logico -> (lat, lon)
        self.nodo_osmnx = {}    # nodo_logico -> id del nodo más cercano en red_vial
        print(f"Red vial descargada: {len(self.red_vial.nodes)} nodos, "
              f"{len(self.red_vial.edges)} tramos.")

    # ------------------------------------------------------------------
    # Métodos de la interfaz RepresentacionGrafo
    # ------------------------------------------------------------------

    def agregarNodo(self, nombre_nodo, lat=None, lon=None):
        """
        Agrega un nodo lógico (punto de despacho o de entrega).
        Si no se dan lat/lon, se intenta geocodificar el nombre dentro de
        `self.lugar` (funciona bien con direcciones reales; para nombres
        inventados como 'Bodega_Central' es más confiable pasar lat/lon).
        """
        if nombre_nodo in self.aristas:
            print(f"Aviso: el nodo '{nombre_nodo}' ya existe, no se agrega de nuevo.")
            return

        if lat is None or lon is None:
            consulta = f"{nombre_nodo}, {self.lugar}"
            try:
                lat, lon = ox.geocode(consulta)
            except Exception as e:
                raise ValueError(
                    f"No se pudo geocodificar '{nombre_nodo}'. Indica sus coordenadas "
                    f"manualmente: agregarNodo('{nombre_nodo}', lat=..., lon=...)."
                ) from e

        nodo_cercano = ox.distance.nearest_nodes(self.red_vial, X=lon, Y=lat)

        self.aristas[nombre_nodo] = {}
        self.coordenadas[nombre_nodo] = (lat, lon)
        self.nodo_osmnx[nombre_nodo] = nodo_cercano

    def eliminarNodo(self, nombre_nodo):
        if nombre_nodo not in self.aristas:
            print(f"Aviso: el nodo '{nombre_nodo}' no existe.")
            return
        del self.aristas[nombre_nodo]
        del self.coordenadas[nombre_nodo]
        del self.nodo_osmnx[nombre_nodo]
        for vecinos in self.aristas.values():
            vecinos.pop(nombre_nodo, None)

    def agregarArista(self, nombre_nodo1, nombre_nodo2, peso, bidireccional=False):
        if not self.existeNodo(nombre_nodo1) or not self.existeNodo(nombre_nodo2):
            print(f"Error: no se puede crear la arista, "
                  f"'{nombre_nodo1}' o '{nombre_nodo2}' no existe(n).")
            return
        self.aristas[nombre_nodo1][nombre_nodo2] = peso
        if bidireccional:
            self.aristas[nombre_nodo2][nombre_nodo1] = peso

    def eliminarArista(self, nodo_origen, nodo_destino):
        if self.existeArista(nodo_origen, nodo_destino):
            del self.aristas[nodo_origen][nodo_destino]

    def actualizarPesoArista(self, nodo_origen, nodo_destino, nuevo_peso):
        if not self.existeArista(nodo_origen, nodo_destino):
            print(f"Error: la arista {nodo_origen} -> {nodo_destino} no existe.")
            return
        self.aristas[nodo_origen][nodo_destino] = nuevo_peso

    def existeNodo(self, nodo):
        return nodo in self.aristas

    def existeArista(self, nodo1, nodo2):
        return nodo1 in self.aristas and nodo2 in self.aristas[nodo1]

    # ------------------------------------------------------------------
    # Métodos que consume Dijkstra.py (equivalentes a MatrizAdyacencia)
    # ------------------------------------------------------------------

    def getMatriz(self):
        """Devuelve los nombres de todos los nodos lógicos (el 'conjunto de vértices')."""
        return list(self.aristas.keys())

    def getNodos(self):
        """Devuelve la lista de adyacencia completa: nodo -> {vecino: peso}."""
        return self.aristas

    # ------------------------------------------------------------------
    # Extras: no están en la interfaz Java original, pero son muy útiles
    # para no tener que inventar los pesos a mano.
    # ------------------------------------------------------------------

    def distancia_red_vial(self, nombre_nodo1, nombre_nodo2):
        """Distancia real en metros entre dos nodos lógicos, siguiendo la red vial."""
        if not self.existeNodo(nombre_nodo1) or not self.existeNodo(nombre_nodo2):
            return None
        origen = self.nodo_osmnx[nombre_nodo1]
        destino = self.nodo_osmnx[nombre_nodo2]
        try:
            metros = nx.shortest_path_length(self.red_vial, origen, destino, weight="length")
            return round(metros)
        except nx.NetworkXNoPath:
            return None

    def agregarAristaAutomatica(self, nombre_nodo1, nombre_nodo2, bidireccional=False):
        """Igual que agregarArista, pero calculando el peso automáticamente
        como la distancia real (en metros) por la red vial."""
        peso = self.distancia_red_vial(nombre_nodo1, nombre_nodo2)
        if peso is None:
            print(f"Error: no existe ruta vial entre '{nombre_nodo1}' y '{nombre_nodo2}'.")
            return
        self.agregarArista(nombre_nodo1, nombre_nodo2, peso, bidireccional=bidireccional)

    def ruta_real(self, nombre_nodo1, nombre_nodo2):
        """Lista de ids de la red vial que forman el camino real (por calles)
        entre dos nodos lógicos. Se usa solo para graficar."""
        origen = self.nodo_osmnx[nombre_nodo1]
        destino = self.nodo_osmnx[nombre_nodo2]
        try:
            return nx.shortest_path(self.red_vial, origen, destino, weight="length")
        except nx.NetworkXNoPath:
            return []

    # ------------------------------------------------------------------
    # Graficación
    # ------------------------------------------------------------------

    def dibujar_camino(self, camino_nodos, titulo="Ruta calculada con Dijkstra", guardar_como=None):
        """
        Dibuja la red vial completa, todos los nodos lógicos (en gris) y resalta
        en rojo el camino recibido (lista de nombres de nodo, en orden).
        """
        import matplotlib.pyplot as plt

        fig, ax = ox.plot_graph(
            self.red_vial, show=False, close=False,
            node_size=0, edge_color="#cccccc", edge_linewidth=0.7,
            bgcolor="white", figsize=(11, 11),
        )

        # Todos los nodos lógicos, en gris
        for nombre, (lat, lon) in self.coordenadas.items():
            ax.scatter(lon, lat, c="#888888", s=40, zorder=3)
            ax.annotate(nombre, (lon, lat), fontsize=8, color="#555555",
                        xytext=(3, 3), textcoords="offset points")

        # Camino real (por calles) tramo a tramo, en rojo
        for i in range(len(camino_nodos) - 1):
            ruta = self.ruta_real(camino_nodos[i], camino_nodos[i + 1])
            if not ruta:
                continue
            xs = [self.red_vial.nodes[n]["x"] for n in ruta]
            ys = [self.red_vial.nodes[n]["y"] for n in ruta]
            ax.plot(xs, ys, c="red", linewidth=3, zorder=4)

        # Nodos que hacen parte del camino: inicio (verde), destino (azul), intermedios (naranja)
        for idx, nombre in enumerate(camino_nodos):
            lat, lon = self.coordenadas[nombre]
            if idx == 0:
                color = "green"
            elif idx == len(camino_nodos) - 1:
                color = "blue"
            else:
                color = "orange"
            ax.scatter(lon, lat, c=color, s=120, zorder=5, edgecolors="black")
            ax.annotate(nombre, (lon, lat), fontsize=10, fontweight="bold",
                        xytext=(5, 5), textcoords="offset points")

        ax.set_title(titulo)
        plt.tight_layout()
        if guardar_como:
            plt.savefig(guardar_como, dpi=150)
            print(f"Gráfico guardado en: {guardar_como}")
        plt.show()
        return fig, ax
