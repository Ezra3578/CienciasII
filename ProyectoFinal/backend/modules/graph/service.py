from core.state import AppState
from .Grafo import Grafo
from .schemas import GrafoConstruirRequest, GrafoConstruirResponse

class GraphService:
    def construir(self, req: GrafoConstruirRequest, state: AppState) -> GrafoConstruirResponse:
        grafo = Grafo(lugar="La Candelaria, Bogotá, Colombia", network_type="drive")
        for nombre, nodo in req.nodos.items():
            grafo.agregarNodo(nombre, nodo.tipo_nodo, lat=nodo.latitud, lon=nodo.longitud)

        # Guarda el grafo en el estado de la simulación por id para que las siguientes etapas puedan acceder a él.
        simulacion = state.crear_simulacion()
        state.actualizar_grafo(simulacion.id, grafo)

        return GrafoConstruirResponse(
            grafo_id=simulacion.id,
            total_nodos=len(grafo.getMatriz()),
            total_depots=len(grafo.getDepositos()),
            total_entregas=len(grafo.getEntregas()),
        )