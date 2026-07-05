"""
Modelos Pydantic usados por los endpoints de FastAPI.
Mantenerlos separados facilita reutilizarlos entre routers y testear
la validación de datos sin levantar el servidor.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class Point(BaseModel):
    lat: float
    lng: float


class GraphBuildRequest(BaseModel):
    place_name: str = Field(..., description="Ej: 'Chía, Cundinamarca, Colombia'")
    network_type: str = Field("drive", description="drive | walk | bike | all")


class DepotDeliveryRequest(BaseModel):
    depot: Point
    deliveries: List[Point]


class ShortestPathRequest(BaseModel):
    origin: Point
    destination: Point


class ColoringRequest(BaseModel):
    depot: Point
    deliveries: List[Point]
    n_colors: Optional[int] = Field(
        None, description="Si es None, se usa el mínimo necesario del coloreado voraz"
    )
    balance: bool = Field(True, description="Si True, rebalancea carga entre zonas")


class ZoneRouteRequest(BaseModel):
    depot: Point
    deliveries: List[Point]
    n_colors: Optional[int] = None
    balance: bool = True
    tsp_method: str = Field("nn_2opt", description="nn_2opt | exact (solo instancias pequeñas)")
