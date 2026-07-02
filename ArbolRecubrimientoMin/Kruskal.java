import java.util.*;

public class Kruskal implements AlgoritmoMSP{

    private ListaAdyacencia grafo;
    private int pasos;
    private List<Arista> mst;
    private int pesoTotal;

    public Kruskal(ListaAdyacencia grafo){
        this.grafo = grafo;
        this.pasos=0;
        this.mst = new ArrayList<>();
        this.pesoTotal = 0;

    }

    @Override
    public void encontrarMSP(String nodo_inicial){
        mst.clear();
        pesoTotal = 0;
        pasos = 0;

        //obtener todas las aristas únicas del grafo
        List<Arista> aristas = obtenerAristasUnicas();

        //ordenar las aristas por peso ascendente
        Collections.sort(aristas);

        //inicializar Union-Find con todos los nodos del grafo
        UnionFind uf = new UnionFind();
        for (String nodo : grafo.getNodos()) {
            uf.agregar(nodo);
        }

        //procesar las aristas en orden
        for (Arista arista : aristas) {
            pasos++;
            String u = arista.nodo1;
            String v = arista.nodo2;
            int peso = arista.peso;

            //si los extremos están en componentes diferentes, unir y agregar la arista al MST
            if (!uf.estanConectados(u, v)) {
                uf.unir(u, v);
                mst.add(arista);
                pesoTotal += peso;
            }

            //detener si ya tenemos V-1 aristas
            if (mst.size() == grafo.getNodos().size() - 1) {
                break;
            }
        }
    }

    @Override
    public String getCamino(String nodo_inicial){
        if (mst.isEmpty()) {
            return "No se ha calculado el MST. Ejecute encontrarMSP primero.";
        }
        StringBuilder sb = new StringBuilder();
        sb.append("Aristas del Árbol de Expansión Mínima:\n");
        for (Arista a : mst) {
            sb.append(a.nodo1).append(" - ").append(a.nodo2)
              .append(" : ").append(a.peso).append("\n");
        }
        sb.append("Peso total: ").append(pesoTotal);
        return sb.toString();
    }

    @Override
    public int getPasos(){
        return pasos;
    }



    //auxiliar:
    private List<Arista> obtenerAristasUnicas() {
        List<Arista> aristas = new ArrayList<>();
        Set<String> procesados = new HashSet<>(); //para no duplicar

        for (String nodo : grafo.getNodos()) {
            for (String vecino : grafo.getAristasDeUnNodo(nodo)) {
                //tomamos la arista cuando el nodo es lexicográficamente menor, así cada arista se agrega una única vez.
                if (nodo.compareTo(vecino) < 0) {
                    int peso = grafo.getPesoArista(nodo, vecino);
                    aristas.add(new Arista(nodo, vecino, peso));
                }
            }
        }
        return aristas;
    }



    //clase privada de Arista, así como la de juanito
    private class Arista implements Comparable<Arista> {
        String nodo1;
        String nodo2;
        int peso;

        Arista(String nodo1, String nodo2, int peso) {
            this.nodo1 = nodo1;
            this.nodo2 = nodo2;
            this.peso = peso;
        }

        @Override
        public int compareTo(Arista otra) {
            return Integer.compare(this.peso, otra.peso);
        }
    }


    //clase privada de westernunion (union-find)
    private class UnionFind {
        private Map<String, String> padre;
        private Map<String, Integer> rango;

        UnionFind() {
            padre = new HashMap<>();
            rango = new HashMap<>();
        }

        void agregar(String nodo) {
            if (!padre.containsKey(nodo)) {
                padre.put(nodo, nodo);
                rango.put(nodo, 0);
            }
        }

        String encontrar(String nodo) {
            if (!padre.get(nodo).equals(nodo)) {
                padre.put(nodo, encontrar(padre.get(nodo))); // compresión de camino
            }
            return padre.get(nodo);
        }

        void unir(String a, String b) {
            String raizA = encontrar(a);
            String raizB = encontrar(b);
            if (raizA.equals(raizB)) return;

            int rangoA = rango.get(raizA);
            int rangoB = rango.get(raizB);
            if (rangoA < rangoB) {
                padre.put(raizA, raizB);
            } else if (rangoA > rangoB) {
                padre.put(raizB, raizA);
            } else {
                padre.put(raizB, raizA);
                rango.put(raizA, rangoA + 1);
            }
        }

        boolean estanConectados(String a, String b) {
            return encontrar(a).equals(encontrar(b));
        }
    }    

}
