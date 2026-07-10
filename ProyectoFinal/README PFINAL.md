# Delivery Zoning & Routing (esqueleto)

Pipeline: **Dijkstra (OSMnx)** → **coloreado de grafos (zonas)** → **TSP heurístico por zona**.

## Estructura

```
delivery_project/
├── backend/
│   ├── main.py              # FastAPI: endpoints de las 3 etapas
│   ├── graph_service.py     # Etapa 1: grafo OSMnx + Dijkstra
│   ├── coloring_service.py  # Etapa 2: coloreado de grafos + balanceo
│   ├── routing_service.py   # Etapa 3: TSP heurístico (NN + 2-opt)
│   └── models.py            # Modelos Pydantic
├── frontend/
│   ├── index.html           # Mapa Leaflet + panel de control
│   ├── app.js                # Lógica: llamadas a la API, dibujo de zonas/rutas
│   └── style.css
├── requirements.txt
└── README.md
```

## Instalación

```bash
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución (versión actual del front, con `conexion.py` como stub)

El proyecto está en transición hacia el nuevo pipeline (Floyd-Warshall +
Monotone chain + Dijkstra anidado). Por ahora el backend real de ese
pipeline **no** está implementado; `conexion.py` es un stub que solo
recibe lo que manda el front, lo imprime por consola, y responde
`{"mensaje": "en trabajo"}`. Úsalo así mientras se desarrollan los
algoritmos:

```bash
cd backend
uvicorn conexion:app --reload --port 8000
```

Luego abre `frontend/index.html` en el navegador (o sírvelo con
Live Server / `python -m http.server` desde `frontend/`). El front está
fijado al barrio de Kamppi, Helsinki, Finlandia.

> Nota: `main.py` (el pipeline anterior con OSMnx + coloreado clásico +
> TSP) sigue existiendo tal cual, pero no está conectado al front actual.
> No corras `main.py` y `conexion.py` al mismo tiempo en el puerto 8000.

## Flujo de uso en la interfaz

1. Pulsa **"1. Construir grafo (Kamppi)"** — llama a `/grafo/construir`
   (por ahora solo confirma la solicitud; a futuro descargará la red vial
   de Kamppi con OSMnx).
2. Coloca nodos directamente en el mapa (limitado a Kamppi; se puede
   hacer zoom pero no desplazar la vista fuera del barrio):
   - **Clic izquierdo** → nodo de entrega (numerado 1, 2, 3...).
   - **Ctrl + clic izquierdo** → depot (nombrado A, B, C...). No se
     permite colocar un depot a menos de 350 m de otro ya existente.
     Mientras mantienes Ctrl presionado, se ven en azul claro los radios
     de 350 m de los depots ya puestos.
   - **Clic derecho** sobre un nodo → lo elimina.
3. Pulsa **"2. Construir zonas"** — llama a `/zonas/construir` con todos
   los nodos y la distancia máxima de agrupamiento. A futuro: Floyd-Warshall
   para distancias entre todos los nodos, agrupamiento y Monotone chain
   para el convex hull de cada zona.
4. Pulsa **"3. Planificar rutas"** — llama a `/rutas/planificar` con todos
   los nodos. A futuro: Dijkstra anidado dentro de cada zona y métricas de
   carga por zona.

### Formato de datos enviado al backend

```json
{
  "1": { "tipo_nodo": "entrega", "longitud": 24.9312, "latitud": 60.1690 },
  "2": { "tipo_nodo": "entrega", "longitud": 24.9325, "latitud": 60.1683 },
  "A": { "tipo_nodo": "depot",   "longitud": 24.9300, "latitud": 60.1678 }
}
```

## Próximos pasos sugeridos

- **Balanceo de carga más robusto**: reemplazar `rebalance_colors`
  (heurística local simple) por un modelo de OR-Tools (CP-SAT) si el
  balanceo es un requisito estricto de evaluación.
- **Comparar heurísticas de TSP**: añadir `python-tsp` (recocido
  simulado) como referencia frente a NN+2-opt, y mostrar ambos tiempos
  en la tabla de resultados.
- **Persistir el grafo**: guardar con `ox.save_graphml()` para no
  re-descargar en cada reinicio del servidor durante desarrollo.
- **Autenticación/CORS**: restringir `allow_origins` en `main.py`
  antes de cualquier despliegue fuera de localhost.
