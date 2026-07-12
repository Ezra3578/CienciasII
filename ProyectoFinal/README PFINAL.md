# Delivery Zoning & Routing (esqueleto)

Backend que recibe depots y puntos de entrega sobre el barrio de
**Kamppi, Helsinki, Finlandia** (región fija del proyecto) y calcula:

- **Zonas de reparto**: cada entrega se asigna a su depot más cercano
  por distancia real de red vial (no en línea recta), y se calcula el
  polígono (convex hull) que envuelve a cada depot con sus entregas.
- **Rutas**: el camino más corto (por calles) de cada depot a cada una
  de sus entregas asignadas, corriendo una implementación propia de
  Dijkstra sobre un grafo de negocio construido encima de la red vial
  real (OSMnx).

## Estructura

```
ProyectoFinal/
├── backend/
│   ├── main.py              # Entry point FastAPI(endpoints) + modo demo por consola
│   ├── graph_service.py     # Red vial compartida (OSMnx, Kamppi): descarga, cache, Dijkstra base
│   ├── graph_adapter.py     # Grafo de negocio por request (depot/delivery), apoyado en graph_service.py
│   ├── Dijkstra.py          # Implementación propia del algoritmo (no usa el Dijkstra de networkx)
│   ├── graph_visualizer.py  # Visualización aparte del grafo completo (ventana Tkinter o PNG si es headless)
│   └── requirements.txt
├── frontend/
│   ├── index.html           # Mapa Leaflet + panel de control, fijado a Kamppi
│   ├── app.js                # Llamadas a la API, dibujo de nodos/zonas/rutas
│   └── style.css
└── README.md
```
> `graph_service.py` es el único que descarga y cachea la red vial
> (un singleton en memoria, compartido por todos los requests).
> `graph_adapter.py` crea una instancia nueva por cada request con los
> depots/entregas de esa petición — nunca modifica el grafo compartido.

## Instalación

```bash
cd ProyectoFinal
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```

## Ejecución

```bash
# servidor 
cd backend
uvicorn main:app --reload --port 8000

# otro comando que corre el servidor
python main.py

#demo por consola (Dijkstra + gráfico), sin servidor
python main.py --demo

# visualizador del grafo completo (aparte, sin cambios)
python graph_visualizer.py
```

En otra terminal, sirve el frontend:

```bash
cd ProyectoFinal/frontend
python -m http.server 8080
```


Abre `http://localhost:8080` — el front está fijado al barrio de
Kamppi, Helsinki (no se puede desplazar el mapa fuera de esa zona).

Para limpiar procesos colgados en el puerto del backend:

```bash
lsof -i :8000
fuser -k 8000/tcp || true
```

## Endpoints

### `POST /process`

Recibe los nodos colocados en el mapa y devuelve zonas + rutas.

**Request:**
```json
{
  "nodes": [
    { "name": "A", "type": "depot",    "longitude": 24.9300, "latitude": 60.1678 },
    { "name": "1", "type": "delivery", "longitude": 24.9312, "latitude": 60.1690 },
    { "name": "2", "type": "delivery", "longitude": 24.9325, "latitude": 60.1683 }
  ]
}
```

**Response:**
```json
{
  "status": "ok",
  "convex_hulls": {
    "A": [ { "lat": 60.1678, "lng": 24.9300 }, "..." ]
  },
  "routes": {
    "A": [
      {
        "delivery": "1",
        "geojson": { "type": "Feature", "geometry": { "type": "LineString", "coordinates": ["..."] } },
        "distancia_metros": 484.37
      }
    ]
  },
  "sin_asignar": []
}
```

`sin_asignar` lista las entregas que no tenían camino a ningún depot
(red vial desconectada entre esos puntos), en vez de romper la
respuesta completa.

### `GET /graph/data`

Devuelve el grafo vial completo de Kamppi en formato node-link JSON
(nodos y aristas de OSMnx, con `node_type` y el resto de atributos ya
saneados para ser serializables), para que el front pueda dibujar la
malla de calles como mapa base. Puede pesar varios MB.

## Flujo de uso en la interfaz

1. Coloca nodos directamente en el mapa (limitado a Kamppi):
   - **Clic izquierdo** → punto de entrega.
   - **Ctrl + clic izquierdo** → depot.
   - **Clic derecho** sobre un nodo → lo elimina.
2. Pulsa el botón de procesar — llama a `POST /process` con todos los
   nodos actuales.
3. El front dibuja los polígonos de zona (`convex_hulls`) y las rutas
   reales (`routes`) que devuelve el backend.

## Notas de diseño

- El rol de cada nodo (`depot`/`deploy`) se guarda **por request**, en
  la instancia de `GrafoLogico` (`graph_adapter.py`), nunca en el
  grafo compartido de `graph_service.py` — evita que dos requests
  concurrentes se pisen el estado.
- El grafo de negocio conecta solo **depot ↔ entrega** (bipartito); no
  hay aristas entrega↔entrega ni depot↔depot, porque `Dijkstra.py` no
  las necesita para este flujo.
- La asignación entrega→depot es por **distancia real de red vial**
  más corta, calculada con el Dijkstra de `networkx` sobre la red vial
  completa (`graph_service.py`), no con el Dijkstra manual (ese se usa
  solo dentro del grafo de negocio bipartito, ya reducido).
