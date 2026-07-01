import interfaces.RepresentacionGrafo;
import java.util.ArrayList;
import java.util.HashMap;

public class MatrizAdyacencia implements RepresentacionGrafo {

    private HashMap<String, HashMap<String, Integer>> nodos;

    // sigue siendo el "almacén de claves" ordenado por inserción
    private ArrayList<String> matriz;

    public MatrizAdyacencia() {
        this.nodos = new HashMap<>();
        this.matriz = new ArrayList<>();
    }

    // ── Métodos de la interface ──────────────────────────────────────────────

    @Override
    public void agregarNodo(String nombre_nodo) {
        if (!this.nodos.containsKey(nombre_nodo)) {
            this.nodos.put(nombre_nodo, new HashMap<>());
            this.matriz.add(nombre_nodo);
        }
    }

    @Override
    public void eliminarNodo(String nombre_nodo) throws Exception {
        if (!existeNodo(nombre_nodo)) {
            throw new Exception("El nodo '" + nombre_nodo + "' no existe");
        }

        //en vecino agarra las claves del hashmap interno de la clave nombre_nodo del hasmap externo
        ArrayList<String> vecinos = new ArrayList<>(this.nodos.get(nombre_nodo).keySet());

        // agarra cada vecino y borra de su hashmap interno el nodo nombre_nodo porque este será eliminado
        for (String vecino : vecinos) {
            this.nodos.get(vecino).remove(nombre_nodo); // borra la referencia inversa
        }

        // elimina el nodo del HashMap principal y de la lista
        this.nodos.remove(nombre_nodo);
        this.matriz.remove(nombre_nodo);
    }

    @Override
    public void agregarArista(String nombre_nodo1, String nombre_nodo2, int peso) {
        // Si alguno no existe se crea
        agregarNodo(nombre_nodo1);
        agregarNodo(nombre_nodo2);

        //si ya existe la conexión, pues, no la hace por segunda vez
        if (!verificarNodos(nombre_nodo1, nombre_nodo2)) return;

        // bidireccional
        this.nodos.get(nombre_nodo1).put(nombre_nodo2, peso);
        this.nodos.get(nombre_nodo2).put(nombre_nodo1, peso);
    }

    @Override
    public void eliminarArista(String nodo_origen, String nodo_destino) {
        // HashMap.remove() ignora silenciosamente si la clave no existe
        if (existeArista(nodo_origen, nodo_destino)) {
            this.nodos.get(nodo_origen).remove(nodo_destino);
            this.nodos.get(nodo_destino).remove(nodo_origen);
        }
    }

    @Override
    public void actualizarPesoArista(String nodo_origen, String nodo_destino, int nuevo_peso) {
        // put() sobre una clave existente simplemente sobreescribe el valor
        if (existeArista(nodo_origen, nodo_destino)) {
            this.nodos.get(nodo_origen).put(nodo_destino, nuevo_peso);
            this.nodos.get(nodo_destino).put(nodo_origen, nuevo_peso);
        }
    }

    @Override
    public boolean existeNodo(String nodo) {
        // O(1) gracias al hash
        return this.nodos.containsKey(nodo);
    }

    @Override
    public boolean existeArista(String nodo1, String nodo2) {

        return existeNodo(nodo1) && this.nodos.get(nodo1).containsKey(nodo2);
    }

    // metodo privado de validación

    private boolean verificarNodos(String nodo1, String nodo2) {
        // ahora delega en existeArista en lugar de duplicar la lógica
        return !existeArista(nodo1, nodo2);
    }

    public String mostrarMatriz() {
        StringBuilder salida = new StringBuilder();

        salida.append("   ");
        for (String nodo : this.matriz) {
            salida.append(String.format("%-4s", nodo));
        }
        salida.append(System.lineSeparator());

        for (String fila : this.matriz) {
            salida.append(String.format("%-3s", fila));
            for (String columna : this.matriz) {
                if (fila.equals(columna)) {
                    salida.append(String.format("%-4s", "-"));
                } else if (existeArista(fila, columna)) {
                    salida.append(String.format("%-4s", this.nodos.get(fila).get(columna)));
                } else {
                    salida.append(String.format("%-4s", "-"));
                }
            }
            salida.append(System.lineSeparator());
        }

        return salida.toString();
    }
}
