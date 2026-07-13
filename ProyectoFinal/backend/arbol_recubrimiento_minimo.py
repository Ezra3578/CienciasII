"""
arbol_recubrimiento_minimo.py
-----------------------------
Implementación del Árbol de Recubrimiento Mínimo (MST - Minimum Spanning Tree)
usando el algoritmo de Prim sobre la matriz de distancias que retorna
FloydWarshall.getMatrizDistancias().

El objetivo es construir el árbol más barato que conecta TODOS los nodos
lógicos del grafo, sin importar si estaban directamente conectados o no
en el grafo original. La matriz de Floyd-Warshall ya nos da la distancia
más corta entre todo par de nodos, así que el MST opera sobre un "grafo
completo virtual" donde cada arista tiene peso = distancia más corta real.

Retorna un objeto GrafoLogico que representa únicamente las aristas del
árbol (subgrafo del grafo completo virtual).
"""

import math
from typing import Dict

from graph_adapter import GrafoLogico


def construir_mst(
    matriz_distancias: Dict[str, Dict[str, float]],
    grafo_original: GrafoLogico,
) -> GrafoLogico:
    """
    Construye el Árbol de Recubrimiento Mínimo a partir de la matriz de
    distancias de Floyd-Warshall, usando el algoritmo de Prim.

    Parámetros
    ----------
    matriz_distancias : dict[str, dict[str, float]]
        Resultado de FloydWarshall.getMatrizDistancias().
        Formato: matriz_distancias[origen][destino] = distancia_minima.

    grafo_original : GrafoLogico
        El grafo lógico original del que se extraen las coordenadas y
        roles de cada nodo (depot/deploy) para poblar el MST resultante.

    Retorna
    -------
    GrafoLogico
        Un nuevo grafo lógico que contiene los mismos nodos pero solo
        las aristas que forman el árbol de recubrimiento mínimo.
    """

    # --- Obtener la lista de todos los nodos del grafo ---
    lista_nodos: list[str] = list(matriz_distancias.keys())
    cantidad_nodos: int = len(lista_nodos)

    # Caso trivial: si hay 0 o 1 nodo, el MST es el grafo sin aristas
    if cantidad_nodos <= 1:
        grafo_mst = GrafoLogico()
        for nombre_nodo in lista_nodos:
            latitud, longitud = grafo_original.coordenadas[nombre_nodo]
            rol_nodo: str = grafo_original.roles.get(nombre_nodo, "normal")
            grafo_mst.agregarNodo(nombre_nodo, latitud, longitud, role=rol_nodo)
        return grafo_mst

    # --- Algoritmo de Prim ---
    # Se mantiene un conjunto de nodos ya incluidos en el MST y se va
    # extendiendo eligiendo siempre la arista de menor peso que conecte
    # un nodo dentro del MST con uno fuera de él.

    # Estructura para guardar las aristas elegidas del MST
    aristas_mst: list[tuple[str, str, float]] = []

    # Conjunto de nodos ya incorporados al árbol
    nodos_en_arbol: set[str] = set()

    # Diccionario de costo mínimo para alcanzar cada nodo desde el árbol.
    # costo_minimo[nodo] = (peso_arista_mas_barata, nodo_padre_en_arbol)
    costo_minimo: dict[str, tuple[float, str | None]] = {}

    # Inicializar todos los costos en infinito
    for nombre_nodo in lista_nodos:
        costo_minimo[nombre_nodo] = (math.inf, None)

    # Elegir el primer nodo como punto de partida (arbitrario)
    nodo_inicial: str = lista_nodos[0]
    costo_minimo[nodo_inicial] = (0.0, None)

    # Iterar hasta incluir todos los nodos en el árbol
    for _ in range(cantidad_nodos):
        # Buscar el nodo no incluido con menor costo de conexión al árbol
        nodo_elegido: str | None = None
        peso_elegido: float = math.inf

        for nombre_nodo in lista_nodos:
            if nombre_nodo in nodos_en_arbol:
                continue  # Ya está en el árbol, saltar
            costo_actual, _ = costo_minimo[nombre_nodo]
            if costo_actual < peso_elegido:
                peso_elegido = costo_actual
                nodo_elegido = nombre_nodo

        # Si no se encontró ningún nodo alcanzable, el grafo es disconexo
        if nodo_elegido is None:
            break

        # Incorporar el nodo elegido al árbol
        nodos_en_arbol.add(nodo_elegido)

        # Si tiene padre (no es el nodo inicial), registrar la arista
        _, padre_nodo = costo_minimo[nodo_elegido]
        if padre_nodo is not None:
            aristas_mst.append((padre_nodo, nodo_elegido, peso_elegido))

        # Actualizar los costos de los nodos aún fuera del árbol
        for nombre_nodo in lista_nodos:
            if nombre_nodo in nodos_en_arbol:
                continue  # Ya está dentro, no necesita actualización

            # Distancia desde el nodo recién agregado hasta este candidato
            distancia_candidata: float = matriz_distancias[nodo_elegido].get(
                nombre_nodo, math.inf
            )

            costo_actual, _ = costo_minimo[nombre_nodo]
            if distancia_candidata < costo_actual:
                costo_minimo[nombre_nodo] = (distancia_candidata, nodo_elegido)

    # --- Construir el GrafoLogico del MST ---
    grafo_mst = GrafoLogico()

    # Agregar todos los nodos con sus coordenadas y roles originales
    for nombre_nodo in lista_nodos:
        latitud, longitud = grafo_original.coordenadas[nombre_nodo]
        rol_nodo = grafo_original.roles.get(nombre_nodo, "normal")
        grafo_mst.agregarNodo(nombre_nodo, latitud, longitud, role=rol_nodo)

    # Agregar solo las aristas que forman el MST (bidireccionales)
    for nodo_origen, nodo_destino, peso_arista in aristas_mst:
        grafo_mst.agregarArista(
            nodo_origen, nodo_destino, peso_arista, bidireccional=True
        )

    return grafo_mst
