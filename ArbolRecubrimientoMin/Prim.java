import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Set;

public class Prim implements AlgoritmoMSP{

    private ListaAdyacencia grafo;
    private Set<String> visitados;
    private PriorityQueue<Arista> pQueue;
    private List<Arista> aristasMST;

    private int pasos;

    public Prim(ListaAdyacencia grafo, boolean copiarGrafo){
        if(copiarGrafo){
            this.grafo = grafo.copiar();
        } else {
            this.grafo = grafo;
        }
        this.visitados = new HashSet<>();
        this.pQueue = new PriorityQueue<>();
        this.pasos = 0;
        this.aristasMST = new ArrayList<>();
    }

        public Prim(ListaAdyacencia grafo){
        this.grafo = grafo;
        this.visitados = new HashSet<>();
        this.pQueue = new PriorityQueue<>();
        this.pasos = 0;
        this.aristasMST = new ArrayList<>();
    }

    @Override
    public void encontrarMSP(String nodo_inicial) {
        //Limpia los valores
        visitados.clear();
        pQueue.clear();
        aristasMST.clear();
        pasos = 0;

        //Toma el primer nodo
        String nodoActual = nodo_inicial;

        //Se marca el actual como visitados
        visitados.add(nodoActual);

        //Se agrega a la priority queue la arista con todos sus vecinos, sin embargo si ya está visitado el vecino, lo ignora
        agregarAristasVecinas(nodoActual);

        //Mientras la queue tenga elementos && los nodos visitados sean menor que los del grafo
        while(!pQueue.isEmpty() && visitados.size() < grafo.getNodos().size()){

            //Saca la primer arista de la queue
            Arista minima = pQueue.poll();
            //Aumenta 1 paso
            pasos++;

            // Lazy deletion: si el destino ya fue visitado, se descarta y seguimos
            if(visitados.contains(minima.getNodo2())){
                continue;
            }

            //Se agrega la arista al arbol
            aristasMST.add(minima);
            //Se crea el nodo adyacente al actual
            String nuevoNodo = minima.getNodo2();
            //Se agrega como visitado 
            visitados.add(nuevoNodo);

            //Hace el ciclo con el nuevo agregado para tomar sus aristas
            agregarAristasVecinas(nuevoNodo);
        }
    }

    private void agregarAristasVecinas(String nodo){
        //Obtiene los vecinos de un nodo
        HashMap<String, Integer> vecinos = this.grafo.getConexiones(nodo);
        
        //Para cada vecino
        for(Map.Entry<String, Integer> vecino : vecinos.entrySet()){
            //Si no está visitado
            if(!visitados.contains(vecino.getKey())){
                //Agrega la arista a la cola
                pQueue.add(new Arista(nodo, vecino.getKey(), vecino.getValue()));
            }
        }
    }

    @Override
    public String getCamino(String nodo_inicial) {
        encontrarMSP(nodo_inicial);
        StringBuilder sb = new StringBuilder();
        int pesoTotal = 0;
        for(Arista a : aristasMST){
            sb.append(a.getNodo1()).append(" -- ").append(a.getNodo2())
              .append(" (").append(a.getPeso()).append(")\n");
            pesoTotal += a.getPeso();
        }
        sb.append("Peso total del MST: ").append(pesoTotal);
        return sb.toString();
    }

    @Override
    public int getPasos() {
        return this.pasos;
    }

    private class Arista implements Comparable<Arista>{
        private String nodo1;
        private String nodo2;
        private Integer peso;

        public Arista(String nodo1, String nodo2, Integer peso){
            this.nodo1 = nodo1;
            this.nodo2 = nodo2;
            this.peso = peso;
        }

        @Override
        public int compareTo(Arista otra){
            return this.peso.compareTo(otra.peso);
        }

        public String getNodo1(){
            return this.nodo1;
        } 

        public String getNodo2(){
            return this.nodo2;
        } 

        public Integer getPeso(){
            return this.peso;
        } 
    }
}