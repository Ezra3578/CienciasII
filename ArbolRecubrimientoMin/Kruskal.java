import java.util.*;

public class Kruskal implements AlgoritmoMSP{

    private ListaAdyacencia grafo;
    private int pasos;
    private List<Arista> mst;
    private int pesoTotal;

    public Kruskal(ListaAdyacencia grafo){
        this.grafo = grafo;
        pasos=0;
    }

    @Override
    public void encontrarMSP(String nodo_inicial){
        System.out.println("hola");
    }

    @Override
    public String getCamino(String nodo_inicial){
        return "sajfns";
    }

    @Override
    public int getPasos(){
        return 0;
    }

}
