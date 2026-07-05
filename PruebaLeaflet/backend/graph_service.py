"""
Etapa 1: construir el grafo de la ciudad con OSMnx y resolver caminos
más cortos (Dijkstra) entre depot y puntos de entrega.

El grafo se cachea en memoria como singleton simple para no volver a
descargarlo de OSM en cada request. Para un proyecto académico esto
es suficiente; en producción real se guardaría en disco (GraphML) o
en una base de datos espacial.
"""

import osmnx as ox
import networkx as nx
from typing import List, Tuple, Dict

# Cache simple en memoria del grafo cargado.
_GRAPH_CACHE: Dict[str, nx.MultiDiGraph] = {}


def build_graph(place_name: str, network_type: str = "drive") -> nx.MultiDiGraph:
    """
    Descarga (o recupera de cache) el grafo vial de una ciudad/zona.
    """
    cache_key = f"{place_name}::{network_type}"
    if cache_key in _GRAPH_CACHE:
        return _GRAPH_CACHE[cache_key]

    G = ox.graph_from_place(place_name, network_type=network_type)
    # Añade atributo 'length' en metros (ya viene por defecto) y tiempo
    # de viaje estimado usando velocidades por tipo de vía.
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)

    _GRAPH_CACHE[cache_key] = G
    return G


def get_graph(place_name: str, network_type: str = "drive") -> nx.MultiDiGraph:
    """Acceso de solo lectura al grafo ya construido (o lo construye si falta)."""
    return build_graph(place_name, network_type)


def nearest_node(G: nx.MultiDiGraph, lat: float, lng: float) -> int:
    """Encuentra el nodo del grafo más cercano a una coordenada (lat, lng)."""
    return ox.distance.nearest_nodes(G, X=lng, Y=lat)


def shortest_path(
    G: nx.MultiDiGraph,
    origin_node: int,
    destination_node: int,
    weight: str = "length",
) -> Tuple[List[int], float]:
    """
    Ejecuta Dijkstra (vía networkx.shortest_path con weight) entre dos nodos.
    weight: 'length' (metros) o 'travel_time' (segundos).
    Retorna la lista de nodos de la ruta y el costo total.
    """
    route = nx.shortest_path(G, origin_node, destination_node, weight=weight, method="dijkstra")
    cost = nx.shortest_path_length(G, origin_node, destination_node, weight=weight, method="dijkstra")
    return route, cost


def route_to_geojson(G: nx.MultiDiGraph, route: List[int]) -> dict:
    """Convierte una lista de nodos en un Feature GeoJSON tipo LineString."""
    coords = [[G.nodes[n]["x"], G.nodes[n]["y"]] for n in route]  # [lng, lat]
    return {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {},
    }


def distance_matrix(
    G: nx.MultiDiGraph, nodes: List[int], weight: str = "length"
) -> List[List[float]]:
    """
    Calcula la matriz de distancias par-a-par entre una lista de nodos,
    corriendo Dijkstra repetido (nx.single_source_dijkstra_path_length).
    Se usa tanto para el coloreado (para detectar 'vecindad/conflicto')
    como para el TSP dentro de cada zona.
    """
    n = len(nodes)
    matrix = [[0.0] * n for _ in range(n)]
    for i, src in enumerate(nodes):
        lengths = nx.single_source_dijkstra_path_length(G, src, weight=weight)
        for j, dst in enumerate(nodes):
            matrix[i][j] = lengths.get(dst, float("inf"))
    return matrix
