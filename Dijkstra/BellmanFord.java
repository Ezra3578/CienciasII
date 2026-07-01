import interfaces.AlgoritmoDistanciaMasCorta;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Map;

public class BellmanFord implements AlgoritmoDistanciaMasCorta {

    MatrizAdyacencia grafo;
    Map<String, Integer> distancias;
    private int pasos;

    // <nodo actual, nodo anterior> más corto desde el nodo inicial
    Map<String, String> predecesores;



    public BellmanFord(MatrizAdyacencia grafo) {
        this.grafo = grafo;
        this.distancias = new java.util.HashMap<>();
        this.predecesores = new java.util.HashMap<>();
        this.pasos = 0;

        for(String nodo : grafo.getMatriz()) {
            distancias.put(nodo, Integer.MAX_VALUE);
            predecesores.put(nodo, null);
        }
    }

    @Override
    public void calcularDistanciaMasCorta(String nodo_inicial){

        distancias.put(nodo_inicial, 0);

        int nVertices = grafo.getMatriz().size();

        //bucle principal de nVertices-1 veces
        for(int i = 0; i < nVertices-1; i++) {
            //bucle del nodo exterior
            for(String nodo : grafo.getNodos().keySet()) {
                //si la distancia del nodo exterior es infinito, pues no hay camino desde el nodo inicial hasta el nodo exterior
                if (distancias.get(nodo) == Integer.MAX_VALUE) continue;

                //bucle de los vecinos del nodo exterior
                for(String vecino : grafo.getNodos().get(nodo).keySet()) {
                    //cantidad de veces que ejecutó este for -> cantidad de pasos
                    this.pasos++;
                    //si la distancia acumulada entre el nodo inicial y el "nodo" + la distancia entre el "nodo" y el "vecino" es
                    //menor que la distancia actual desde el nodo inicial hasta el "vecino", pues actualice esa distancia porque es menor
                    int distanciaCandidata = distancias.get(nodo) + grafo.getNodos().get(nodo).get(vecino);
                    if(distanciaCandidata < distancias.get(vecino)) {
                        distancias.put(vecino, distanciaCandidata);

                        // para llegar al vecino se pasa por el nodo exterior
                        predecesores.put(vecino, nodo);
                    }
                }
            }
        }
    }

    @Override
    public String getDistancia(String nodo_inicial){
        StringBuilder respuesta = new StringBuilder("Distancias más cortas desde el nodo inicial " + nodo_inicial + ":\n");
        for (String nodo : grafo.getMatriz()) {
            respuesta.append("Distancia a ").append(nodo).append(": ").append(distancias.get(nodo)).append("\n");
        }
        return respuesta.toString();
    }

    @Override
    public String getDistancia(String nodo_inicial, String nodo_destino){
        return "La distancia más corta entre " + nodo_inicial + " y " + nodo_destino + " es: " + distancias.get(nodo_destino);
    }

    @Override
    public String getCamino(String nodo_inicial){
        StringBuilder respuesta = new StringBuilder("Caminos más cortos desde " + nodo_inicial + ":\n");
        for (String nodo : grafo.getMatriz()) {
            respuesta.append(getCamino(nodo_inicial, nodo)).append("\n");
        }
        return respuesta.toString();
    }

    @Override
    public String getCamino(String nodo_inicial, String nodo_destino){
        // si nunca se alcanzó, no hay predecesor que seguir
        if (distancias.get(nodo_destino) == Integer.MAX_VALUE) {
            return nodo_inicial + " -> " + nodo_destino + ": no hay camino posible";
        }

        ArrayList<String> camino = new ArrayList<>();
        String actual = nodo_destino;

        // caminar hacia atrás desde el destino, siguiendo predecesores, hasta llegar al inicio (predecesor == null)
        while (actual != null) {
            camino.add(actual);
            actual = predecesores.get(actual);
        }

        Collections.reverse(camino); // se armó al revés (destino → inicio), toca invertirlo
        return String.join(" -> ", camino);
    }


    @Override
    public int getPasos() {
        return pasos;
    }
}
