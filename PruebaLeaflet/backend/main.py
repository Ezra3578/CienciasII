"""
Backend FastAPI. Orquesta las 3 etapas:
  1. /graph/build          -> construir grafo de Kamppi, Helsinki (OSMnx)
  2. /route/shortest       -> Dijkstra simple entre dos puntos
  3. /zones/build          -> coloreado de grafos -> zonas de reparto
  4. /zones/plan-routes    -> TSP heurístico dentro de cada zona + comparación

Ejecutar con:
    uvicorn main:app --reload --port 8000

Modo alterno de arranque (solo para visualización preliminar):
    python main.py --visualize
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from models import (
    GraphBuildRequest,
    ShortestPathRequest,
    ColoringRequest,
    ZoneRouteRequest,
)
import graph_service
import coloring_service
import routing_service

app = FastAPI(title="Delivery Zoning & Routing API")

# Permite que el front (servido en otro puerto durante desarrollo) consuma la API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en desarrollo; restringir en producción
    allow_methods=["*"],
    allow_headers=["*"],
)

#Solo se toma el network_type al ser estatica la región
STATE = {"network_type": None}


@app.post("/graph/build")
def build_graph(req: GraphBuildRequest):
    graph_service.build_graph(req.network_type)
    STATE["network_type"] = req.network_type
    return {"status": "ok", "place_name": graph_service.PLACE_NAME}


def _require_graph():
    if STATE["network_type"] is None:
        raise HTTPException(400, "Primero llama a /graph/build")
    return graph_service.get_graph(STATE["network_type"])


@app.post("/route/shortest")
def shortest_route(req: ShortestPathRequest):
    G = _require_graph()
    o_node = graph_service.nearest_node(G, req.origin.lat, req.origin.lng)
    d_node = graph_service.nearest_node(G, req.destination.lat, req.destination.lng)
    route, cost = graph_service.shortest_path(G, o_node, d_node, weight="weight")
    return {
        "geojson": graph_service.route_to_geojson(G, route),
        "distance_meters": cost,
    }


@app.post("/zones/build")
def build_zones(req: ColoringRequest):
    G = _require_graph()

    # Reseteamos roles de una petición anterior antes de marcar los
    # nuevos depot/deploy de esta petición.
    graph_service.reset_node_roles(G)

    depot_node = graph_service.nearest_node(G, req.depot.lat, req.depot.lng)
    graph_service.set_node_role(G, depot_node, "depot")

    delivery_nodes = [
        graph_service.nearest_node(G, p.lat, p.lng) for p in req.deliveries
    ]
    for node in delivery_nodes:
        graph_service.set_node_role(G, node, "deploy")

    dist_matrix = graph_service.distance_matrix(G, delivery_nodes, weight="weight")

    zones = coloring_service.build_zones(
        delivery_points=req.deliveries,
        delivery_nodes=delivery_nodes,
        distance_matrix=dist_matrix,
        n_colors=req.n_colors,
        balance=req.balance,
    )

    # Traduce índices de zona a coordenadas para que el front pinte los puntos.
    zones_coords = {
        str(color): [
            {"lat": req.deliveries[i].lat, "lng": req.deliveries[i].lng} for i in indices
        ]
        for color, indices in zones.items()
    }

    return {"depot_node": depot_node, "zones": zones_coords}


@app.post("/zones/plan-routes")
def plan_zone_routes(req: ZoneRouteRequest):
    G = _require_graph()

    graph_service.reset_node_roles(G)

    depot_node = graph_service.nearest_node(G, req.depot.lat, req.depot.lng)
    graph_service.set_node_role(G, depot_node, "depot")

    delivery_nodes = [
        graph_service.nearest_node(G, p.lat, p.lng) for p in req.deliveries
    ]
    for node in delivery_nodes:
        graph_service.set_node_role(G, node, "deploy")

    dist_matrix = graph_service.distance_matrix(G, delivery_nodes, weight="weight")

    zones = coloring_service.build_zones(
        delivery_points=req.deliveries,
        delivery_nodes=delivery_nodes,
        distance_matrix=dist_matrix,
        n_colors=req.n_colors,
        balance=req.balance,
    )

    results = {}
    for color, indices in zones.items():
        # Submatriz de distancias solo para los puntos de esta zona.
        # Se incluye el depot como "punto 0" virtual de cada zona para
        # que la ruta salga y regrese a él.
        zone_points = [req.depot] + [req.deliveries[i] for i in indices]
        zone_nodes = [depot_node] + [delivery_nodes[i] for i in indices]
        zone_matrix = graph_service.distance_matrix(G, zone_nodes, weight="weight")

        solution = routing_service.solve_zone_route(zone_matrix, depot_index=0)

        # Traduce índices locales de vuelta a coordenadas para el front.
        ordered_points = [
            {"lat": zone_points[idx].lat, "lng": zone_points[idx].lng}
            for idx in solution["route_indices"]
        ]

        results[str(color)] = {
            "ordered_points": ordered_points,
            "total_distance_meters": solution["total_distance"],
            "compute_time_seconds": solution["compute_time_seconds"],
            "method": solution["method"],
        }

    return {"zones": results}


# Sirve el front-end estático (index.html, app.js, style.css) directamente
# desde FastAPI, para no depender de un segundo servidor ni de CORS en
# producción. Comentar/ajustar esta línea si prefieres servir el front
# aparte (ej. con Live Server) durante desarrollo.
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")


# ======================================================================
# MÓDULO DE VISUALIZACIÓN (solo para desarrollo/depuración)
# ======================================================================
# Ejecutar con: python main.py --visualize
# pensado solo para inspeccionar visualmente el objeto grafo.

if __name__ == "__main__":
    import sys
    import graph_service as _gs
    import networkx as nx
    import json

    def graph_to_json(G):
        # Convierte el grafo a formato node-link
        data = nx.node_link_data(G)

        # Recorre nodos y aristas para serializar geometrías
        for node in data["nodes"]:
            for k, v in list(node.items()):
                if hasattr(v, "coords"):  # geometrías shapely
                    node[k] = list(v.coords)

        for link in data["links"]:
            for k, v in list(link.items()):
                if hasattr(v, "coords"):
                    link[k] = list(v.coords)

        return data

    if "--visualize" in sys.argv:
        from graph_visualizer import show_graph_window
        G = _gs.build_graph()

        # Exportar grafo a JSON
        data = graph_to_json(G)
        with open("graph_export.json", "w") as f:
            json.dump(data, f, indent=2)

        print("✅ Grafo exportado a graph_export.json")
        show_graph_window(G)
    else:
        G = _gs.build_graph()
        data = graph_to_json(G)
        with open("graph_export.json", "w") as f:
            json.dump(data, f, indent=2)

        print("✅ Grafo exportado a graph_export.json")

        import uvicorn
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
