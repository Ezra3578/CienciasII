import math
from typing import Dict, List, Tuple
import numpy as np
from scipy.optimize import linear_sum_assignment

from FloydWarshall import FloydWarshall


def calcular_zonas_y_tamanos( n_direcciones: int, max_nodos_por_zona: int,) -> Tuple[int, List[int]]:
    if max_nodos_por_zona <= 0:
        raise ValueError("max_nodos_por_zona debe ser mayor a 0.")
    if n_direcciones < 0:
        raise ValueError("n_deliveries no puede ser negativo.")

    if n_direcciones == 0:
        return 0, []

    n_zonas = math.ceil(n_direcciones / max_nodos_por_zona)

    base = n_direcciones // n_zonas
    resto = n_direcciones % n_zonas
    #arreglo de direcciones por grupo de direcciones
    tamano = [base + 1 if i < resto else base for i in range(n_zonas)]

    return n_zonas, tamano


def elegir_mejor_depot(matriz: Dict[str, Dict[str, float]], depots: List[str], nodo_referencia: str,) -> str:
    #nodo referencia es meiode del grupo
    candidatos = [(d, matriz[nodo_referencia][d]) for d in depots]
    #se asegura que haya ruta
    candidatos = [c for c in candidatos if c[1] != float("inf")]
    if not candidatos:
        raise ValueError(
            f"Ningun deposito tiene camino real hasta '{nodo_referencia}'; "
            "no se le puede asignar un deposito a esta zona."
        )
    return min(candidatos, key=lambda c: c[1])[0]


def nombrar_zonas(depot_por_zona: List[str]) -> List[str]:
    contador_por_depot: Dict[str, int] = {}
    nombres = []
    for depot in depot_por_zona:
        contador_por_depot[depot] = contador_por_depot.get(depot, 0) + 1
        nombres.append(f"{depot}_Zona_{contador_por_depot[depot]}")
    #arreglo de nombres de zonas
    return nombres


def grupos_balanceados(fw: FloydWarshall,
    tamano: List[int],
    depots: List[str],
    nodos: List[str] = None,
    n_iter: int = 100,
    seed: int = 42,
) -> Tuple[Dict[int, Dict[str, Dict[str, float]]], List[str]]:
    """
    Devuelve (grupos, depot_por_zona):
      - grupos: {indice_de_zona: matriz_de_adyacencia_de_la_zona}, con
        el deposito elegido ya replicado adentro.
      - depot_por_zona: lista de largo len(sizes), el deposito elegido
        para cada zona (mismo orden que `sizes`).
    """
    matriz = fw.getMatrizDistancias()
    if nodos is None:
        nodos = fw.nodos
    n = len(nodos)
    k = len(tamano)

    if not depots:
        raise ValueError("Se necesita al menos un deposito en `depots`.")
    if sum(tamano) != n:
        raise ValueError(
            f"La suma de tamano ({sum(tamano)}) debe ser igual a la cantidad de nodos a agrupar ({n})."
        )

    def dist(a: str, b: str) -> float:
        return matriz[a][b]

    #meiodes al azar
    rng = np.random.default_rng(seed)
    medoides = [nodos[i] for i in rng.choice(n, k, replace=False)]

    assign = None
    pasos_realizados = 0
    espacios_total = sum(tamano)

    for _ in range(n_iter):
        pasos_realizados += 1

        #construye columnas con tamaños de zonas
        cost = np.zeros((n, espacios_total))
        col_to_grupo = []
        col = 0
        for g, cap in enumerate(tamano):
            #columnas con la distancia al meiode
            distancias_al_medoide = np.array([dist(p, medoides[g]) for p in nodos])
            for _ in range(cap):
                cost[:, col] = distancias_al_medoide
                col_to_grupo.append(g)
                col += 1

        #Algoritmo hungaro, minimo costo
        row_ind, col_ind = linear_sum_assignment(cost)
        nuevo_assign = np.zeros(n, dtype=int)
        #asignar dato a su columna correcta
        for r, c in zip(row_ind, col_ind):
            nuevo_assign[r] = col_to_grupo[c]

        #recalcular medoide, minimizanod distancia entre puntos
        nuevos_medoides = list(medoides)
        for g in range(k):
            miembros = [nodos[i] for i in range(n) if nuevo_assign[i] == g]
            if not miembros:
                continue
            costos = {m: sum(dist(m, o) for o in miembros) for m in miembros}
            nuevos_medoides[g] = min(costos, key=costos.get)

        # si no cambiaron los meoides, se corta despues de n_eteraciones
        if assign is not None and np.array_equal(nuevo_assign, assign):
            assign = nuevo_assign
            break

        assign = nuevo_assign
        medoides = nuevos_medoides

    # Buscamos el depot mas cercano a nuestro medoide , se crea matriz de adyacencia con el depot
    grupos: Dict[int, Dict[str, Dict[str, float]]] = {}
    depot_por_zona: List[str] = []
    for g in range(k):
        nodos_grupo = [nodos[i] for i in range(n) if assign[i] == g]
        depot = elegir_mejor_depot(matriz, depots, medoides[g])
        depot_por_zona.append(depot)

        todos = nodos_grupo if depot in nodos_grupo else nodos_grupo + [depot]
        grupos[g] = {
            n1: {n2: matriz[n1][n2] for n2 in todos if n2 != n1}
            for n1 in todos
        }

    return grupos, depot_por_zona, pasos_realizados


def zonificar(fw, depots, entregas, max_nodos_por_zona, n_iter=100, seed=42):
    n_zonas, tamano = calcular_zonas_y_tamanos(len(entregas), max_nodos_por_zona)
    if n_zonas == 0:
        return {}, []

    grupos, depot_por_zona,pasos_realizados = grupos_balanceados(
        fw, tamano, depots, nodos=entregas, n_iter=n_iter, seed=seed
    )
    nombres_zona = nombrar_zonas(depot_por_zona)

    matrices: Dict[str, Dict[str, Dict[str, float]]] = {}
    resumen: List[dict] = []
    for g in range(n_zonas):
        nombre = nombres_zona[g]
        depot = depot_por_zona[g]
        matriz_zona = grupos[g]
        entregas_zona = [nombre_nodo for nombre_nodo in matriz_zona.keys() if nombre_nodo != depot]

        matrices[nombre] = matriz_zona
        resumen.append({
            "nombre": nombre,
            "deposito": depot,
            "cantidad_entregas": len(entregas_zona),
            "cantidad_nodos": len(matriz_zona),
            "entregas": entregas_zona,
        })

    return matrices, resumen, pasos_realizados