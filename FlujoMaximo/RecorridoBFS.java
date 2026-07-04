package FlujoMaximo;

import java.util.*;

public class RecorridoBFS {
    // algoritmo de recorrido en anchura

    // metodo de recorrido de grafos BFS
    // a diferencia del DFS, aquí se exploran todos los vecinos del nodo actual
    // antes de avanzar al siguiente nivel. Esto garantiza que el primer camino
    // encontrado hasta el nodo objetivo sea el más corto en número de aristas.
    // Esta propiedad es justamente la que usa Edmonds-Karp para acotar el número
    // de iteraciones del Ford-Fulkerson clásico.

    public List<String> caminoBFS(MatrizAdyacencia grafo, String nodoInicial, String nodo_objetivo) {

        // mapa para reconstruir el camino una vez se llegue al nodo objetivo
        Map<String, String> padres = new HashMap<>();
        Set<String> visitados = new HashSet<>();
        Queue<String> cola = new LinkedList<>();

        cola.add(nodoInicial);
        visitados.add(nodoInicial);

        while (!cola.isEmpty()) {

            // saco el primer nodo de la cola (FIFO, propio del BFS)
            String nodoActual = cola.poll();

            if (nodoActual.equals(nodo_objetivo)) {
                return reconstruirCamino(padres, nodoInicial, nodo_objetivo);
            }

            // mapa de vecinos del nodo actual con var para evitar errores si llega a ser null
            var vecinosMap = grafo.getNodos().get(nodoActual);

            // Si el nodo no existe o no tiene vecinos/hijos, simplemente no hay nada que expandir
            if (vecinosMap == null || vecinosMap.isEmpty()) {
                continue;
            }

            // for que recorre los vecinos del nodo actual
            for (String vecino : vecinosMap.keySet()) {

                // guarda la capacidad entre el nodo actual y el vecino
                int capacidadDisponible = vecinosMap.get(vecino);

                // si el vecino no ha sido visitado, y la capacidad disponible es mayor que 0, se encola
                if (!visitados.contains(vecino) && capacidadDisponible > 0) {
                    visitados.add(vecino);
                    padres.put(vecino, nodoActual);
                    cola.add(vecino);
                }
            }
        }

        // si la cola se vacía sin haber llegado al nodo objetivo, no hay camino aumentante
        return null;
    }

    // reconstruye el camino desde nodoInicial hasta nodoObjetivo recorriendo el mapa de padres hacia atrás
    private List<String> reconstruirCamino(Map<String, String> padres, String nodoInicial, String nodoObjetivo) {
        LinkedList<String> camino = new LinkedList<>();
        String nodoActual = nodoObjetivo;

        while (!nodoActual.equals(nodoInicial)) {
            camino.addFirst(nodoActual);
            nodoActual = padres.get(nodoActual);
        }
        camino.addFirst(nodoInicial);

        return camino;
    }

}