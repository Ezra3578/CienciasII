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
        la.agregarArista("A", "B", 4);
        la.agregarArista("A", "D", 3);

        la.agregarArista("B", "D", 5);
        la.agregarArista("B", "C", 3);
        la.agregarArista("B", "E", 6);

        la.agregarArista("C", "E", 4);
        la.agregarArista("C", "H", 2);

        la.agregarArista("D", "E", 7);
        la.agregarArista("D", "F", 4);

        la.agregarArista("E", "F", 5);
        la.agregarArista("E", "G", 3);

        la.agregarArista("F", "G", 7);

        la.agregarArista("G", "H", 5);

        la.imprimirConexiones();  // muestra cada nodo y sus pesos


        // ===================================
        // 7. PRIM
        // ===================================
        System.out.println("============ PRIM ============");

        Prim prim = new Prim(la);

        System.out.println("El árbol de expansión mínima es: "+prim.getCamino("A"));

    }
}
