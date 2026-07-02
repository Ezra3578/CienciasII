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
        System.out.println("===== Dijsktra =====");
        AlgoritmoDistanciaMasCorta dijkstra = new Dijkstra(ma);
        // Calcular desde A
        dijkstra.calcularDistanciaMasCorta("A");

        System.out.println(dijkstra.getDistancia("A"));
        System.out.println(dijkstra.getDistancia("A", "C"));
        System.out.println("Caminos desde nodo A:");
        System.out.println(dijkstra.getCamino("A"));
        System.out.println("Caminos desde nodo A a C:");
        System.out.println(dijkstra.getCamino("A", "C"));
        //Conteo de pasos en matrix 4X4
        System.out.println("La cantidad de pasos de Djikstra es: "+dijkstra.getPasos());

        // Probar también con nodo destino que no existe
        System.out.println("Prueba de error con una distancia entre nodo A y uno do que no existe:");
        System.out.println(dijkstra.getDistancia("A", "Z"));
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
        la.agregarArista("A", "D", 4);

        la.agregarArista("B", "D", 5);
        la.agregarArista("B", "C", 3);
        la.agregarArista("B", "E", 6);

        la.agregarArista("C", "E", 4);
        la.agregarArista("C", "H", 2);

        la.agregarArista("D", "E", 7);
        la.agregarArista("D", "F", 4);

        la.agregarArista("E", "F", 4);
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


        // ================================
        // 5. FLOYD–WARSHALL
        // ================================
        System.out.println("\n===== FLOYD–WARSHALL =====");
        FloydWarshall fw = new FloydWarshall(ma);


        try {
            fw.calcularDistanciaMasCorta("A");
            
            // Calcula todas las distancias mínimas
            fw.calcularDistanciaMasCorta("A");
            
            // Distancias desde A hacia todos
            System.out.println(fw.getDistancia("A"));

            // Distancia específica A → D
            System.out.println("Distancia A -> D = " + fw.getDistancia("A", "D"));

            // Camino completo desde A hacia todos
            System.out.println(fw.getCamino("A"));

            // Camino específico A → D
            System.out.println("Camino A -> D = " + fw.getCamino("A", "D"));

            //Cantidad de pasos de FloydWharshall
            System.out.println("La cantidad de pasos de FloydWharshall es: "+fw.getPasos());

        } catch (IllegalStateException e) {
            // Avisa del error en Floyd-Warshall pero NO detiene el Main
            System.err.println("[Floyd-Warshall] " + e.getMessage());
        }
        


        // ===================================
        // 6. BELLMAN-FORD
        // ===================================
        System.out.println("============ BELLMAN-FORD ============");

        BellmanFord algoritmoBellmanFord = new BellmanFord(ma);

        //ejecutar el algoritmo desde el nodo inicial "A"
        algoritmoBellmanFord.calcularDistanciaMasCorta("A");

        //obtener la distancias más corta desde A hasta todos los nodos
        System.out.println(algoritmoBellmanFord.getDistancia("A"));

        // obtener la distancia más corta entre A y D
        System.out.println(algoritmoBellmanFord.getDistancia("A", "D"));

        //obtener el camino más corto desde el nodo inicial "A" hasta el nodo destino "D"
        System.out.println(algoritmoBellmanFord.getCamino("A", "D"));

        //obtener todos los caminos más cortos desde el nodo inicial "A" hasta cualquier otro nodo
        System.out.println(algoritmoBellmanFord.getCamino("A"));

        //obtener cantidad de pasos
        System.out.println("Pasos para el algoritmo Bellman-Ford es : " + algoritmoBellmanFord.getPasos());

    }
}
