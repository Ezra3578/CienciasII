"""
schemas_zonas.py
----------------
Modelos Pydantic de la respuesta del endpoint /process (versión MST + BFS).

La respuesta es un dict donde cada llave es el nombre de un depot y
el valor es un objeto ZonaResponse con:
  - frontera: lista de nodos que forman el borde de la zona
  - ruta: lista ordenada de nodos que define la ruta de recorrido
          dentro de la zona

Cada nodo se representa con su nombre, longitud y latitud.
"""

from pydantic import BaseModel
from typing import Dict, List


class NodoCoord(BaseModel):
    """Representa un nodo con su nombre y coordenadas geográficas."""
    nombre: str
    longitud: float
    latitud: float


class regionData(BaseModel):
    """
    Respuesta de una zona individual:
      - frontera: nodos que delimitan el borde de la zona
      - ruta: orden de visita de los nodos dentro de la zona
    """
    frontera: List[NodoCoord]
    ruta: List[NodoCoord]


# FastAPI acepta un Dict como response_model directamente,
# no necesitamos envolverlo en otro BaseModel con __root__.
ProcessResponse = Dict[str, regionData]
