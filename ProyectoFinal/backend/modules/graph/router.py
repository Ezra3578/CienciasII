from core.state import AppState, get_app_state
from fastapi import APIRouter, Depends
from .schemas import GrafoConstruirRequest, GrafoConstruirResponse
from .service import GraphService

router = APIRouter(prefix="/grafo", tags=["grafo"])
service = GraphService()

@router.post("/construir", response_model=GrafoConstruirResponse)
def construir_grafo(req: GrafoConstruirRequest, state: AppState = Depends(get_app_state)):
    return service.construir(req, state)