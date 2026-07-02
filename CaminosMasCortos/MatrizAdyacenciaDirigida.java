import java.util.ArrayList;

/**
 * Variante dirigida de MatrizAdyacencia.
 * A diferencia de la clase padre (que registra cada arista en ambos sentidos),
 * aquí una arista origen -> destino SOLO se almacena en ese sentido.
 * Esto es indispensable para Floyd-Warshall con pesos negativos.
 */
public class MatrizAdyacenciaDirigida extends MatrizAdyacencia {

    @Override
    public void agregarArista(String origen, String destino, int peso) {
        // Si alguno no existe, se crea
        agregarNodo(origen);
        agregarNodo(destino);

        // Si ya existe esa arista dirigida, no la duplica (usar actualizarPesoArista)
        if (existeArista(origen, destino)) return;

        // Solo se registra el sentido origen -> destino
        this.getNodos().get(origen).put(destino, peso);
    }

    @Override
    public void eliminarArista(String origen, String destino) {
        if (existeArista(origen, destino)) {
            this.getNodos().get(origen).remove(destino);
        }
    }

    @Override
    public void actualizarPesoArista(String origen, String destino, int nuevo_peso) {
        if (existeArista(origen, destino)) {
            this.getNodos().get(origen).put(destino, nuevo_peso);
        }
    }

    @Override
    public void eliminarNodo(String nombre_nodo) {
        if (!existeNodo(nombre_nodo)) {
            throw new IllegalArgumentException("El nodo '" + nombre_nodo + "' no existe");
        }

        // En un grafo dirigido, el mapa interno de nombre_nodo
        // solo contiene sus aristas SALIENTES. Para eliminarlo por completo
        // hay que recorrer TODOS los nodos y borrar cualquier arista ENTRANTE
        // que apunte hacia él
        ArrayList<String> todosLosNodos = new ArrayList<>(getMatriz());
        for (String otroNodo : todosLosNodos) {
            if (!otroNodo.equals(nombre_nodo)) {
                getNodos().get(otroNodo).remove(nombre_nodo);
            }
        }

        getNodos().remove(nombre_nodo);
        getMatriz().remove(nombre_nodo);
    }
}