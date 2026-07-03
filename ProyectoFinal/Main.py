"""
Main.py
-------
Ejemplo de uso de Grafo.py + Dijkstra.py sobre la red vial real de
Madrid, Cundinamarca, Colombia (obtenida con osmnx).

Flujo:
    1. Crear el grafo (descarga la red vial real desde OpenStreetMap).
    2. Agregar los puntos de despacho y los puntos de entrega (nodos lógicos).
    3. Conectar esos puntos con aristas (peso manual o distancia real automática).
    4. Ejecutar Dijkstra entre un punto de despacho y un punto de entrega.
    5. Mostrar el resultado en texto y graficar el camino sobre el mapa real.
"""

from Grafo import Grafo
from Dijkstra import Dijkstra


def main():
    # 1) Crear el grafo con la red vial de Madrid, Cundinamarca
    grafo = Grafo(lugar="Madrid, Cundinamarca, Colombia", network_type="drive")

    # 2) ---------------------------------------------------------------
    #    PUNTOS DE DESPACHO
    #    Agrega aquí tus bodegas / centros de despacho. Si conoces las
    #    coordenadas exactas pásalas (es más confiable que geocodificar un
    #    nombre inventado); si el nombre es una dirección real, puedes omitir
    #    lat/lon y se geocodifica automáticamente.
    # --------------------------------------------------------------------
    grafo.agregarNodo("Bodega_Central", lat=4.7331, lon=-74.2666)     # centro de Madrid, Cund.
    grafo.agregarNodo("Centro_Despacho_2", lat=4.7280, lon=-74.2590)

    # PUNTOS DE ENTREGA
    grafo.agregarNodo("Cliente_1", lat=4.7395, lon=-74.2620)
    grafo.agregarNodo("Cliente_2", lat=4.7250, lon=-74.2720)
    grafo.agregarNodo("Cliente_3", lat=4.7360, lon=-74.2540)

    # 3) ---------------------------------------------------------------
    #    ARISTAS
    #    Opción A: peso manual, tal como en la interfaz original:
    #       grafo.agregarArista("Bodega_Central", "Cliente_1", 10)
    #    Opción B (la que se usa aquí): peso = distancia real en metros
    #       siguiendo la red vial, calculada automáticamente.
    # --------------------------------------------------------------------
    grafo.agregarAristaAutomatica("Bodega_Central", "Cliente_1", bidireccional=True)
    grafo.agregarAristaAutomatica("Bodega_Central", "Cliente_2", bidireccional=True)
    grafo.agregarAristaAutomatica("Bodega_Central", "Centro_Despacho_2", bidireccional=True)
    grafo.agregarAristaAutomatica("Centro_Despacho_2", "Cliente_2", bidireccional=True)
    grafo.agregarAristaAutomatica("Centro_Despacho_2", "Cliente_3", bidireccional=True)
    grafo.agregarAristaAutomatica("Cliente_1", "Cliente_3", bidireccional=True)

    # 4) ---------------------------------------------------------------
    #    DIJKSTRA: un punto de despacho -> un punto de entrega
    # --------------------------------------------------------------------
    dijkstra = Dijkstra(grafo)

    punto_despacho = "Bodega_Central"
    punto_entrega = "Cliente_3"

    print(dijkstra.getDistancia(punto_despacho, punto_entrega))
    print(dijkstra.getCamino(punto_despacho, punto_entrega))
    print(f"Pasos realizados por el algoritmo: {dijkstra.getPasos()}")

    # 5) ---------------------------------------------------------------
    #    GRAFICAR EL CAMINO ENCONTRADO SOBRE EL MAPA REAL
    # --------------------------------------------------------------------
    camino = dijkstra.getCaminoLista(punto_despacho, punto_entrega)
    if camino:
        grafo.dibujar_camino(
            camino,
            titulo=f"Ruta más corta: {punto_despacho} -> {punto_entrega}",
            guardar_como="ruta_dijkstra.png",
        )
    else:
        print("No se encontró un camino para graficar.")


if __name__ == "__main__":
    main()
