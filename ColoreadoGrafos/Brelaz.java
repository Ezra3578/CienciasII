package ColoreadoGrafos;

import java.util.*;

public class Brelaz implements AlgoritmoColoreadoGrafos {

    ListaAdyacencia grafo;
    private int pasos;                    
    private Map<String, Integer> colores; // Almacena la coloración tras ejecutar el algoritmo
    private int maxColor;                 // Número máximo de colores usados

    public Brelaz(ListaAdyacencia grafo) {
        this.grafo = grafo;
        this.pasos = 0;
    }

    /**
     * Ejecuta el algoritmo Brelaz (DSATUR) y guarda el resultado.
     * Muestra la coloración y el número cromático aproximado por consola.
     */
    public void colorear() {
        colores = new HashMap<>();
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
            // Seleccionar nodo con mayor grado de saturación (criterio Brelaz)
            String elegido = null;
            int maxSaturacion = -1;
            int maxGrado = -1;

            for (String nodo : grafo.getNodos()) {
                if (colores.get(nodo) == 0) {
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

            // Menor color no utilizado por vecinos
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
            pasos++;  // Incrementar contador de pasos

            // Actualizar saturación de vecinos no coloreados
            for (String vecino : grafo.getConexiones(elegido).keySet()) {
                if (colores.get(vecino) == 0) {
                    coloresVecinos.get(vecino).add(colorAsignado);
                }
            }
        }

        // Calcular número máximo de colores usados
        maxColor = colores.values().stream().max(Integer::compare).orElse(0);
    }

    /**
     * @return String con la coloración obtenida (nodo -> color).
     */
    public String getColoracion() {
        if (colores == null) {
            return "Aún no se ha ejecutado el algoritmo de coloración.";
        }
        StringBuilder sb = new StringBuilder();
        sb.append("Coloración obtenida con el algoritmo Brelaz:\n");
        for (String nodo : grafo.getNodos()) {
            sb.append("Nodo ").append(nodo).append(" -> Color ").append(colores.get(nodo)).append("\n");
        }
        return sb.toString();
    }

    /**
     * @return String con el número de colores utilizados (cota superior del número cromático).
     */

    public String getNumeroCromatico() {
        if (colores == null) {
            return "Aún no se ha ejecutado el algoritmo de coloración.";
        }
        return "Número cromático aproximado: " + maxColor;
    }

    @Override
    public int getPasos() {
        return pasos;
    }
    
}
