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

## Ejecución

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Luego abre `http://127.0.0.1:8000` en el navegador (FastAPI sirve el
frontend directamente gracias al `StaticFiles` montado en `main.py`).

## Flujo de uso en la interfaz

1. Escribe el nombre de la ciudad/zona (ej. `"Chía, Cundinamarca, Colombia"`)
   y pulsa **"Construir grafo"**. OSMnx descargará la red vial desde OSM
   (puede tardar según el tamaño del área).
2. Haz clic en el mapa: el **primer clic** marca el depot, los
   **siguientes clics** marcan puntos de entrega.
3. Pulsa **"Colorear / crear zonas"**: llama a `/zones/build`, que
   construye un grafo de conflicto entre entregas cercanas y aplica
   coloreado voraz de NetworkX + rebalanceo de carga.
4. Pulsa **"Planificar rutas por zona"**: llama a `/zones/plan-routes`,
   que corre Dijkstra repetido para la matriz de distancias de cada
   zona y resuelve un TSP heurístico (vecino más cercano + 2-opt)
   dentro de cada una. Se muestra la ruta coloreada por zona y una
   tabla comparativa de distancia/tiempo de cómputo.

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
