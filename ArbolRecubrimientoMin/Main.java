import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        

    //PRUEBA 1:
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
        la.agregarArista("F", "G", 7);
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

        //Grafo con 10 nuevas aristas (iteración 5)
        System.out.println("\n================ Iteración 5 ================");
        la.agregarArista("D", "F", 2);
        la.agregarArista("I", "J", 3);
        la.imprimirConexiones();  // muestra cada nodo y sus pesos
        prim.add(new Prim(la, true));
        kruskal.add(new Kruskal(la, true));

        //Grafo con 15 nuevas aristas (iteración 6)
        System.out.println("\n================ Iteración 6 ================");
        la.agregarArista("A", "C", 10);
        la.agregarArista("C", "I", 7);
        la.agregarArista("D", "G", 4);
        la.agregarArista("D", "J", 17);
        la.agregarArista("F", "H", 6);
        la.imprimirConexiones();  // muestra cada nodo y sus pesos
        prim.add(new Prim(la, true));
        kruskal.add(new Kruskal(la, true));

        //Grafo con 20 nuevas aristas (iteración final)
        System.out.println("\n================ Iteración 7 ================");
        la.agregarArista("A", "E", 21);
        la.agregarArista("B", "J", 2);
        la.agregarArista("C", "H", 7);
        la.agregarArista("E", "G", 5);
        la.agregarArista("G", "I", 12);
        la.imprimirConexiones();  // muestra cada nodo y sus pesos
        prim.add(new Prim(la, true));
        kruskal.add(new Kruskal(la, true));

        for(int i=0; i<8;i++){
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

    //PRUEBA 2:
        ListaAdyacencia li = new ListaAdyacencia();
        li.agregarNodo("A");
        li.agregarNodo("B");
        li.agregarNodo("C");
        li.agregarNodo("D");
        li.agregarNodo("E");
        li.agregarNodo("F");
        li.agregarNodo("G");
        li.agregarNodo("H");
        li.agregarNodo("I");
        li.agregarNodo("J");
        li.agregarNodo("K");
        li.agregarNodo("L");
        li.agregarNodo("M");
        li.agregarNodo("N");
        li.agregarNodo("O");
        li.agregarNodo("P");
        li.agregarNodo("Q");
        li.agregarNodo("R");
        li.agregarNodo("S");
        li.agregarNodo("T");
        
        li.agregarArista("A", "K", 2);
        li.agregarArista("A", "L", 4);
        li.agregarArista("B", "C", 5);
        li.agregarArista("C", "D", 2);
        li.agregarArista("C", "M", 7);
        li.agregarArista("D", "N", 3);
        li.agregarArista("E", "F", 11);
        li.agregarArista("E", "N", 6);
        li.agregarArista("E", "P", 9);
        li.agregarArista("G", "H", 6);
        li.agregarArista("G", "P", 12);
        li.agregarArista("G", "Q", 4);
        li.agregarArista("H", "R", 5);
        li.agregarArista("I", "J", 9);
        li.agregarArista("I", "S", 3);
        li.agregarArista("I", "T", 5);
        li.agregarArista("J", "T", 10);
        li.agregarArista("L", "M", 8);
        li.agregarArista("N", "O", 9);
        li.agregarArista("R", "S", 8);

        ArrayList<Prim> pr = new ArrayList<>();
        ArrayList<Kruskal> kr = new ArrayList<>();

        pr.add(new Prim(li, true));
        kr.add(new Kruskal(li, true));        

        li.agregarArista("B", "D", 7);
        li.agregarArista("B", "M", 6);
        li.agregarArista("E", "O", 4);
        li.agregarArista("F", "H", 10);
        li.agregarArista("K", "N", 6);

        pr.add(new Prim(li, true));
        kr.add(new Kruskal(li, true)); 
        
        li.agregarArista("B", "N", 10);
        li.agregarArista("F", "P", 2);
        li.agregarArista("H", "Q", 12);
        li.agregarArista("O", "R", 11);
        li.agregarArista("P", "Q", 8);

        pr.add(new Prim(li, true));
        kr.add(new Kruskal(li, true)); 

        li.agregarArista("A", "O", 14);
        li.agregarArista("D", "P", 13);
        li.agregarArista("E", "J", 16);
        li.agregarArista("G", "I", 8);
        li.agregarArista("S", "T", 7);

        pr.add(new Prim(li, true));
        kr.add(new Kruskal(li, true)); 

        li.agregarArista("A", "E", 12);
        li.agregarArista("F", "S", 15);
        li.agregarArista("J", "S", 9);
        li.agregarArista("P", "R", 11);
        li.agregarArista("K", "L", 5);

        pr.add(new Prim(li, true));
        kr.add(new Kruskal(li, true)); 

        li.agregarArista("B", "J", 7);
        li.agregarArista("C", "E", 4);
        li.agregarArista("C", "I", 15);
        li.agregarArista("I", "M", 13);
        li.agregarArista("R", "T", 9);   
        
        pr.add(new Prim(li, true));
        kr.add(new Kruskal(li, true)); 

        li.agregarArista("D", "M", 4);
        li.agregarArista("F", "N", 7);
        li.agregarArista("H", "I", 8);
        li.agregarArista("J", "R", 8);
        li.agregarArista("K", "M", 7);  
        
        pr.add(new Prim(li, true));
        kr.add(new Kruskal(li, true));         

        
        for(int i=0; i<7;i++){
            System.out.println("\n\n================ Iteración "+(i)+" ================");

            //PRIM
            System.out.println("============ PRIM ============");
            System.out.println("El árbol de expansión mínima es:\n"+pr.get(i).getCamino("A"));
            System.out.println("Número de pasos: "+pr.get(i).getPasos());

            //Kruskal
            System.out.println("============ KRUSKAL ============");
            System.out.println("El árbol de expansión mínima es:"+kr.get(i).getCamino("A"));
            System.out.println("Número de pasos: "+kr.get(i).getPasos());            
        }        
    }
}
