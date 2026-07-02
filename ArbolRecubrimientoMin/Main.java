import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        
        // ================================
        // LISTA DE ADYACENCIA
        // ================================
        System.out.println("\n===== LISTA DE ADYACENCIA =====");
        ListaAdyacencia la = new ListaAdyacencia();
        la.agregarNodo("A");
        la.agregarNodo("B");
        la.agregarNodo("C");
        la.agregarNodo("D");
        la.agregarNodo("E");
        la.agregarNodo("F");
        la.agregarNodo("G");
        la.agregarNodo("H");
        la.agregarNodo("I");
        la.agregarNodo("J");

        //Grafo inicial (iteración 0)
        la.agregarArista("A", "B", 5);
        la.agregarArista("A", "J", 2);
        la.agregarArista("B", "C", 4);
        la.agregarArista("B", "I", 8);
        la.agregarArista("C", "G", 10);
        la.agregarArista("D", "E", 4);
        la.agregarArista("D", "H", 7);
        la.agregarArista("E", "F", 6);
        la.agregarArista("F", "G", 1);
        la.agregarArista("H", "I", 3);
        la.imprimirConexiones();  // muestra cada nodo y sus pesos

        ArrayList<Prim> prim = new ArrayList<>();
        ArrayList<Kruskal> kruskal = new ArrayList<>();

        prim.add(new Prim(la));
        kruskal.add(new Kruskal(la));


        //Grafo con 2 nuevas aristas (iteración 1)
        la.agregarArista("B", "H", 9);
        la.agregarArista("H", "J", 13);
        la.imprimirConexiones();  // muestra cada nodo y sus pesos
        prim.add(new Prim(la));
        kruskal.add(new Kruskal(la));

        //Grafo con 4 nuevas aristas (iteración 2)
        la.agregarArista("A", "I", 7);
        la.agregarArista("B", "E", 15);
        la.imprimirConexiones();  // muestra cada nodo y sus pesos
        prim.add(new Prim(la));
        kruskal.add(new Kruskal(la));

        //Grafo con 6 nuevas aristas (iteración 3)
        la.agregarArista("C", "D", 6);
        la.agregarArista("G", "H", 2);
        la.imprimirConexiones();  // muestra cada nodo y sus pesos
        prim.add(new Prim(la));
        kruskal.add(new Kruskal(la));

        //Grafo con 8 nuevas aristas (iteración 4)
        la.agregarArista("B", "D", 11);
        la.agregarArista("A", "G", 15);
        la.imprimirConexiones();  // muestra cada nodo y sus pesos
        prim.add(new Prim(la));
        kruskal.add(new Kruskal(la));
        
        //Grafo con 10 nuevas aristas (iteración final)
        la.agregarArista("D", "F", 5);
        la.agregarArista("I", "J", 9);
        la.imprimirConexiones();  // muestra cada nodo y sus pesos
        prim.add(new Prim(la));
        kruskal.add(new Kruskal(la));

        for(int i=0; i<5;i++){
            System.out.println("\n\n================ Iteración "+(i)+" ================");

            //PRIM
            System.out.println("============ PRIM ============");
            System.out.println("El árbol de expansión mínima es: "+prim.get(i).getCamino("A"));
            System.out.println("Número de pasos: "+prim.get(i).getPasos());

            //Kruskal
            System.out.println("============ KRUSKAL ============");
            System.out.println("El árbol de expansión mínima es: "+kruskal.get(i).getCamino("A"));
            System.out.println("Número de pasos: "+kruskal.get(i).getPasos());            
        }
    }
}
