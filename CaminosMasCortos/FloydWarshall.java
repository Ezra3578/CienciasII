import java.util.*;

public class FloydWarshall implements AlgoritmoDistanciaMasCorta {

    private MatrizAdyacencia grafo;
    private long[][] dist;
    private int[][] next;
    private static final long INF = (long) 1e15;
    private int pasos; 

    public FloydWarshall(MatrizAdyacencia grafo) {
        this.grafo = grafo;
    }

    @Override
    public void calcularDistanciaMasCorta(String nodo_inicial) {
        //Inicializar el contador en cero
        this.pasos = 0;

        //Construir matriz de adyacencia
        List<String> nodos = grafo.getMatriz(); 
        int V = nodos.size();
        dist = new long[V][V];
        next = new int[V][V];

        // Inicializar
        for (int i = 0; i < V; i++) {
            for (int j = 0; j < V; j++) {
                if (i == j) {
                    dist[i][j] = 0;
                } 
                
                else if (grafo.existeArista(nodos.get(i), nodos.get(j))) {
                    dist[i][j] = grafo.getPeso(nodos.get(i), nodos.get(j)); 
                } 
                else {
                    dist[i][j] = INF; 
                }
                next[i][j] = j;
            }
        }

        //CORE del algoritmo Floyd–Warshall
        for (int k = 0; k < V; k++) {
            for (int i = 0; i < V; i++) {
                for (int j = 0; j < V; j++) {

                    //Se cuentan los pasos del algoritmo principal
                    this.pasos++;

                    //Evitar que INF + valor negativo provoque una búsqueda infinita

                    if(dist[i][k] != INF && dist[k][j] != INF){
                        if (dist[i][k] + dist[k][j] < dist[i][j]) {
                            dist[i][j] = dist[i][k] + dist[k][j];
                            next[i][j] = next[i][k];
                        }
                    }
                }
            }
        }

        //Verificar si hay ciclos negativos que provocan búsquedas infinitas

        verificarCiclosNegativos(nodos);    
    }

    private void verificarCiclosNegativos(List<String> nodos) {
        List<String> nodosAfectados = new ArrayList<>();
        for (int i = 0; i < nodos.size(); i++) {
            if (dist[i][i] < 0) {
                nodosAfectados.add(nodos.get(i));
            }
        }

        if (!nodosAfectados.isEmpty()) {
            boolean esDirigido = grafo instanceof MatrizAdyacenciaDirigida;
            String tipo = esDirigido ? "dirigido" : "no dirigido";
            String nota = esDirigido
                ? "Existe un camino cerrado real cuya suma de pesos es negativa."
                : "En un grafo NO dirigido, basta con que UNA sola arista tenga peso "
                + "negativo para generar un ciclo negativo trivial (ida y vuelta por esa misma arista).";

            throw new IllegalStateException(
                "¡Grafo inválido (" + tipo + ")! Se detectó un ciclo negativo que involucra "
                + "al/los nodo(s): " + String.join(", ", nodosAfectados) + ". " + nota
            );
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

