//package com.example;

import java.util.ArrayList;
import java.util.HashMap;

public class MatrizAdyacencia {

    // hashMap que tomará los nodos como clave y los nodos adyacentes con su peso
    // como valor
    private HashMap<String, HashMap<String, Integer>> nodos;

    private ArrayList<String> matriz;

    // inicializar nodos y matriz vacíos
    public MatrizAdyacencia() {
        this.nodos = new HashMap<>();
        this.matriz = new ArrayList<>();
    }
    public ArrayList<String> getListaNodos() {
    return matriz;
    }

    public HashMap<String, HashMap<String, Integer>> getNodosMapa() {
        return nodos;
    }
    public boolean existeNodo(String nodo) {
        return this.nodos.containsKey(nodo);
    }

    // método recibe una arista con el par de nodos que invilucra y el peso
    public void crearNodoYValor(String nodo1, String nodo2, Integer peso) throws Exception {

        if (!verificarNodos(nodo1, nodo2)) {
            throw new Exception(
                    "el nodo no puede tener dos arista iguales o esa arista ya está en uso por otros nodos");
        }

        // ArrayList.contains() es O(n)
        if (!this.matriz.contains(nodo1))
            this.matriz.add(nodo1);
        if (!this.matriz.contains(nodo2))
            this.matriz.add(nodo2);

        // computeIfAbsent: si el nodo no existe lo crea, si ya existe lo deja
        // se pone de ambos lados para acceder desde cualquier nodo
        this.nodos.computeIfAbsent(nodo1, k -> new HashMap<>()).put(nodo2, peso);
        this.nodos.computeIfAbsent(nodo2, k -> new HashMap<>()).put(nodo1, peso);

    }

    public void eliminarNodo(String nodo) throws Exception {
        if (this.nodos.containsKey(nodo)) {
            this.nodos.remove(nodo);
            this.matriz.remove(nodo);
        }

        throw new Exception("el nodo no existe");
    }

    public void actualizarPeso(String nodo1, String nodo2, Integer peso) throws Exception {

        if (this.nodos.containsKey(nodo1) && this.nodos.containsKey(nodo2)) {

            if (!verificarNodos(nodo1, nodo2)) {
                // accedo a la clave nodo1 en el hashMap y luiego a la clave nodo2 y actualizo
                // el valor
                // pues si a .put() se le da una clave que ya existe, el valor se actualiza no
                // se duplica
                this.nodos.get(nodo1).put(nodo2, peso);
                this.nodos.get(nodo2).put(nodo1, peso);
                return;

            } else {
                throw new Exception("la arista no existe");
            }
        }
        throw new Exception("el nodo no existe");
    }

    public String mostrarMatriz() {

        StringBuilder salida = new StringBuilder();

        // ── Encabezado: nombres de columnas ─────────────────────────────
        salida.append("   "); // celda vacía para alinear con las etiquetas de fila
        for (String nodo : this.matriz) {
            // %-4s → alineado a la izquierda, ancho fijo de 4 caracteres
            // garantiza que las columnas queden alineadas sin importar el largo del nombre
            salida.append(String.format("%-4s", nodo));
        }
        salida.append(System.lineSeparator());

        // ── Filas: un nodo por fila ──────────────────────────────────────
        for (String fila : this.matriz) {
            salida.append(String.format("%-3s", fila)); // etiqueta de fila, ancho 3

            for (String columna : this.matriz) {
                if (fila.equals(columna)) {
                    // diagonal: un nodo no se conecta consigo mismo
                    salida.append(String.format("%-4s", "-"));

                } else if (this.nodos.containsKey(fila)
                        && this.nodos.get(fila).containsKey(columna)) {
                    // ambos containsKey son O(1) por hash — no es fuerza bruta
                    // si hay conexión → mostrar el peso
                    salida.append(String.format("%-4s", this.nodos.get(fila).get(columna)));

                } else {
                    // no hay conexión entre estos dos nodos
                    salida.append(String.format("%-4s", "-"));
                }
            }
            salida.append(System.lineSeparator());
        }

        return salida.toString();
    }

    private boolean verificarNodos(String nodo1, String nodo2) {
        // si el hashmap contiene al nodo 1 entonces verifique si este tiene a nodo 2
        if (this.nodos.containsKey(nodo1)) {
            return !this.nodos.get(nodo1).containsKey(nodo2);
        }
        return true; // nodo1 ni siquiera existe aún → conexión válida
    }
    /*
     * public static void main(String[] args) {
     * 
     * MatrizAdyacencia g = new MatrizAdyacencia();
     * try {
     * g.crearNodoYValor("A", "B", 1);
     * g.crearNodoYValor("A", "C", 2);
     * g.crearNodoYValor("B", "C", 3);
     * g.crearNodoYValor("B", "D", 4);
     * g.crearNodoYValor("C", "D", 5);
     * g.crearNodoYValor("C", "E", 6);
     * g.crearNodoYValor("D", "E", 7);
     * g.crearNodoYValor("D", "F", 8);
     * g.crearNodoYValor("E", "F", 9);
     * g.crearNodoYValor("E", "G", 10);
     * g.crearNodoYValor("F", "G", 11);
     * g.crearNodoYValor("F", "H", 12);
     * g.crearNodoYValor("G", "H", 13);
     * g.crearNodoYValor("G", "I", 14);
     * g.crearNodoYValor("H", "I", 15);
     * g.crearNodoYValor("H", "J", 16);
     * g.crearNodoYValor("I", "J", 17);
     * g.crearNodoYValor("I", "K", 18);
     * g.crearNodoYValor("J", "K", 19);
     * g.crearNodoYValor("J", "L", 20);
     * g.crearNodoYValor("K", "L", 21);
     * g.crearNodoYValor("K", "M", 22);
     * g.crearNodoYValor("L", "M", 23);
     * g.crearNodoYValor("L", "N", 24);
     * g.crearNodoYValor("M", "N", 25);
     * g.crearNodoYValor("M", "O", 26);
     * g.crearNodoYValor("N", "O", 27);
     * g.crearNodoYValor("N", "P", 28);
     * g.crearNodoYValor("O", "P", 29);
     * g.crearNodoYValor("O", "Q", 30);
     * g.crearNodoYValor("P", "Q", 31);
     * g.crearNodoYValor("P", "R", 32);
     * g.crearNodoYValor("Q", "R", 33);
     * g.crearNodoYValor("Q", "S", 34);
     * g.crearNodoYValor("R", "S", 35);
     * g.crearNodoYValor("R", "T", 36);
     * g.crearNodoYValor("S", "T", 37);
     * g.crearNodoYValor("S", "U", 38);
     * g.crearNodoYValor("T", "U", 39);
     * g.crearNodoYValor("T", "V", 40);
     * g.crearNodoYValor("U", "V", 41);
     * g.crearNodoYValor("U", "W", 42);
     * g.crearNodoYValor("V", "W", 43);
     * g.crearNodoYValor("V", "X", 44);
     * g.crearNodoYValor("W", "X", 45);
     * g.crearNodoYValor("W", "Y", 46);
     * g.crearNodoYValor("X", "Y", 47);
     * g.crearNodoYValor("X", "Z", 48);
     * g.crearNodoYValor("Y", "Z", 49);
     * g.crearNodoYValor("Y", "A", 50);
     * g.crearNodoYValor("Z", "A", 51);
     * g.crearNodoYValor("Z", "B", 52);
     * g.crearNodoYValor("A", "B", 53);
     * } catch (Exception e) {
     * System.out.println(e.getMessage());
     * }
     * System.out.println(g.mostrarMatriz());
     * 
     * try {
     * g.actualizarPeso("A", "B", 5);
     * g.actualizarPeso("A", "C", 2);
     * g.actualizarPeso("B", "C", 44);
     * g.actualizarPeso("B", "D", 4);
     * g.actualizarPeso("C", "D", 5);
     * g.actualizarPeso("C", "E", 6);
     * g.actualizarPeso("D", "E", 7);
     * g.actualizarPeso("D", "F", 8);
     * g.actualizarPeso("E", "F", 9);
     * g.actualizarPeso("E", "G", 10);
     * g.actualizarPeso("F", "G", 11);
     * g.actualizarPeso("F", "H", 12);
     * g.actualizarPeso("G", "H", 13);
     * g.actualizarPeso("G", "I", 14);
     * g.actualizarPeso("H", "I", 15);
     * g.actualizarPeso("H", "J", 16);
     * g.actualizarPeso("I", "J", 17);
     * g.actualizarPeso("I", "K", 18);
     * g.actualizarPeso("J", "K", 19);
     * g.actualizarPeso("J", "L", 20);
     * g.actualizarPeso("K", "L", 21);
     * g.actualizarPeso("K", "M", 22);
     * g.actualizarPeso("L", "M", 23);
     * g.actualizarPeso("L", "N", 24);
     * g.actualizarPeso("M", "N", 25);
     * g.actualizarPeso("M", "O", 26);
     * g.actualizarPeso("N", "O", 27);
     * g.actualizarPeso("N", "P", 28);
     * g.actualizarPeso("O", "P", 29);
     * g.actualizarPeso("O", "Q", 30);
     * g.actualizarPeso("P", "Q", 31);
     * g.actualizarPeso("P", "R", 32);
     * g.actualizarPeso("Q", "R", 33);
     * g.actualizarPeso("Q", "S", 34);
     * g.actualizarPeso("R", "S", 35);
     * g.actualizarPeso("R", "T", 36);
     * g.actualizarPeso("S", "T", 37);
     * g.actualizarPeso("S", "U", 38);
     * g.actualizarPeso("T", "U", 39);
     * g.actualizarPeso("T", "V", 40);
     * g.actualizarPeso("U", "V", 41);
     * g.actualizarPeso("U", "W", 42);
     * g.actualizarPeso("V", "W", 43);
     * g.actualizarPeso("V", "X", 44);
     * g.actualizarPeso("W", "X", 45);
     * g.actualizarPeso("W", "Y", 46);
     * g.actualizarPeso("X", "Y", 47);
     * g.actualizarPeso("X", "Z", 48);
     * g.actualizarPeso("Y", "Z", 49);
     * g.actualizarPeso("Y", "A", 50);
     * g.actualizarPeso("Z", "A", 51);
     * g.actualizarPeso("Z", "B", 52);
     * g.actualizarPeso("A", "B", 53);
     * } catch (Exception e) {
     * System.out.println(e.getMessage());
     * }
     * System.out.println(g.mostrarMatriz());
     * }
     */
}
