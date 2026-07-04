package FlujoMaximo;

import caminoMasCortoAlgoritmos.BellmanFord.BellmanFord;
import libreriaGrafos.Grafos.MatrizAdyacencia;
import libreriaGrafos.Grafos.MatrizAdyacenciaDirigida;

public class Main {

    public static void main(String[] args) throws Exception {


        MatrizAdyacencia m = new MatrizAdyacencia();

        m.agregarArista("A", "B", 2);
        m.agregarArista("A", "C", 4);
        m.agregarArista("B", "C", 1);
        m.agregarArista("B", "D", 3);
        m.agregarArista("D", "E", 9);
        m.agregarArista("C", "E", 5);


        System.out.println(m.mostrarMatriz());

        // ===================================
        // 6. BELLMAN-FORD
        // ===================================
        System.out.println("============ BELLMAN-FORD ============");

        BellmanFord algoritmoBellmanFord = new BellmanFord(m);

        //ejecutar el algoritmo desde el nodo inicial "A"
        algoritmoBellmanFord.calcularDistanciaMasCorta("A");

        //obtener la distancias más corta desde A hasta todos los nodos
        System.out.println(algoritmoBellmanFord.getDistancia("A"));

        // obtener la distancia más corta entre A y D
        System.out.println(algoritmoBellmanFord.getDistancia("A", "D"));

        //obtener el camino más corto desde el nodo inicial "A" hasta el nodo destino "E"
        System.out.println(algoritmoBellmanFord.getCamino("A", "D"));

        //obtener todos los caminos más cortos desde el nodo inicial "A" hasta cualquier otro nodo
        System.out.println(algoritmoBellmanFord.getCamino("A"));

        //obtener cantidad de pasos
        System.out.println("Pasos para el algoritmo Bellman-Ford es : " + algoritmoBellmanFord.getPasos());

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


        FordFulkerson fordFulkerson = new FordFulkerson();
        int flujoMaximo = fordFulkerson.calcularFlujoMaximo(m2, "S", "T");
        System.out.println(fordFulkerson.getCaminos());
        System.out.println("El flujo máximo desde S hasta T es: " + flujoMaximo);


    }
}
