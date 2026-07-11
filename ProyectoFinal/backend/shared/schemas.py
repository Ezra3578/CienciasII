# shared/schemas.py — esto SÍ es transversal: zoning y routing también reciben nodos
from pydantic import BaseModel
from typing import Literal

class NodoInput(BaseModel):
    tipo_nodo: Literal["entrega", "depot"]
    longitud: float
    latitud: float