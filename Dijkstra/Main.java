import ListaAdjacencia;
import ListaIncidencia;
import MatrizAdyacencia;
import MatrizIncidencia;

public class Main {
    public static void main(String[] args) {
        // ================================
        // 1. MATRIZ DE ADYACENCIA
        // ================================
        System.out.println("===== MATRIZ DE ADYACENCIA =====");
        MatrizAdyacencia ma = new MatrizAdyacencia();
        try {
            ma.crearNodoYValor("A", "B", 2);
            ma.crearNodoYValor("A", "C", 4);
            ma.crearNodoYValor("B", "C", 1);
            ma.crearNodoYValor("B", "D", 3);
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
        ListaAdjacencia la = new ListaAdjacencia();
        la.agregarNodo("A");
        la.agregarNodo("B");
        la.agregarNodo("C");
        la.agregarNodo("D");
        la.agregarArista("A", "B", 2);
        la.agregarArista("A", "C", 4);
        la.agregarArista("B", "C", 1);
        la.agregarArista("B", "D", 3);
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
