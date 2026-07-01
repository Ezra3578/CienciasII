public class BellmanFord implements AlgoritmoDistanciaMasCorta{

    MatrizAdyacencia grafo;
    
    BellmanFord(MatrizAdyacencia grafo) {
        this.grafo = grafo;
    }

    @Override
    public void calcularDistanciaMasCorta(String nodo_inicial){
        System.out.println("ola erick");
    }

    @Override
    public String getDistancia(String nodo_inicial){
        return "guau";
    }

    @Override
    public String getDistancia(String nodo_inicial, String nodo_destino){
        return "guau2";
    }

    @Override
    public String getCamino(String nodo_inicial){
        return "acá va el camino general desde un nodo especifico";
    }

    @Override
    public String getCamino(String nodo_inicial, String nodo_destino){
        return "acá un pedacito, solo el de un nodo a otro";
    }

    @Override
    public int getPasos() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getPasos'");
    }    
    
}
