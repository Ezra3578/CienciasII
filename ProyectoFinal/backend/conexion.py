from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

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

class Node(BaseModel):
    name: str
    type: str          # "depot" o "delivery"
    longitude: float
    latitude: float

class RequestData(BaseModel):
    nodes: List[Node]

@app.get("/")
async def root():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/process")
async def process_data(data: RequestData):
    print("Nodos recibidos:")
    for node in data.nodes:
        print(f"  {node.name} ({node.type}): lon={node.longitude}, lat={node.latitude}")

    # Respuesta provisional
    return {
        "status": "en trabajo",
        "convex_hulls": {},
        "routes": {}
    }

app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")