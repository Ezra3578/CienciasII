package ColoreadoGrafos;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class Brelaz implements AlgoritmoColoreadoGrafos {

    ListaAdyacencia grafo;
    int pasos;

    public Brelaz(ListaAdyacencia grafo) {
        this.grafo = grafo;
        this.pasos = 0;
    }

        /**
     * Ejecuta el algoritmo de coloración Brelaz y muestra por consola
     * el color asignado a cada nodo. Los colores se representan como números
     * enteros positivos (1, 2, 3, ...).
     */

    @Override    
    public void colorear() {
        Map<String, Integer> colores = new HashMap<>();
        Map<String, Set<Integer>> coloresVecinos = new HashMap<>();
        Map<String, Integer> grados = new HashMap<>();

        // Inicialización
        for (String nodo : grafo.getNodos()) {
            colores.put(nodo, 0);
            coloresVecinos.put(nodo, new HashSet<>());
            grados.put(nodo, grafo.getGrado(nodo));
        }

        int totalNodos = grafo.getNodos().size();
        int coloreados = 0;

        while (coloreados < totalNodos) {
            // Seleccionar el nodo no coloreado con mayor grado de saturación.
            // En caso de empate, se elige el de mayor grado original.
            // Si persiste el empate, se toma el de menor orden lexicográfico.
            String elegido = null;
            int maxSaturacion = -1;
            int maxGrado = -1;

            for (String nodo : grafo.getNodos()) {
                if (colores.get(nodo) == 0) {  // aún no coloreado
                    int saturacion = coloresVecinos.get(nodo).size();
                    int grado = grados.get(nodo);

                    if (saturacion > maxSaturacion ||
                        (saturacion == maxSaturacion && grado > maxGrado) ||
                        (saturacion == maxSaturacion && grado == maxGrado &&
                         (elegido == null || nodo.compareTo(elegido) < 0))) {
                        maxSaturacion = saturacion;
                        maxGrado = grado;
                        elegido = nodo;
                    }
                }
            }

            // Asignar el menor color que no esté siendo usado por sus vecinos
            Set<Integer> coloresProhibidos = new HashSet<>();
            for (String vecino : grafo.getConexiones(elegido).keySet()) {
                int colorVecino = colores.get(vecino);
                if (colorVecino != 0) {
                    coloresProhibidos.add(colorVecino);
                }
            }

            int colorAsignado = 1;
            while (coloresProhibidos.contains(colorAsignado)) {
                colorAsignado++;
            }
            colores.put(elegido, colorAsignado);
            coloreados++;
            pasos++;

            // Actualizar la saturación de los vecinos no coloreados
            for (String vecino : grafo.getConexiones(elegido).keySet()) {
                if (colores.get(vecino) == 0) {
                    coloresVecinos.get(vecino).add(colorAsignado);
                }
            }
        }

        // Mostrar resultados por consola
        System.out.println("Coloración obtenida con el algoritmo Brelaz (DSATUR):");
        for (String nodo : grafo.getNodos()) {
            System.out.println("Nodo " + nodo + " -> Color " + colores.get(nodo));
        }

        // Número de colores utilizados (cota superior del número cromático)
        int maxColor = colores.values().stream().max(Integer::compare).orElse(0);
        System.out.println("Número cromático aproximado: " + maxColor);
    }

    @Override
    public int getPasos() {
        return pasos;
    }
    
}
