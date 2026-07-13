"""
bfs_multifuente.py
------------------
Implementación de BFS multi-fuente (multi-source BFS) sobre el Árbol de
Recubrimiento Mínimo (MST).

La idea: se lanza un recorrido por niveles (BFS) simultáneamente desde
TODOS los nodos de tipo "depot" al mismo tiempo. En cada nivel del BFS,
cada depot "reclama" los nodos vecinos aún no asignados, respetando un
cupo máximo de nodos por zona.

Resultado:
  - zona:     dict[nombre_nodo] -> nombre_depot   (a qué depot pertenece cada nodo)
  - frontera: dict[nombre_depot] -> set(nodos)    (nodos de borde de cada zona,
              es decir, nodos que tienen al menos un vecino asignado a otra zona)
"""

from collections import deque
from typing import Dict, List, Set, Tuple

from graph_adapter import GrafoLogico


def bfs_multifuente(
    grafo_mst: GrafoLogico,
    lista_depots: List[str],
    cupo_maximo_por_zona: int,
) -> Tuple[Dict[str, str], Dict[str, Set[str]]]:
    """
    Ejecuta un BFS multi-fuente sobre el grafo MST para asignar cada
    nodo a la zona del depot más cercano (en hops del árbol), respetando
    un cupo máximo de nodos por zona.

    Parámetros
    ----------
    grafo_mst : GrafoLogico
        El Árbol de Recubrimiento Mínimo construido en el paso anterior.
        Sus aristas representan las conexiones del árbol (no del grafo
        original completo).

    lista_depots : list[str]
        Nombres de los nodos que son depósitos (puntos de salida de
        los camiones). Son las "fuentes" del BFS.

    cupo_maximo_por_zona : int
        Cantidad máxima de nodos (incluyendo el depot) que puede tener
        cada zona. Si una zona alcanza este límite, ya no reclama más
        nodos vecinos.

    Retorna
    -------
    (zona, frontera)
        - zona: dict[str, str]
            Mapeo nombre_nodo -> nombre_depot. Indica a qué depot
            pertenece cada nodo del grafo.
        - frontera: dict[str, set[str]]
            Mapeo nombre_depot -> set de nodos que son frontera de esa
            zona (nodos que tienen al menos un vecino en otra zona).
    """

    # --- Diccionario de adyacencia del MST ---
    # grafo_mst.getNodos() retorna el dict {nodo: {vecino: peso, ...}}
    adyacencia: dict[str, dict[str, float]] = grafo_mst.getNodos()

    # --- Inicialización ---
    # Cada depot se asigna a sí mismo como zona
    zona: Dict[str, str] = {}
    for nombre_depot in lista_depots:
        zona[nombre_depot] = nombre_depot

    # Contador de nodos asignados a cada zona (el depot ya cuenta como 1)
    conteo_zona: Dict[str, int] = {}
    for nombre_depot in lista_depots:
        conteo_zona[nombre_depot] = 1

    # Cola del BFS: contiene tuplas (nombre_nodo, nombre_depot_dueno)
    # Se inicializa con todos los depots (multi-source)
    cola_bfs: deque[Tuple[str, str]] = deque()
    for nombre_depot in lista_depots:
        cola_bfs.append((nombre_depot, nombre_depot))

    # --- Recorrido BFS por niveles ---
    # En cada iteración, se procesan todos los nodos del nivel actual
    # antes de pasar al siguiente. Esto garantiza que los depots
    # "expanden" sus zonas de forma equitativa (nivel a nivel).
    while cola_bfs:
        # Determinamos cuántos nodos hay en el nivel actual
        tamano_nivel_actual: int = len(cola_bfs)

        for _ in range(tamano_nivel_actual):
            nodo_actual, depot_dueno = cola_bfs.popleft()

            # Revisar cada vecino del nodo actual en el MST
            vecinos_del_nodo: dict[str, float] = adyacencia.get(nodo_actual, {})

            for nombre_vecino in vecinos_del_nodo:
                # Si el vecino ya fue asignado a alguna zona, saltar
                if nombre_vecino in zona:
                    continue

                # Si la zona del depot dueño ya alcanzó su cupo máximo, saltar
                if conteo_zona[depot_dueno] >= cupo_maximo_por_zona:
                    continue

                # Asignar el vecino a la zona del depot dueño
                zona[nombre_vecino] = depot_dueno
                conteo_zona[depot_dueno] += 1

                # Encolar el vecino para seguir expandiendo en el próximo nivel
                cola_bfs.append((nombre_vecino, depot_dueno))

    # --- Nodos huérfanos ---
    # Si algún nodo no fue asignado (por cupo agotado en todas las zonas),
    # se asigna al depot cuya zona tenga menos nodos (balance residual).
    todos_los_nodos: list[str] = list(adyacencia.keys())
    nodos_sin_asignar: list[str] = [
        nombre_nodo for nombre_nodo in todos_los_nodos if nombre_nodo not in zona
    ]

    for nombre_nodo in nodos_sin_asignar:
        # Buscar el depot con menos nodos asignados
        depot_con_menos_carga: str = min(conteo_zona, key=conteo_zona.get)
        zona[nombre_nodo] = depot_con_menos_carga
        conteo_zona[depot_con_menos_carga] += 1

    # --- Cálculo de la frontera de cada zona ---
    # Un nodo es "frontera" de su zona si tiene al menos un vecino
    # asignado a una zona diferente.
    frontera: Dict[str, Set[str]] = {nombre_depot: set() for nombre_depot in lista_depots}

    for nombre_nodo, depot_dueno in zona.items():
        vecinos_del_nodo = adyacencia.get(nombre_nodo, {})
        for nombre_vecino in vecinos_del_nodo:
            # Si el vecino está en otra zona, este nodo es frontera
            zona_vecino: str = zona.get(nombre_vecino, "")
            if zona_vecino != depot_dueno:
                frontera[depot_dueno].add(nombre_nodo)
                break  # Ya sabemos que es frontera, no necesitamos seguir

    return zona, frontera
