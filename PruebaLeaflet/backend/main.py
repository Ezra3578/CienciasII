"""
Backend FastAPI. Orquesta las 3 etapas:
  1. /graph/build          -> construir grafo de la ciudad (OSMnx)
  2. /route/shortest       -> Dijkstra simple entre dos puntos
  3. /zones/build          -> coloreado de grafos -> zonas de reparto
  4. /zones/plan-routes    -> TSP heurístico dentro de cada zona + comparación

Ejecutar con:
    uvicorn main:app --reload --port 8000
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

# Estado simple en memoria: qué ciudad está activa. Para un proyecto
# académico basta; en un sistema real esto viajaría en cada request
# o se guardaría por sesión/usuario.
STATE = {"place_name": None, "network_type": "drive"}


@app.post("/graph/build")
def build_graph(req: GraphBuildRequest):
    graph_service.build_graph(req.place_name, req.network_type)
    STATE["place_name"] = req.place_name
    STATE["network_type"] = req.network_type
    return {"status": "ok", "place_name": req.place_name}


def _require_graph():
    if STATE["place_name"] is None:
        raise HTTPException(400, "Primero llama a /graph/build")
    return graph_service.get_graph(STATE["place_name"], STATE["network_type"])


@app.post("/route/shortest")
def shortest_route(req: ShortestPathRequest):
    G = _require_graph()
    o_node = graph_service.nearest_node(G, req.origin.lat, req.origin.lng)
    d_node = graph_service.nearest_node(G, req.destination.lat, req.destination.lng)
    route, cost = graph_service.shortest_path(G, o_node, d_node, weight="length")
    return {
        "geojson": graph_service.route_to_geojson(G, route),
        "distance_meters": cost,
    }


@app.post("/zones/build")
def build_zones(req: ColoringRequest):
    G = _require_graph()

    depot_node = graph_service.nearest_node(G, req.depot.lat, req.depot.lng)
    delivery_nodes = [
        graph_service.nearest_node(G, p.lat, p.lng) for p in req.deliveries
    ]

    dist_matrix = graph_service.distance_matrix(G, delivery_nodes, weight="length")

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

    depot_node = graph_service.nearest_node(G, req.depot.lat, req.depot.lng)
    delivery_nodes = [
        graph_service.nearest_node(G, p.lat, p.lng) for p in req.deliveries
    ]

    dist_matrix = graph_service.distance_matrix(G, delivery_nodes, weight="length")

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
        zone_matrix = graph_service.distance_matrix(G, zone_nodes, weight="length")

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
