from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NodoData(BaseModel):
    tipo_nodo: str
    longitud: float
    latitud: float

class RequestData(BaseModel):
    max_nodos: int
    nodos: Dict[str, NodoData]

@app.get("/")
async def root():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/process")
async def process_data(data: RequestData):
    print(f"Máximo de nodos por zona: {data.max_nodos}")
    print("Nodos recibidos:")
    for nombre, nodo in data.nodos.items():
        print(f"  {nombre} ({nodo.tipo_nodo}): lon={nodo.longitud}, lat={nodo.latitud}")

    # Respuesta provisional
    return {
        "status": "en trabajo",
        "convex_hulls": {},
        "routes": {}
    }

app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")