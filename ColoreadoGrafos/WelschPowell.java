package ColoreadoGrafos;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;



public class WelschPowell implements AlgoritmoColoreadoGrafos{

    ListaAdyacencia grafo; //El grafo :v
    private int pasos; //Los números de pasos :v
    private int maxColor; //Núm. máx. de colores usados xD
    private HashMap<Integer, List<String>> colores; //Lo que guarda los colores de cada nodo xD 

    public WelschPowell(ListaAdyacencia grafo){
        this.grafo = grafo;
        this.pasos = 0;
        this.maxColor = 0;
        this.colores = new HashMap<>();
    }

    @Override
    public void colorear() {
        // 1. Ordenar de mayor a menor cantidad de adyacencias
        List<String> orden = new ArrayList<>(this.grafo.getAdjList().keySet());
        orden.sort((a, b) -> Integer.compare(
                this.grafo.getAdjList().get(b).size(),
                this.grafo.getAdjList().get(a).size()));
        this.pasos += orden.size();

        // Lista de pendientes: se va reduciendo, así no se re-escanean los ya coloreados
        LinkedList<String> pendientes = new LinkedList<>(orden);

        this.maxColor = 0;

        // 2. Asignar colores mientras queden nodos pendientes
        while (!pendientes.isEmpty()) {

            this.maxColor++;
            List<String> nodoConMismoColor = new ArrayList<>();
            Set<String> prohibidos = new HashSet<>(); // adyacentes de los ya puestos en este color

            Iterator<String> it = pendientes.iterator();
            while (it.hasNext()) {
                String nombreActual = it.next();
                this.pasos++;

                // Chequeo O(1) en vez de recorrer la lista del grupo
                if (!prohibidos.contains(nombreActual)) {
                    nodoConMismoColor.add(nombreActual);
                    prohibidos.addAll(this.grafo.getAdjList().get(nombreActual).keySet());
                    it.remove(); // ya no vuelve a ser revisado en próximos colores
                }
            }

            colores.put(this.maxColor, nodoConMismoColor);
        }
    }

    public String getColoracion() {
        if (colores == null || colores.isEmpty()) {
            return "Aún no se ha ejecutado el algoritmo de coloración.";
        }
        StringBuilder sb = new StringBuilder();
        sb.append("Coloración obtenida con el algoritmo Welsh-Powell:\n");
        for (int color = 1; color <= maxColor; color++) {
            List<String> nodos = colores.get(color);
            if (nodos == null) continue;
            sb.append("Color ").append(color).append(" -> ").append(nodos).append("\n");
        }
        return sb.toString();
    }

    public String getNumeroCromatico() {
        if (colores == null) {
            return "Aún no se ha ejecutado el algoritmo de coloración.";
        }
        return "Número cromático aproximado: " + maxColor;
    }

    @Override
    public int getPasos() {
        return this.pasos;
    }
    
}
