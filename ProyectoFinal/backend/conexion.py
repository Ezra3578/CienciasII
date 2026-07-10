from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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