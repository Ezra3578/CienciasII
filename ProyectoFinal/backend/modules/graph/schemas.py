from shared.schemas import NodoInput
from pydantic import BaseModel

class GrafoConstruirRequest(BaseModel):
    max_nodos: int
    nodos: dict[str, NodoInput]   # el dict que manda el front, ya validado

class GrafoConstruirResponse(BaseModel):
    grafo_id: str
    total_nodos: int
    total_depots: int
    total_entregas: int