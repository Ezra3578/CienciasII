import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        
        //LISTA DE ADYACENCIA
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
        System.out.println("\n================ Iteración 0 ================");
        la.agregarArista("A", "B", 9);
        la.agregarArista("A", "J", 8);
        la.agregarArista("B", "C", 7);
        la.agregarArista("B", "I", 8);
        la.agregarArista("C", "G", 15);
        la.agregarArista("D", "E", 13);
        la.agregarArista("D", "H", 7);
        la.agregarArista("E", "F", 10);
        la.agregarArista("F", "G", 9);
        la.agregarArista("H", "I", 8);
        la.imprimirConexiones();  // muestra cada nodo y sus pesos

        ArrayList<Prim> prim = new ArrayList<>();
        ArrayList<Kruskal> kruskal = new ArrayList<>();

        prim.add(new Prim(la, true));
        kruskal.add(new Kruskal(la, true));


        //Grafo con 2 nuevas aristas (iteración 1)
        System.out.println("\n================ Iteración 1 ================");
        la.agregarArista("B", "H", 6);
        la.agregarArista("H", "J", 6);
        la.imprimirConexiones();  // muestra cada nodo y sus pesos
        prim.add(new Prim(la, true));
        kruskal.add(new Kruskal(la, true));

        //Grafo con 4 nuevas aristas (iteración 2)
        System.out.println("\n================ Iteración 2 ================");
        la.agregarArista("A", "I", 5);
        la.agregarArista("B", "E", 11);
        la.imprimirConexiones();  // muestra cada nodo y sus pesos
        prim.add(new Prim(la, true));
        kruskal.add(new Kruskal(la, true));

        //Grafo con 6 nuevas aristas (iteración 3)
        System.out.println("\n================ Iteración 3 ================");
        la.agregarArista("C", "D", 4);
        la.agregarArista("G", "H", 1);
        la.imprimirConexiones();  // muestra cada nodo y sus pesos
        prim.add(new Prim(la, true));
        kruskal.add(new Kruskal(la, true));

        //Grafo con 8 nuevas aristas (iteración 4)
        System.out.println("\n================ Iteración 4 ================");
        la.agregarArista("B", "D", 6);
        la.agregarArista("A", "G", 5);
        la.imprimirConexiones();  // muestra cada nodo y sus pesos
        prim.add(new Prim(la, true));
        kruskal.add(new Kruskal(la, true));

        //Grafo con 10 nuevas aristas (iteración final)
        System.out.println("\n================ Iteración 5 ================");
        la.agregarArista("D", "F", 2);
        la.agregarArista("I", "J", 3);
        la.imprimirConexiones();  // muestra cada nodo y sus pesos
        prim.add(new Prim(la, true));
        kruskal.add(new Kruskal(la, true));

        for(int i=0; i<5;i++){
            System.out.println("\n\n================ Iteración "+(i)+" ================");

            //PRIM
            System.out.println("============ PRIM ============");
            System.out.println("El árbol de expansión mínima es:\n"+prim.get(i).getCamino("A"));
            System.out.println("Número de pasos: "+prim.get(i).getPasos());

            //Kruskal
            System.out.println("============ KRUSKAL ============");
            System.out.println("El árbol de expansión mínima es:"+kruskal.get(i).getCamino("A"));
            System.out.println("Número de pasos: "+kruskal.get(i).getPasos());            
        }
    }
}
