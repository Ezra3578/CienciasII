from dataclasses import dataclass, field
from datetime import datetime
from threading import Lock
from typing import Optional
import uuid

from modules.graph.Grafo import Grafo


@dataclass
class SimulacionState:
    """Todo lo que vive durante el pipeline de una simulación (3 etapas)."""
    id: str
    grafo: Optional[Grafo] = None
    zonas: Optional[dict] = None      # resultado de la Etapa 2 (zoning)
    rutas: Optional[dict] = None      # resultado de la Etapa 3 (routing)
    creado_en: datetime = field(default_factory=datetime.utcnow)


class AppState:
    """
    Store en memoria para el estado del pipeline entre peticiones HTTP.
    es decir que se guarda el estado de cada etapa del grafo para que las siguientes etapas puedan acceder a él.
    Un único proceso, sin persistencia — si reinicias el server, se pierde todo.
    Si el día de mañana necesitas multi-worker o persistencia real, este es
    el único lugar que tocarías (cambiarlo por Redis, por ejemplo).
    """
    def __init__(self):
        self._simulaciones: dict[str, SimulacionState] = {}
        self._lock = Lock()

    def crear_simulacion(self) -> SimulacionState:
        sim_id = str(uuid.uuid4())
        with self._lock:
            sim = SimulacionState(id=sim_id)
            self._simulaciones[sim_id] = sim
        return sim

    def obtener(self, sim_id: str) -> SimulacionState:
        sim = self._simulaciones.get(sim_id)
        if sim is None:
            raise KeyError(f"No existe una simulación con id '{sim_id}'")
        return sim

    def actualizar_grafo(self, sim_id: str, grafo: Grafo) -> None:
        with self._lock:
            self.obtener(sim_id).grafo = grafo

    def actualizar_zonas(self, sim_id: str, zonas: dict) -> None:
        with self._lock:
            self.obtener(sim_id).zonas = zonas

    def actualizar_rutas(self, sim_id: str, rutas: dict) -> None:
        with self._lock:
            self.obtener(sim_id).rutas = rutas

    def eliminar(self, sim_id: str) -> None:
        with self._lock:
            self._simulaciones.pop(sim_id, None)


# Singleton real: una única instancia para todo el proceso de FastAPI
_app_state = AppState()


def get_app_state() -> AppState:
    """Dependency provider — esto se inyecta con Depends() en los routers."""
    return _app_state