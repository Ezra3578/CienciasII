package ColoreadoGrafos;

public class Main {
    public static void main(String[] args) {

        //javac ColoreadoGrafos/*.java && java ColoreadoGrafos.Main

        //acá copié y pegué un grafo de arboles.
        System.out.println("=== Lista de Adyacencia ===");
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
        la.agregarArista("B", "H", 6);
        la.agregarArista("H", "J", 6);
        la.agregarArista("A", "I", 5);
        la.agregarArista("B", "E", 11);
        la.imprimirConexiones();  // muestra cada nodo y sus pesos                        

        //******BRELAZ*****
        System.out.println("\n=== Algoritmo Brelaz===");
        Brelaz brelaz = new Brelaz(la);
        brelaz.colorear();  // ejecuta y muestra en consola

        String resultadoColoracion = brelaz.getColoracion();
        String resultadoCromatico = brelaz.getNumeroCromatico();

        System.out.println(resultadoColoracion);
        System.out.println(resultadoCromatico);
        System.out.println("Pasos realizados: " + brelaz.getPasos());
    
        //****** WELSCH POWELL *****
        System.out.println("\n=== Algoritmo Welsch Powell===");
        WelschPowell welschPowell = new WelschPowell(la);
        welschPowell.colorear();  // ejecuta y muestra en consola

        resultadoColoracion = welschPowell.getColoracion();
        resultadoCromatico = welschPowell.getNumeroCromatico();

        System.out.println(resultadoColoracion);
        System.out.println(resultadoCromatico);
        System.out.println("Pasos realizados: " + welschPowell.getPasos());
        //****** SECUENCIA BASICO(VORAZ) *****
        System.out.println("\n=== Algoritmo de Secuencia Basico===");
        VorazColoreado voraz = new VorazColoreado(la);
        voraz.colorear();
        System.out.println(voraz.imprimir());
    
    }
}
