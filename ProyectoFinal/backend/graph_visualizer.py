"""
Módulo de visualización del grafo vial (apoyo para desarrollo).

No forma parte del servidor FastAPI: es una herramienta para confirmar
visualmente que el grafo de Kamppi se construyó bien y que los nodos
depot/deploy quedaron marcados donde corresponde (inicialmente como tipo normal)

Uso:
    python graph_visualizer.py
o bien:
    python main.py --visualize
"""

import os
import sys

import matplotlib
import networkx as nx
import osmnx as ox

NODE_TYPE_COLORS = {
    "normal": "#3B82F6",  # azul
    "depot": "#DC2626",   # rojo
    "deploy": "#16A34A",  # verde
}

# --- Detección de entorno gráfico ---
# En Linux, sin la variable DISPLAY (y sin WAYLAND_DISPLAY) no hay
# servidor X al que dibujarle una ventana; en Windows/Mac se asume que
# sí hay entorno gráfico salvo que se fuerce lo contrario.
HAS_DISPLAY = (
    sys.platform.startswith("win")
    or sys.platform == "darwin"
    or bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
)

if HAS_DISPLAY:
    matplotlib.use("TkAgg")
else:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402  (después de matplotlib.use)


def _node_colors(G: nx.MultiDiGraph) -> list:
    return [
        NODE_TYPE_COLORS.get(G.nodes[n].get("node_type", "normal"), "#3B82F6")
        for n in G.nodes
    ]


def _node_sizes(G: nx.MultiDiGraph) -> list:
    return [
        18 if G.nodes[n].get("node_type", "normal") != "normal" else 4
        for n in G.nodes
    ]


def build_figure(G: nx.MultiDiGraph):
    fig, ax = ox.plot_graph(
        G,
        node_color=_node_colors(G),
        node_size=_node_sizes(G),
        edge_color="#9CA3AF",
        edge_linewidth=0.6,
        bgcolor="white",
        show=False,
        close=False,
    )
    ax.set_title("Grafo vial - Kamppi, Helsinki (rojo=depot, verde=deploy)")
    return fig


def show_graph_window(G: nx.MultiDiGraph) -> None:
    """
    Muestra el grafo. Si hay entorno gráfico, abre una ventana Tkinter
    interactiva. Si no (headless, ej. Codespaces), guarda un PNG y
    avisa la ruta por consola.
    """
    if not HAS_DISPLAY:
        fig = build_figure(G)
        out_path = os.path.abspath("grafo_kamppi.png")
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(
            "No se detectó entorno gráfico (DISPLAY no definido). "
            f"Se guardó una imagen del grafo en: {out_path}\n"
            "Ábrela desde el explorador de archivos de VS Code / Codespaces."
        )
        return

    import tkinter as tk
    from tkinter import ttk
    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg,
        NavigationToolbar2Tk,
    )

    root = tk.Tk()
    root.title("Visualizador de grafo - Kamppi, Helsinki")
    root.geometry("900x750")

    info = ttk.Label(
        root,
        text=f"Nodos: {G.number_of_nodes()}  |  Aristas: {G.number_of_edges()}",
        padding=8,
    )
    info.pack(side=tk.TOP, fill=tk.X)

    fig = build_figure(G)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()

    root.mainloop()
    plt.close(fig)


if __name__ == "__main__":
    import graph_service

    G = graph_service.build_graph()
    show_graph_window(G)