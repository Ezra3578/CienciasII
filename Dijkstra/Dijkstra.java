public class Dijkstra implements AlgoritmoDistanciaMasCorta {

    MatrizAdyacencia grafo;
    
    Dijkstra(MatrizAdyacencia grafo) {
        this.grafo = grafo;
    }

    @Override
    public void calcularDistanciaMasCorta(String nodo_inicial){
        System.out.println("ola laura");
    }

    @Override
    public String getDistancia(String nodo_inicial){
        return "miau";
    }

    @Override
    public String getDistancia(String nodo_inicial, String nodo_destino){
        return "miau2";
    }

    @Override
    public String getCamino(String nodo_inicial){
        return "acá va el camino general desde un nodo especifico";
    }

    @Override
    public String getCamino(String nodo_inicial, String nodo_destino){
        return "acá un pedacito, solo el de un nodo a otro";
    }

}
