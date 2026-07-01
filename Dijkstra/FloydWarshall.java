import java.util.*;

public class FloydWarshall implements AlgoritmoDistanciaMasCorta {

    private MatrizAdyacencia grafo;
    private int[][] dist;
    private int[][] next;
    private static final int INF = (int)1e8;
    private int pasos; 

    public FloydWarshall(MatrizAdyacencia grafo) {
        this.grafo = grafo;
    }

    @Override
    public void calcularDistanciaMasCorta(String nodo_inicial) {
        //Inicializar el contador en cero
        this.pasos = 0;

        // Paso 1: construir matriz de adyacencia
        List<String> nodos = grafo.getMatriz(); // necesitas un getter en MatrizAdyacencia
        int V = nodos.size();
        dist = new int[V][V];
        next = new int[V][V];

        // inicializar
        for (int i = 0; i < V; i++) {
            for (int j = 0; j < V; j++) {
                if (i == j) {
                    dist[i][j] = 0;
                } else if (grafo.existeArista(nodos.get(i), nodos.get(j))) {
                    dist[i][j] = grafo.getPeso(nodos.get(i), nodos.get(j)); // necesitas getPeso
                } else {
                    dist[i][j] = INF;
                }
                next[i][j] = j;
            }
        }

        // Paso 2: algoritmo Floyd–Warshall
        for (int k = 0; k < V; k++) {
            for (int i = 0; i < V; i++) {
                for (int j = 0; j < V; j++) {

                    //Se cuentan los pasos del algoritmo principal
                    this.pasos++;
                    if (dist[i][k] + dist[k][j] < dist[i][j]) {
                        dist[i][j] = dist[i][k] + dist[k][j];
                        next[i][j] = next[i][k];
                    }
                }
            }
        }
    }

    @Override
    public String getDistancia(String nodo_inicial) {
        // devuelve todas las distancias desde nodo_inicial
        List<String> nodos = grafo.getMatriz();
        int idx = nodos.indexOf(nodo_inicial);
        StringBuilder sb = new StringBuilder();
        for (int j = 0; j < nodos.size(); j++) {
            sb.append("Distancia ").append(nodo_inicial)
              .append(" -> ").append(nodos.get(j))
              .append(" = ").append(dist[idx][j] == INF ? "INF" : dist[idx][j])
              .append("\n");
        }
        return sb.toString();
    }

    @Override
    public String getDistancia(String nodo_inicial, String nodo_destino) {
        List<String> nodos = grafo.getMatriz();
        int i = nodos.indexOf(nodo_inicial);
        int j = nodos.indexOf(nodo_destino);
        return dist[i][j] == INF ? "No hay camino" : String.valueOf(dist[i][j]);
    }

    @Override
    public String getCamino(String nodo_inicial) {
        // ejemplo: mostrar caminos desde nodo_inicial a todos
        List<String> nodos = grafo.getMatriz();
        int i = nodos.indexOf(nodo_inicial);
        StringBuilder sb = new StringBuilder();
        for (int j = 0; j < nodos.size(); j++) {
            if (i != j) {
                sb.append(nodo_inicial).append(" -> ").append(nodos.get(j))
                  .append(": ").append(reconstruirCamino(i, j, nodos)).append("\n");
            }
        }
        return sb.toString();
    }

    @Override
    public String getCamino(String nodo_inicial, String nodo_destino) {
        List<String> nodos = grafo.getMatriz();
        int i = nodos.indexOf(nodo_inicial);
        int j = nodos.indexOf(nodo_destino);
        return reconstruirCamino(i, j, nodos);
    }

    private String reconstruirCamino(int i, int j, List<String> nodos) {
        if (dist[i][j] == INF) return "No hay camino";
        List<String> camino = new ArrayList<>();
        camino.add(nodos.get(i));
        while (i != j) {
            i = next[i][j];
            camino.add(nodos.get(i));
        }
        return String.join(" -> ", camino);
    }

    @Override
    public int getPasos() {
        return this.pasos;
    }

}
