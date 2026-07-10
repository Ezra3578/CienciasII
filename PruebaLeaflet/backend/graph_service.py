"""
Etapa 1: construir el grafo de la ciudad con OSMnx y resolver caminos
más cortos (Dijkstra) entre depot y puntos de entrega.

El grafo se cachea en memoria como singleton simple para no volver a
descargarlo de OSM en cada request.
"""

import osmnx as ox
import networkx as nx
from typing import List, Tuple, Dict

# Región de trabajo fija para todo el proyecto. No se expone como
# parámetro de los endpoints para evitar reconstruir el grafo sobre
# otra ciudad por error.
PLACE_NAME = "Kamppi, Helsinki, Finland"

# Cache simple en memoria del grafo cargado.
_GRAPH_CACHE: Dict[str, nx.MultiDiGraph] = {}


def build_graph(network_type: str = "drive") -> nx.MultiDiGraph:
    """
    Descarga (o recupera de cache) el grafo vial de Kamppi, Helsinki.
    """
    cache_key = f"{PLACE_NAME}::{network_type}"
    if cache_key in _GRAPH_CACHE:
        return _GRAPH_CACHE[cache_key]

    G = ox.graph_from_place(PLACE_NAME, network_type=network_type)
    # Añade velocidades por tipo de vía y tiempo de viaje estimado.
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)

    # --- Atributos mínimos requeridos por nodo ---
    # 'x' (lng) e 'y' (lat) ya vienen por defecto en cada nodo gracias
    # a OSMnx. Acá inicializamos el tipo de nodo del negocio de
    # reparto: todos arrancan como "normal" (luego se puede marcar
    # alguno como "depot" o "deploy" con set_node_role).
    nx.set_node_attributes(G, "normal", "node_type")

    # --- Peso de las aristas ---
    # OSMnx ya trae 'length' (metros, distancia real del segmento vial)
    # en cada arista. Se espeja en un atributo explícito 'weight', que
    # es el que usan Dijkstra, la matriz de distancias y el TSP.
    for u, v, k, data in G.edges(keys=True, data=True):
        data["weight"] = data["length"]

    _GRAPH_CACHE[cache_key] = G
    return G


def get_graph(network_type: str = "drive") -> nx.MultiDiGraph:
    """Acceso de solo lectura al grafo ya construido (o lo construye si falta)."""
    return build_graph(network_type)


def set_node_role(G: nx.MultiDiGraph, node: int, role: str) -> None:
    """
    Marca un nodo con su rol de negocio: 'normal' | 'depot' | 'deploy'.
    """
    if role not in {"normal", "depot", "deploy"}:
        raise ValueError(f"role inválido: {role}")
    G.nodes[node]["node_type"] = role


def reset_node_roles(G: nx.MultiDiGraph) -> None:
    """
    Vuelve a marcar todos los nodos como 'normal'. Como el grafo se
    cachea (singleton), esto evita que quede un depot/deploy "viejo"
    marcado de una petición anterior con otras coordenadas.
    """
    nx.set_node_attributes(G, "normal", "node_type")


def nearest_node(G: nx.MultiDiGraph, lat: float, lng: float) -> int:
    """Encuentra el nodo del grafo más cercano a una coordenada (lat, lng)."""
    return ox.distance.nearest_nodes(G, X=lng, Y=lat)


def shortest_path(
    G: nx.MultiDiGraph,
    origin_node: int,
    destination_node: int,
    weight: str = "weight",
) -> Tuple[List[int], float]:
    """
    Ejecuta Dijkstra (vía networkx.shortest_path con weight) entre dos nodos.
    weight: 'weight' (distancia en metros, por defecto) o 'travel_time' (segundos).
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
    G: nx.MultiDiGraph, nodes: List[int], weight: str = "weight"
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
