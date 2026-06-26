package com.example;

import java.util.ArrayList;
import java.util.HashMap;

public class MatrizAdyacencia {

    // hashMap que tomará los nodos como clave y los nodos adyacentes con su peso como valor
    private  HashMap<String, HashMap<String, Integer>> nodos;

    private ArrayList<String> matriz;

   
    // inicializar nodos y matriz vacíos
    public MatrizAdyacencia() {
        this.nodos = new HashMap<>();
        this.matriz = new ArrayList<>();
    }
    

    //método recibe una arista con el par de nodos que invilucra y el peso 
    public void crearNodoYValor(String nodo1, String nodo2, Integer peso) throws Exception{

        if(!verificarNodos(nodo1, nodo2)){
            throw new Exception("el nodo no puede tener dos arista iguales o esa arista ya está en uso por otros nodos");
        }

        // ArrayList.contains() es O(n)
        if (!this.matriz.contains(nodo1)) this.matriz.add(nodo1);
        if (!this.matriz.contains(nodo2)) this.matriz.add(nodo2);
        


    // computeIfAbsent: si el nodo no existe lo crea, si ya existe lo deja
    // se pone de ambos lados para acceder desde cualquier nodo
        this.nodos.computeIfAbsent(nodo1, k -> new HashMap<>()).put(nodo2, peso);
        this.nodos.computeIfAbsent(nodo2, k -> new HashMap<>()).put(nodo1, peso);

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
        //si el hashmap contiene al nodo 1 entonces verifique si este tiene a nodo 2
        if (this.nodos.containsKey(nodo1)) {
            return !this.nodos.get(nodo1).containsKey(nodo2);
        }
        return true; // nodo1 ni siquiera existe aún → conexión válida
    }


    

    public static void main(String[] args) {
        System.out.println("Hello world!");
    }

}