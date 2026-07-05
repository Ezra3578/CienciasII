"""
Etapa 2: coloreado de grafos para asignar zonas de reparto.

Estrategia:
1. Construir un grafo de "conflicto" entre puntos de entrega: dos puntos
   son adyacentes/conflictivos si están dentro de un radio de distancia
   (o son vecinos cercanos en el grafo vial). Esto define qué nodos NO
   pueden compartir color (zona).
2. Aplicar coloreado voraz de NetworkX (greedy_color) sobre ese grafo
   de conflicto.
3. (Opcional) Rebalancear cargas entre colores con una heurística local:
   mover un punto de un color sobrecargado a otro color válido (que no
   rompa la restricción de vecinos) si eso mejora el balance.

Nota conceptual: el coloreado clásico minimiza colores, no balancea
carga. El paso 3 es la parte que introduce el balanceo como requisito
adicional del proyecto.
"""

import networkx as nx
from typing import List, Dict
from collections import defaultdict


def build_conflict_graph(
    delivery_nodes: List[int], distance_matrix: List[List[float]], conflict_radius: float
) -> nx.Graph:
    """
    Crea un grafo simple donde cada entrega es un nodo, y hay arista
    (conflicto) entre dos entregas si su distancia en el grafo vial es
    menor a conflict_radius (ej. 300 metros => se consideran "vecinas").
    """
    n = len(delivery_nodes)
    C = nx.Graph()
    C.add_nodes_from(range(n))  # usamos índices 0..n-1, no ids del grafo vial
    for i in range(n):
        for j in range(i + 1, n):
            if distance_matrix[i][j] <= conflict_radius:
                C.add_edge(i, j)
    return C


def color_deliveries(
    conflict_graph: nx.Graph,
    n_colors: int | None = None,
    strategy: str = "saturation_largest_first",
) -> Dict[int, int]:
    """
    Aplica coloreado voraz de NetworkX. Retorna {indice_entrega: color}.
    Si n_colors se especifica y el greedy usa menos, está bien (subconjunto
    de zonas activas); si usa más, se podría re-ejecutar con otra estrategia
    o aceptar el resultado según el proyecto.
    """
    coloring = nx.algorithms.coloring.greedy_color(conflict_graph, strategy=strategy)
    return coloring


def rebalance_colors(
    coloring: Dict[int, int],
    conflict_graph: nx.Graph,
    max_iterations: int = 200,
) -> Dict[int, int]:
    """
    Heurística simple de rebalanceo de carga por color (zona):
    mientras exista una zona con más nodos que otra por encima de un
    umbral, intenta mover un nodo de la zona sobrecargada a la
    subcargada, siempre que no tenga vecinos (conflicto) en la zona
    destino.
    """
    coloring = dict(coloring)  # copia mutable

    def load_by_color(col: Dict[int, int]) -> Dict[int, int]:
        loads = defaultdict(int)
        for node, color in col.items():
            loads[color] += 1
        return loads

    for _ in range(max_iterations):
        loads = load_by_color(coloring)
        if not loads:
            break
        max_color = max(loads, key=loads.get)
        min_color = min(loads, key=loads.get)

        if loads[max_color] - loads[min_color] <= 1:
            break  # ya está razonablemente balanceado

        moved = False
        for node, color in coloring.items():
            if color != max_color:
                continue
            neighbor_colors = {coloring[nb] for nb in conflict_graph.neighbors(node)}
            if min_color not in neighbor_colors:
                coloring[node] = min_color
                moved = True
                break

        if not moved:
            break  # no hay movimiento válido posible, se detiene

    return coloring


def build_zones(
    delivery_points: list,
    delivery_nodes: List[int],
    distance_matrix: List[List[float]],
    conflict_radius: float = 300.0,
    n_colors: int | None = None,
    balance: bool = True,
) -> Dict[int, List[int]]:
    """
    Pipeline completo de la etapa 2.
    Retorna {color: [indices de entrega en esa zona]}.
    """
    conflict_graph = build_conflict_graph(delivery_nodes, distance_matrix, conflict_radius)
    coloring = color_deliveries(conflict_graph, n_colors=n_colors)

    if balance:
        coloring = rebalance_colors(coloring, conflict_graph)

    zones = defaultdict(list)
    for idx, color in coloring.items():
        zones[color].append(idx)

    return dict(zones)
