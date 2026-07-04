package FlujoMaximo;

import java.util.*;

public class RecorridoDFS {
    //algoritmo de recorrido en profundidad


    //metodo de recorrido de grafos DFS
    //lo que hace es ir al primer vecino, y de ahí va al primer vecino y asi hasta no encontrar más vecinos
    // luego se devuelve al nodo exactamente anterior y se vuelve a ir al siguiente vecino
    // cuando llegue al final del grafo, se devuelve al nodo inicial

    //en búsqueda toca hacer que cuando encuentre un nodo ya visitado, no lo vuelva a visitar
    // y cuando encuentre el nodo objetivo, acabe el algoritmo

    public List<String> caminoDFS(MatrizAdyacencia grafo, String nodoInicial, String nodo_objetivo) {
         Set<String> visitados = new HashSet<>();
         List<String> camino = new ArrayList<>();

         if(dfsRecursivo(grafo, nodoInicial, nodo_objetivo, visitados, camino)) {
             return camino;
         }

         return null;
    }

    // este metodo es recursivo por la naturaleza el DFS
    private boolean dfsRecursivo(MatrizAdyacencia grafo, String nodoActual, String nodoObjetivo, Set<String> visitados, List<String> camino) {

        camino.add(nodoActual);
        visitados.add(nodoActual);

        if(nodoActual.equals(nodoObjetivo)) return true;

        // mapa de vecinos del nodo actual con var para evitar errores si llega a ser null
        var vecinosMap = grafo.getNodos().get(nodoActual);

        // Si el nodo no existe o no tiene vecinos/hijos hace backtracking
        if (vecinosMap == null || vecinosMap.isEmpty()) {
            //camino.removeLast(); //comentada pq el codespace usa es java versión 11, y ese método existe es desde la fokin versión 21
            camino.remove(camino.size()-1);
            return false;
        }

        //for que recorre los vecinos del nodo actual|
        for(String vecino : grafo.getNodos().get(nodoActual).keySet()) {

            //guarda la capacida entre el nodo actual y el vecino
            int capacidadDisponible = grafo.getNodos().get(nodoActual).get(vecino);

            //si el vecino no ha sido visitado, y la capacidad disponible es mayor que 0, llama recursivamente tomando este vecino como nodo actual
            if(!visitados.contains(vecino) && capacidadDisponible > 0 && dfsRecursivo(grafo, vecino, nodoObjetivo, visitados, camino)) {
                    return true;
            }
        }

        //backtracking en caso de que no se haya encontrado el nodo objetivo en este camino/sub-arbol
        //camino.removeLast();
        camino.remove(camino.size()-1);
        return false;
    }


}
