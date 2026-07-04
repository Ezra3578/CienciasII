package FlujoMaximo;

public class Main {

    public static void main(String[] args) throws Exception {

        // ============================
        // FORD-FULKERNSON
        // ============================

        // matriz de adyacencia dirigida para el algoritmo de flujo máximo
        MatrizAdyacenciaDirigida m2 = new MatrizAdyacenciaDirigida();

        m2.agregarArista("S", "V1", 3);
        m2.agregarArista("S", "V2", 7);

        m2.agregarArista("V1", "V3", 3);
        m2.agregarArista("V1", "V4", 4);

        m2.agregarArista("V2", "V1", 5);
        m2.agregarArista("V2", "V4", 3);

        m2.agregarArista("V3", "V4", 3);
        m2.agregarArista("V3", "T", 2);

        m2.agregarArista("V4", "T", 6);

        
        System.out.println("El grafo sobre iterar es el siguiente: \n"+m2.mostrarMatriz());


        FordFulkerson fordFulkerson = new FordFulkerson();
        int flujoMaximo = fordFulkerson.calcularFlujoMaximo(m2, "S", "T");
        System.out.println("El camino correspondiente al Ford-Fulkerson desde el nodo S hasta el nodo T es: \n");
        System.out.println(fordFulkerson.getCaminos());
        System.out.println("El flujo máximo desde S hasta T es: " + flujoMaximo);

        // ============================
        // EDMONDS-KARP
        // ============================
        EdmondsKarp edmondsKarp = new EdmondsKarp();
        int flujoMax = edmondsKarp.calcularFlujoMaximo(m2, "S", "T");
        System.out.println("El camino correspondiente al Edmonds-Karp desde el nodo S hasta el nodo T es: \n");
        System.out.println(edmondsKarp.getCaminos());
        System.out.println("El flujo máximo desde S hasta T es: " + flujoMax);

    }
}
