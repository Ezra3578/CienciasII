"""
zoning_assembler.py
-------------------
Función de ensamblado de la respuesta final del endpoint /process.

Convierte los resultados del BFS multi-fuente (zona y frontera) en el
diccionario tipado ProcessResponse que se envía al frontend.

La llave de cada entrada es el nombre del depot (e.g. "A", "Bodega_Central"),
no un id inventado como "id_región1".
"""

from typing import Dict, List, Set, Tuple

from graph_adapter import GrafoLogico
from schemas_zonas import NodoCoord, regionData, ProcessResponse


def construir_ruta_zona(
    grafo_mst: GrafoLogico,
    nodos_de_la_zona: set[str],
    nombre_depot: str,
) -> Tuple[List[str], float]:
    """
    Construye el orden de visita (ruta) de los nodos de una zona
    recorriendo el subgrafo del MST restringido a esos nodos, usando
    un DFS (Depth-First Search) desde el depot.
    Ademas acumula la distancia real recorrida: cada arista del MST
    que el DFS atraviesa se cuenta dos veces (ida y vuelta), ya que el
    circuito cierra regresando al depot por el mismo arbol.
    El DFS garantiza un recorrido que sigue las ramas del árbol,
    visitando cada nodo exactamente una vez. Es la forma natural de
    "caminar" un árbol para hacer entregas.

    Parámetros
    ----------
    grafo_mst : GrafoLogico
        El Árbol de Recubrimiento Mínimo completo (con todos los nodos).

    nodos_de_la_zona : set[str]
        Conjunto de nombres de nodos que pertenecen a esta zona
        (incluye el depot).

    nombre_depot : str
        Nombre del depot desde donde inicia el recorrido.

    etorna
    -------
    (orden_visita, distancia_metros)
        - orden_visita: lista ordenada de nombres de nodos (depot al
          inicio y al final).
        - distancia_metros: metros totales recorridos (ida + vuelta)
          sobre las aristas del MST de esta zona.
    """

    # Adyacencia del MST completo
    adyacencia: dict[str, dict[str, float]] = grafo_mst.getNodos()

    # Recorrido DFS restringido a los nodos de la zona
    orden_visita: List[str] = []
    nodos_visitados: set[str] = set()
    pila_dfs: list[tuple[str, float | None]] = [(nombre_depot, None)]
    distancia_ida: float = 0.0

    while pila_dfs:
        nodo_actual, peso_desde_padre = pila_dfs.pop()

        if nodo_actual in nodos_visitados:
            continue

        nodos_visitados.add(nodo_actual)
        orden_visita.append(nodo_actual)

        if peso_desde_padre is not None:
            distancia_ida += peso_desde_padre

        vecinos_del_nodo: dict[str, float] = adyacencia.get(nodo_actual, {})
        for nombre_vecino in sorted(vecinos_del_nodo.keys()):
            if nombre_vecino in nodos_de_la_zona and nombre_vecino not in nodos_visitados:
              pila_dfs.append((nombre_vecino, vecinos_del_nodo[nombre_vecino]))

    # Cerrar el circuito: volver al depot al final de la ruta
    if len(orden_visita) > 1 and orden_visita[0] == nombre_depot:
        orden_visita.append(nombre_depot)

    distancia_metros: float = distancia_ida * 2 
    return orden_visita, distancia_metros


def construir_respuesta(
    zona: Dict[str, str],
    frontera: Dict[str, Set[str]],
    grafo_mst: GrafoLogico,
    coordenadas: Dict[str, Tuple[float, float]],
    lista_depots: List[str],
) -> ProcessResponse:
    """
    Ensambla el diccionario de respuesta final a partir de los resultados
    del BFS multi-fuente.

    Parámetros
    ----------
    zona : dict[str, str]
        Mapeo nombre_nodo -> nombre_depot (a qué depot pertenece cada nodo).

    frontera : dict[str, set[str]]
        Mapeo nombre_depot -> set de nodos que son frontera de esa zona.

    grafo_mst : GrafoLogico
        El Árbol de Recubrimiento Mínimo (para construir la ruta de visita).

    coordenadas : dict[str, tuple[float, float]]
        Mapeo nombre_nodo -> (latitud, longitud). Se construye a partir
        de datos.nodes (el body del request), NO del grafo lógico.

    lista_depots : list[str]
        Lista de nombres de los nodos depot.

    Retorna
    -------
    ProcessResponse (Dict[str, regionData])
        Diccionario donde la llave es el nombre del depot y el valor
        es un regionData con frontera y ruta.
    """

    respuesta: ProcessResponse = {}
    distancia_total_km: float = 0.0
    print("=== NODOS Y KILOMETROS POR ZONA ===")
    for indice, nombre_depot in enumerate(lista_depots, start=1):
        # Obtener todos los nodos asignados a este depot
        nodos_de_esta_zona: set[str] = {
            nombre_nodo
            for nombre_nodo, depot_asignado in zona.items()
            if depot_asignado == nombre_depot
        }

        # Construir el orden de visita (ruta) mediante DFS sobre el MST
        orden_ruta, distancia_metros = construir_ruta_zona(
            grafo_mst, nodos_de_esta_zona, nombre_depot
        )
        #imprimir en kilometros y nodos
        distancia_km = distancia_metros / 1000
        distancia_total_km += distancia_km
        print(
            f"Zona '{nombre_depot}': {len(nodos_de_esta_zona)} nodos, "
            f"{distancia_km:.2f} km recorridos"
        )
        # Ensamblar el regionData con coordenadas reales
        # La clave de la zona se representa con un identificador numérico
        # secuencial, que el frontend puede leer fácilmente.
        respuesta[str(indice)] = regionData(
            frontera=[
                NodoCoord(
                    nombre=nombre_nodo,
                    longitud=coordenadas[nombre_nodo][1],  # longitud es el segundo elemento
                    latitud=coordenadas[nombre_nodo][0],   # latitud es el primer elemento
                )
                for nombre_nodo in frontera.get(nombre_depot, set())
            ],
            ruta=[
                NodoCoord(
                    nombre=nombre_nodo,
                    longitud=coordenadas[nombre_nodo][1],
                    latitud=coordenadas[nombre_nodo][0],
                )
                for nombre_nodo in orden_ruta
            ],
        )
    print(f"=== TOTAL: {distancia_total_km:.2f} km recorridos en todas las zonas ===\n")
    return respuesta
