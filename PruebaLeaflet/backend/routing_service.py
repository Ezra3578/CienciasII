"""
Etapa 3: dentro de cada zona (color), planificar la ruta de entrega
más corta (heurística de TSP) y comparar tiempos entre estrategias.

Se implementa una heurística simple y transparente:
  1. Vecino más cercano (nearest neighbor) para una solución inicial.
  2. Mejora local 2-opt para refinarla.

Esto es intencionalmente sencillo de leer/depurar. Si se requiere una
cota de referencia más fuerte, se puede comparar contra `python-tsp`
u OR-Tools (ver comentarios al final).
"""

import time
from typing import List, Tuple


def nearest_neighbor_route(distance_matrix: List[List[float]], start: int = 0) -> List[int]:
    n = len(distance_matrix)
    unvisited = set(range(n))
    route = [start]
    unvisited.remove(start)
    current = start

    while unvisited:
        nxt = min(unvisited, key=lambda j: distance_matrix[current][j])
        route.append(nxt)
        unvisited.remove(nxt)
        current = nxt

    return route


def route_length(route: List[int], distance_matrix: List[List[float]]) -> float:
    return sum(distance_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))


def two_opt(route: List[int], distance_matrix: List[List[float]]) -> List[int]:
    """
    Mejora 2-opt clásica: intenta invertir segmentos de la ruta si eso
    reduce la distancia total, hasta que no haya más mejoras posibles.
    """
    best = route[:]
    improved = True

    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best) - 1):
                if j - i == 1:
                    continue
                new_route = best[:i] + best[i:j][::-1] + best[j:]
                if route_length(new_route, distance_matrix) < route_length(best, distance_matrix):
                    best = new_route
                    improved = True

    return best


def solve_zone_route(
    distance_matrix: List[List[float]], depot_index: int = 0
) -> dict:
    """
    Resuelve el TSP heurístico dentro de una zona, empezando y (si se
    quiere ciclo cerrado) regresando al depot. Retorna la ruta (índices
    locales), la distancia total y el tiempo que tomó calcularla, para
    poder comparar entre zonas o entre métodos.
    """
    t0 = time.perf_counter()

    initial = nearest_neighbor_route(distance_matrix, start=depot_index)
    improved = two_opt(initial, distance_matrix)

    elapsed = time.perf_counter() - t0

    return {
        "route_indices": improved,
        "total_distance": route_length(improved, distance_matrix),
        "compute_time_seconds": elapsed,
        "method": "nearest_neighbor + 2opt",
    }


# --------------------------------------------------------------------
# Punto de extensión: comparación contra otra heurística/solver exacto.
# Ejemplo de integración con python-tsp (instalar con:
#   pip install python-tsp)
#
# from python_tsp.heuristics import solve_tsp_simulated_annealing
# import numpy as np
#
# def solve_zone_route_reference(distance_matrix):
#     matrix = np.array(distance_matrix)
#     permutation, distance = solve_tsp_simulated_annealing(matrix)
#     return {"route_indices": permutation, "total_distance": distance}
# --------------------------------------------------------------------
