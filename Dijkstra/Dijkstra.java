import java.util.*;
public class Dijkstra implements AlgoritmoDistanciaMasCorta {

    private MatrizAdyacencia grafo;
    private HashMap<String, HashMap<String, Integer>> distanciasPorOrigen;
    private HashMap<String, HashMap<String, String>> predecesoresPorOrigen;
    private int pasos;
    
    Dijkstra(MatrizAdyacencia grafo) {
        this.grafo = grafo;
        this.distanciasPorOrigen = new HashMap<>();
        this.predecesoresPorOrigen = new HashMap<>();
        this.pasos=0;
    }

    @Override
    public void calcularDistanciaMasCorta(String nodo_inicial){
        HashMap<String, Integer> distancias = new HashMap<>();
        HashMap<String, Boolean> visitados = new HashMap<>();
        HashMap<String, String> predecesores = new HashMap<>();
        pasos=0;
        for (String nodo : grafo.getMatriz()) {
            distancias.put(nodo, Integer.MAX_VALUE);
            visitados.put(nodo, false);
            predecesores.put(nodo, null);
        }

        distancias.put(nodo_inicial, 0);

        int tamano = grafo.getMatriz().size();
        //seleccionar nodo con distancia menor 
        for (int iter = 0; iter < tamano; iter++) {
            int distancia_min=Integer.MAX_VALUE;
            String nodo_menor =null;
            for (String nodo : grafo.getMatriz()) {
                if(!visitados.get(nodo) && distancias.get(nodo) < distancia_min){
                    distancia_min=distancias.get(nodo);
                    nodo_menor=nodo;
                }
                pasos++;
            }
            if(nodo_menor==null){
                break;
            }
            visitados.put(nodo_menor,true);
            //revisar si es la menor distancia
            for (Map.Entry<String, Integer> nodo_entrada : grafo.getNodos().get(nodo_menor).entrySet()){
                String nodoComparacion=nodo_entrada.getKey();
                int peso=nodo_entrada.getValue();
                if(!visitados.get(nodoComparacion)){
                    int temp=distancias.get(nodo_menor)+peso;
                    if(temp<distancias.get(nodoComparacion)){
                        distancias.put(nodoComparacion, temp);
                        predecesores.put(nodoComparacion, nodo_menor);
                    }
                }
            }
        }
        distanciasPorOrigen.put(nodo_inicial, distancias);
        predecesoresPorOrigen.put(nodo_inicial, predecesores);
    }

    @Override
    public String getDistancia(String nodo_inicial){
        if (!grafo.existeNodo(nodo_inicial)) {
        return "Error: El nodo de inicio no existe en el grafo.";
        }
        calcularDistanciaMasCorta(nodo_inicial);
        HashMap<String, Integer> distancias = distanciasPorOrigen.get(nodo_inicial);
        String resultado = "Distancias desde el nodo " + nodo_inicial + ":\n";

        for (String nodo : grafo.getMatriz()) {
            int dist = distancias.get(nodo);
            if (dist == Integer.MAX_VALUE) {
                resultado = resultado + nodo + ": INFINITO (no alcanzable)\n";
            } else {
                resultado = resultado + nodo + ": " + dist + "\n";
            }
        }
        return resultado;
    }

    @Override
    public String getDistancia(String nodo_inicial, String nodo_destino){
        if (!grafo.existeNodo(nodo_inicial)||!grafo.existeNodo(nodo_destino)) {
        return "Error: Al menos uno de sus nodos no existe en el grafo.";
        }
        calcularDistanciaMasCorta(nodo_inicial);
        HashMap<String, Integer> distancias = distanciasPorOrigen.get(nodo_inicial);
        int dist = distancias.get(nodo_destino);
        
        if (dist == Integer.MAX_VALUE) {
            return "No existe camino entre " + nodo_inicial + " y " + nodo_destino + ".";
        }
        return "Distancia entre " + nodo_inicial + " y " + nodo_destino + ": " + dist;
    }

    @Override
    public String getCamino(String nodo_inicial){
        if (!grafo.existeNodo(nodo_inicial)) {
        return "Error: El nodo de inicio no existe en el grafo.";
        }
        calcularDistanciaMasCorta(nodo_inicial);
        String stringCamino="";
        for (String nodo : grafo.getMatriz()) {
            if (nodo.equals(nodo_inicial)) continue;
                stringCamino = stringCamino + nodo_inicial + " -> " + nodo + ": "+ reconstruirCamino(nodo_inicial, nodo) + "\n";
        }
        return stringCamino;
    }

    @Override
    public String getCamino(String nodo_inicial, String nodo_destino){
        if (!grafo.existeNodo(nodo_inicial)||!grafo.existeNodo(nodo_destino)) {
        return "Error: Al menos uno de sus nodos no existe en el grafo.";
        }
        calcularDistanciaMasCorta(nodo_inicial);
        return reconstruirCamino(nodo_inicial, nodo_destino);
    }
    @Override
    public int getPasos(){
        return pasos;
    }
    private String reconstruirCamino(String nodo_inicial, String nodo_destino) {
        HashMap<String, Integer> distancias = distanciasPorOrigen.get(nodo_inicial);
        HashMap<String, String> predecesores = predecesoresPorOrigen.get(nodo_inicial);

        if (distancias.get(nodo_destino) == Integer.MAX_VALUE) {
            return "No existe camino";
        }

        LinkedList<String> camino = new LinkedList<>();
        String actual = nodo_destino;

        while (actual != null) {
            camino.addFirst(actual);
            actual = predecesores.get(actual);
        }

        return String.join(" -> ", camino);
    }

}
