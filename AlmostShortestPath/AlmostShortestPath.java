package AlmostShortestPath;

import java.util.*;
import java.io.*;


public class AlmostShortestPath {

    // Representa una arista dirigida hacia "destino" con un "peso" determinado
    static class Arista {
        int destino;
        int peso;

        Arista(int destino, int peso) {
            this.destino = destino;
            this.peso = peso;
        }
    }

    static final long INFINITO = Long.MAX_VALUE / 2;

    public static void main(String[] args) throws IOException {
        // Se usa StreamTokenizer para lectura rapida por consola (System.in),
        // ya que puede haber varios casos de prueba y hasta 10^4 aristas por caso.
        StreamTokenizer entrada = new StreamTokenizer(new BufferedReader(new InputStreamReader(System.in)));
        StringBuilder salida = new StringBuilder();

        while (true) {
            entrada.nextToken();
            int n = (int) entrada.nval;
            entrada.nextToken();
            int m = (int) entrada.nval;

            // Fin de la entrada: linea con "0 0"
            if (n == 0 && m == 0) {
                break;
            }

            entrada.nextToken();
            int s = (int) entrada.nval;
            entrada.nextToken();
            int d = (int) entrada.nval;

            // Listas de adyacencia del grafo original y del grafo invertido
            List<List<Arista>> grafo = new ArrayList<>();
            List<List<Arista>> grafoInverso = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                grafo.add(new ArrayList<>());
                grafoInverso.add(new ArrayList<>());
            }

            // Guardamos tambien la lista de aristas por separado, para poder
            // recorrerlas todas al momento de filtrar
            int[] origenArista = new int[m];
            int[] destinoArista = new int[m];
            int[] pesoArista = new int[m];

            for (int i = 0; i < m; i++) {
                entrada.nextToken();
                int u = (int) entrada.nval;
                entrada.nextToken();
                int v = (int) entrada.nval;
                entrada.nextToken();
                int p = (int) entrada.nval;

                origenArista[i] = u;
                destinoArista[i] = v;
                pesoArista[i] = p;

                grafo.get(u).add(new Arista(v, p));
                grafoInverso.get(v).add(new Arista(u, p));
            }

            // Paso 1: distancia minima desde S hacia todos los nodos
            long[] distDesdeS = dijkstra(grafo, s, n);

            // Si D no es alcanzable desde S, ni siquiera existe el camino mas corto,
            // por lo tanto tampoco puede existir el "almost shortest path"
            if (distDesdeS[d] >= INFINITO) {
                salida.append(-1).append("\n");
                continue;
            }

            long distanciaMasCorta = distDesdeS[d];

            // Paso 2: distancia minima desde todos los nodos hacia D
            // (se logra corriendo Dijkstra desde D en el grafo invertido)
            long[] distHaciaD = dijkstra(grafoInverso, d, n);

            // Paso 3: construir el grafo filtrado, eliminando TODAS las aristas
            // que pertenezcan a cualquier camino mas corto de S a D
            List<List<Arista>> grafoFiltrado = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                grafoFiltrado.add(new ArrayList<>());
            }

            for (int i = 0; i < m; i++) {
                int u = origenArista[i];
                int v = destinoArista[i];
                int p = pesoArista[i];

                boolean perteneceACaminoMasCorto =
                        distDesdeS[u] < INFINITO &&
                        distHaciaD[v] < INFINITO &&
                        (distDesdeS[u] + p + distHaciaD[v] == distanciaMasCorta);

                if (!perteneceACaminoMasCorto) {
                    grafoFiltrado.get(u).add(new Arista(v, p));
                }
            }

            // Paso 4: correr Dijkstra una vez mas, sobre el grafo ya filtrado
            long[] distCasiMasCorto = dijkstra(grafoFiltrado, s, n);

            if (distCasiMasCorto[d] >= INFINITO) {
                salida.append(-1).append("\n");
            } else {
                salida.append(distCasiMasCorto[d]).append("\n");
            }
        }

        System.out.print(salida);
    }

    /**
     * Dijkstra clasico usando cola de prioridad.
     * Devuelve un arreglo con la distancia minima desde "origen" hacia cada nodo del grafo.
     */
    static long[] dijkstra(List<List<Arista>> grafo, int origen, int n) {
        long[] dist = new long[n];
        Arrays.fill(dist, INFINITO);
        dist[origen] = 0;

        // Cada elemento de la cola es {nodo, distanciaActual}
        PriorityQueue<long[]> cola = new PriorityQueue<>((a, b) -> Long.compare(a[1], b[1]));
        cola.add(new long[]{origen, 0L});

        boolean[] visitado = new boolean[n];

        while (!cola.isEmpty()) {
            long[] actual = cola.poll();
            int nodo = (int) actual[0];

            if (visitado[nodo]) {
                continue;
            }
            visitado[nodo] = true;

            for (Arista arista : grafo.get(nodo)) {
                if (!visitado[arista.destino] && dist[nodo] + arista.peso < dist[arista.destino]) {
                    dist[arista.destino] = dist[nodo] + arista.peso;
                    cola.add(new long[]{arista.destino, dist[arista.destino]});
                }
            }
        }

        return dist;
    }
}