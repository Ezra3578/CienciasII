public class Main {
    public static void main(String[] args) {
        // ================================
        // 1. MATRIZ DE ADYACENCIA
        // ================================
        System.out.println("===== MATRIZ DE ADYACENCIA =====");
        MatrizAdyacencia ma = new MatrizAdyacencia();
        try {
            ma.agregarArista("A", "B", 2);
            ma.agregarArista("B", "C", 4);
            ma.agregarArista("C", "D", 1);
            ma.agregarArista("D", "A", 3);
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println(ma.mostrarMatriz());
        // ================================
        // 2. MATRIZ DE INCIDENCIA
        // ================================
        System.out.println("\n===== MATRIZ DE INCIDENCIA =====");
        String[] vertices = {"A", "B", "C", "D"};
        MatrizIncidencia mi = new MatrizIncidencia(vertices);
        mi.adicionarArista("E1", "A", "B", 2);
        mi.adicionarArista("E2", "A", "C", 4);
        mi.adicionarArista("E3", "B", "C", 1);
        mi.adicionarArista("E4", "B", "D", 3);
        mi.mostrarMatriz();

        // ================================
        // 3. LISTA DE ADYACENCIA
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

        // ================================
        // 4. LISTA DE INCIDENCIA
        // ================================
        System.out.println("\n===== LISTA DE INCIDENCIA =====");
        ListaIncidencia li = new ListaIncidencia();
        li.agregar("A", "B", 2);
        li.agregar("A", "C", 4);
        li.agregar("B", "C", 1);
        li.agregar("B", "D", 3);
        li.mostrarEstadoGrafo();
    }
}
