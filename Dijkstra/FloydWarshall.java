public class FloydWarshall implements AlgoritmoDistanciaMasCorta{

    MatrizAdyacencia grafo;
    
    FloydWarshall(MatrizAdyacencia grafo) {
        this.grafo = grafo;
    }

    @Override
    public void calcularDistanciaMasCorta(String nodo_inicial){
        System.out.println("ola daniel");
    }

    @Override
    public String getDistancia(String nodo_inicial){
        return "asdf";
    }

    @Override
    public String getDistancia(String nodo_inicial, String nodo_destino){
        return "asdfg";
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
