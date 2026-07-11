"""
main.py
-------
Servidor FastAPI de ProyectoFinal (antes vivía en conexion.py; se
renombró a main.py, que es la convención estándar de entry point).

Se levanta con:
    uvicorn main:app --reload --port 8000

Recibe una lista de nodos (depots y deliveries) y responde con:
  - convex_hulls: por cada depot, el polígono (lista de {lat, lng}) que
    envuelve al depot y sus entregas asignadas, para pintar la zona en
    el mapa.
  - routes: por cada depot, la ruta real (GeoJSON LineString, siguiendo
    calles) hacia cada una de sus entregas asignadas, calculada
    corriendo el Dijkstra manual (Dijkstra.py) sobre el grafo de
    negocio (graph_adapter.GrafoLogico), apoyado en la red vial real de
    graph_service.py (Kamppi, Helsinki).

Asignación depot -> delivery: cada delivery se asigna a su depot más
cercano por distancia real de red vial (no en línea recta).

También expone un modo de demostración por consola, sin servidor (ver
el bloque MODO DEMO al final del archivo):
    python main.py --demo
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from shapely.geometry import MultiPoint

import graph_service
from graph_adapter import GrafoLogico
from Dijkstra import Dijkstra

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Node(BaseModel):
    name: str
    type: str          # "depot" o "delivery"
    longitude: float
    latitude: float


class RequestData(BaseModel):
    nodes: List[Node]


@app.on_event("startup")
def _cargar_grafo_al_iniciar():
    """
    Pre-descarga y cachea la red vial de Kamppi al levantar el servidor,
    para que la primera petición a /process no tenga que esperar la
    descarga de OSMnx.
    """
    graph_service.build_graph()


def _asignar_depot_mas_cercano(grafo: GrafoLogico, depots: List[Node], deliveries: List[Node]):
    """
    Para cada delivery, busca a qué depot está más cerca por red vial
    real (usando las aristas que ya conectó conectar_depots_con_entregas).
    Retorna (asignacion, sin_asignar):
      - asignacion: {nombre_depot: [nombres_delivery, ...]}
      - sin_asignar: [nombres_delivery sin ruta a ningún depot]
    """
    asignacion = {d.name: [] for d in depots}
    sin_asignar = []

    for entrega in deliveries:
        mejor_depot = None
        mejor_distancia = None
        for depot in depots:
            distancia = grafo.aristas.get(depot.name, {}).get(entrega.name)
            if distancia is None:
                continue
            if mejor_distancia is None or distancia < mejor_distancia:
                mejor_distancia = distancia
                mejor_depot = depot.name

        if mejor_depot is not None:
            asignacion[mejor_depot].append(entrega.name)
        else:
            sin_asignar.append(entrega.name)

    return asignacion, sin_asignar


def _convex_hull(grafo: GrafoLogico, nombres_nodos: List[str]):
    """
    Calcula el polígono (convex hull) de un conjunto de nodos lógicos.
    Devuelve una lista de {'lat':..., 'lng':...} en orden. Si no hay
    suficientes puntos (o están alineados) para formar un polígono real,
    devuelve los puntos tal cual, sin envolvente.
    """
    puntos = [grafo.coordenadas[n] for n in nombres_nodos]  # (lat, lon)
    if len(puntos) < 3:
        return [{"lat": lat, "lng": lon} for lat, lon in puntos]

    multipunto = MultiPoint([(lon, lat) for lat, lon in puntos])  # shapely usa (x=lon, y=lat)
    hull = multipunto.convex_hull

    if hull.geom_type != "Polygon":
        return [{"lat": lat, "lng": lon} for lat, lon in puntos]

    return [{"lat": y, "lng": x} for x, y in hull.exterior.coords]


@app.get("/graph/data")
def get_graph_data():
    """
    Devuelve el grafo vial completo de Kamppi en formato node-link JSON,
    para que el frontend pueda dibujar la malla base de calles.
    """
    G = graph_service.get_graph()
    return graph_service.graph_to_json(G)


@app.post("/process")
async def process_data(data: RequestData):
    depots = [n for n in data.nodes if n.type == "depot"]
    deliveries = [n for n in data.nodes if n.type == "delivery"]

    if not depots:
        raise HTTPException(400, "Se necesita al menos un nodo tipo 'depot'.")

    # Grafo de negocio (temporal, solo para este request) sobre la red
    # vial compartida de Kamppi, Helsinki.
    grafo = GrafoLogico()

    for depot in depots:
        grafo.agregarNodo(depot.name, depot.latitude, depot.longitude, role="depot")
    for entrega in deliveries:
        grafo.agregarNodo(entrega.name, entrega.latitude, entrega.longitude, role="deploy")

    grafo.conectar_depots_con_entregas(
        [d.name for d in depots], [e.name for e in deliveries]
    )

    asignacion, sin_asignar = _asignar_depot_mas_cercano(grafo, depots, deliveries)

    dijkstra = Dijkstra(grafo)

    convex_hulls = {}
    routes = {}

    for depot in depots:
        entregas_asignadas = asignacion[depot.name]

        # --- convex hull de esta zona (depot + sus entregas) ---
        puntos_zona = [depot.name] + entregas_asignadas
        convex_hulls[depot.name] = _convex_hull(grafo, puntos_zona)

        # --- rutas reales (por calles) desde el depot a cada entrega ---
        rutas_depot = []
        for nombre_entrega in entregas_asignadas:
            camino_logico = dijkstra.getCaminoLista(depot.name, nombre_entrega)
            if not camino_logico:
                continue

            # Traduce el camino lógico a una ruta real continua sobre la
            # red vial, tramo a tramo (evita duplicar el nodo de unión).
            nodos_reales = []
            for i in range(len(camino_logico) - 1):
                tramo = grafo.ruta_real(camino_logico[i], camino_logico[i + 1])
                if not tramo:
                    continue
                nodos_reales.extend(tramo if not nodos_reales else tramo[1:])

            if not nodos_reales:
                continue

            geojson = graph_service.route_to_geojson(grafo.red_vial, nodos_reales)
            distancia_metros = dijkstra.distancias_por_origen[depot.name][nombre_entrega]

            rutas_depot.append({
                "delivery": nombre_entrega,
                "geojson": geojson,
                "distancia_metros": distancia_metros,
            })

        routes[depot.name] = rutas_depot

    return {
        "status": "ok",
        "convex_hulls": convex_hulls,
        "routes": routes,
        "sin_asignar": sin_asignar,
    }


# ======================================================================
# MODO DEMO (solo consola, sin servidor)
# ======================================================================
# Ejecutar con: python main.py --demo
# Corre Dijkstra.py sobre un ejemplo fijo (un depot, dos entregas) y
# grafica el camino más corto encontrado con matplotlib. No inicia el
# servidor FastAPI; es solo para probar/depurar el flujo desde consola.
def _demo_dibujar_camino(grafo: GrafoLogico, camino_nodos, titulo="Ruta calculada con Dijkstra", guardar_como=None):
    import matplotlib
    matplotlib.use("Agg")  # cambia a "TkAgg" si tienes entorno gráfico local
    import matplotlib.pyplot as plt
    import osmnx as ox

    fig, ax = ox.plot_graph(
        grafo.red_vial, show=False, close=False,
        node_size=0, edge_color="#cccccc", edge_linewidth=0.7,
        bgcolor="white", figsize=(11, 11),
    )

    for nombre, (lat, lon) in grafo.coordenadas.items():
        ax.scatter(lon, lat, c="#888888", s=40, zorder=3)
        ax.annotate(nombre, (lon, lat), fontsize=8, color="#555555",
                    xytext=(3, 3), textcoords="offset points")

    for i in range(len(camino_nodos) - 1):
        ruta = grafo.ruta_real(camino_nodos[i], camino_nodos[i + 1])
        if not ruta:
            continue
        xs = [grafo.red_vial.nodes[n]["x"] for n in ruta]
        ys = [grafo.red_vial.nodes[n]["y"] for n in ruta]
        ax.plot(xs, ys, c="red", linewidth=3, zorder=4)

    for idx, nombre in enumerate(camino_nodos):
        lat, lon = grafo.coordenadas[nombre]
        color = "green" if idx == 0 else ("blue" if idx == len(camino_nodos) - 1 else "orange")
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

def _demo_exportar_json(grafo: GrafoLogico, ruta_salida: str = "grafo_demo.json"):
    """
    Vuelca el grafo vial completo (mismo formato que /graph/data) a un
    archivo JSON, y además imprime en consola solo los nodos reales
    anclados a los puntos lógicos agregados en la demo, anotados con su
    rol (depot/deploy). El rol se lee de grafo.roles (por instancia),
    no del grafo compartido -- ver la nota en graph_adapter.py.
    """
    import json

    data = graph_service.graph_to_json(grafo.red_vial)
    n_aristas = len(data.get("links", data.get("edges", [])))

    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Grafo completo guardado en: {ruta_salida} "
          f"({len(data['nodes'])} nodos, {n_aristas} aristas)")

    # id del nodo real -> nombre lógico (Bodega_Central, Cliente_1, ...)
    id_a_nombre = {nid: nombre for nombre, nid in grafo.nodo_osmnx.items()}

    nodos_interes = []
    for n in data["nodes"]:
        nombre = id_a_nombre.get(n["id"])
        if nombre is None:
            continue
        n = dict(n)  # copia: no mutar el JSON completo ya guardado
        n["node_type"] = grafo.roles.get(nombre, "normal")
        n["nombre_logico"] = nombre
        nodos_interes.append(n)

    print("\nNodos reales anclados a los puntos lógicos de la demo:")
    print(json.dumps(nodos_interes, indent=2, ensure_ascii=False))


def _demo():
    grafo = GrafoLogico()

    grafo.agregarNodo("Bodega_Central", lat=60.1673, lon=24.9308, role="depot")
    grafo.agregarNodo("Cliente_1", lat=60.1660, lon=24.9330, role="deploy")
    grafo.agregarNodo("Cliente_2", lat=60.1690, lon=24.9280, role="deploy")

    grafo.conectar_depots_con_entregas(["Bodega_Central"], ["Cliente_1", "Cliente_2"])

    dijkstra = Dijkstra(grafo)

    punto_despacho = "Bodega_Central"
    punto_entrega = "Cliente_2"

    print(dijkstra.getDistancia(punto_despacho, punto_entrega))
    print(dijkstra.getCamino(punto_despacho, punto_entrega))
    print(f"Pasos realizados por el algoritmo: {dijkstra.getPasos()}")

    
    camino = dijkstra.getCaminoLista(punto_despacho, punto_entrega)
    if camino:
        _demo_dibujar_camino(
            grafo, camino,
            titulo=f"Ruta más corta: {punto_despacho} -> {punto_entrega}",
            guardar_como="ruta_dijkstra.png",
        )
    else:
        print("No se encontró un camino para graficar.")

    #Exporta el json con la información del grafo completo y los nodos de interés de la demo
    _demo_exportar_json(grafo)

if __name__ == "__main__":
    import sys

    if "--demo" in sys.argv:
        _demo()
    else:
        import uvicorn

        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)