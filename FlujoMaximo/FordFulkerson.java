package FlujoMaximo;

import java.util.List;

public class FordFulkerson implements AlgoritmosFlujoMax{

    private StringBuilder caminos = new StringBuilder();
    private int pasos = 0;

    public StringBuilder getCaminos() {
        return caminos;
    }

    @Override
    public int getPasos() {
        return pasos;
    }

    @Override
    public int calcularFlujoMaximo(MatrizAdyacencia grafoOriginal, String nodoInicial, String nodoFinal) {

        pasos = 0;
        caminos.setLength(0);

        //Para no dañar los datos originales
        MatrizAdyacencia grafoResidual = clonarGrafo(grafoOriginal);

        int flujoMaximo = 0;

        RecorridoDFS buscador = new RecorridoDFS();

        //  bucle principal de Ford-Fulkerson
        while (true) {
            // se crea el camino desde la nodoInicial hasta el nodoFinal usando DFS
            int[] pasosBusqueda = new int[1];
            List<String> camino = buscador.caminoDFS(grafoResidual, nodoInicial, nodoFinal, pasosBusqueda);
            pasos += pasosBusqueda[0];

            // Si devuelve null significa que ya no hay más formas de llegar
            if (camino == null) {
                break;
            }

            // hallar el cuello de botella de ese camino
            int cuelloBotella = encontrarCuelloBotella(grafoResidual, camino);

            //actualizar las capacidades en el grafo residual con arista de vuelta por si en una futura iteración se encuentra un mejor camino
            actualizarCapacidades(grafoResidual, camino, cuelloBotella);

            //Acumula el flujo
            flujoMaximo += cuelloBotella;
        }

        return flujoMaximo;
    }

    private void actualizarCapacidades(MatrizAdyacencia grafoResidual, List<String> camino, int cuelloBotella) {
        // para cada nodo en el camino
        for(int i = 0; i < camino.size() - 1; i++) {

            //agarro el nodo actual y el siguiente
            String nodoActual = camino.get(i);
            String nodoSiguiente = camino.get(i + 1);

            //al valor de la clave "nodoSiguiente" del hashmap interno del nodo actual le resto el cuello de botella
            grafoResidual.getNodos().get(nodoActual).put(nodoSiguiente, grafoResidual.getNodos().get(nodoActual).get(nodoSiguiente) - cuelloBotella);

            // Sumar a la arista de VUELTA
            // Si la arista de vuelta no existe (porque originalmente era de un solo sentido), se crea con 0
            if (!grafoResidual.getNodos().get(nodoSiguiente).containsKey(nodoActual)) {
                grafoResidual.getNodos().get(nodoSiguiente).put(nodoActual, 0);
            }

            //ahora si se suma el cuello de botella a la arista de VUELTA (0 + cuelloBotella)
            grafoResidual.getNodos().get(nodoSiguiente).put(nodoActual, grafoResidual.getNodos().get(nodoSiguiente).get(nodoActual) + cuelloBotella);

            // hacer el string del camino con las nuevas capacidades entre nodos
            caminos.append(nodoActual).append(" -> ").append(nodoSiguiente).append(" (Capacidad: ").append(grafoResidual.getNodos().get(nodoActual).get(nodoSiguiente)).append(")\n");
        }
    }


    private int encontrarCuelloBotella(MatrizAdyacencia grafoResidual, List<String> camino) {
        //inicializar el cuello de botella como el valor máximo de un entero
        int cuelloBotella = Integer.MAX_VALUE;

        // para cada nodo en la lista camino
        for (int i = 0; i < camino.size() - 1; i++) {
            // agarro el nodo actual y el siguiente nodo en el camino
            String nodoActual = camino.get(i);
            String nodoSiguiente = camino.get(i + 1);

            //guardo la capacidad entre el nodo actual y el siguiente nodo
            int capacidad = grafoResidual.getNodos().get(nodoActual).get(nodoSiguiente);

            //si la capacidad del nodo actual es menor que el cuello de botella, actualizo el cuello de botella
            if (capacidad < cuelloBotella) {
                cuelloBotella = capacidad;
            }
        }
        return cuelloBotella;
    }

    private MatrizAdyacencia clonarGrafo(MatrizAdyacencia grafoOriginal) {
        return grafoOriginal.clone();
    }

}
