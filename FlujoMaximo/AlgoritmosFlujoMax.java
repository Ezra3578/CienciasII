package FlujoMaximo;

public interface AlgoritmosFlujoMax{

    public int calcularFlujoMaximo(MatrizAdyacencia grafoOriginal, String nodoInicial, String nodoFinal);

    public int getPasos();

}