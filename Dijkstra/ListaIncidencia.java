package com.example;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;
import java.util.Set;

public class ListaIncidencia {

    private List<Arista> lista;

    public ListaIncidencia() {
        this.lista = new ArrayList<>();
    }

    public boolean agregar(String nodo1, String nodo2, int peso) {
        //Si ya existe, retorna false
        if (aristaExiste(nodo1, nodo2)) {
            System.out.println("La conexion entre " + nodo1.toUpperCase() + " y " + nodo2.toUpperCase() + " ya existe.");
            return false;
        }
        lista.add(new Arista(nodo1, nodo2, peso));
        return true;
    }

    public boolean eliminarArista(String nodo1, String nodo2) {
        //Busca el indice en el ArrayList de una arista 
        int idx = indiceArista(nodo1, nodo2);
        if (idx != -1) {
            lista.remove(idx);
            return true;
        }
        return false;
    }

    public void eliminarNodo(String nodo) {
        //Formatear a mayúsculas
        String n = nodo.toUpperCase();

        //Elimina las aristas que contengan al nodo
        lista.removeIf(a -> a.getNodo1().equals(n) || a.getNodo2().equals(n));
    }

    public boolean aristaExiste(String nodo1, String nodo2) {
        //Si encuentra el indice retorna true
        return indiceArista(nodo1, nodo2) != -1;
    }

    public int getPeso(String nodo1, String nodo2) {
        int idx = indiceArista(nodo1, nodo2);

        //Si encuentra el indice, retorna el peso de la arista, si no, da -1
        return idx != -1 ? lista.get(idx).getPeso() : -1;
    }

    public List<String> vecinosString(String nodo) {
        String n = nodo.toUpperCase();
        List<String> vecinos = new ArrayList<>();
        for (Arista a : lista) {
            if (a.getNodo1().equals(n))      vecinos.add(a.getNodo2());
            else if (a.getNodo2().equals(n)) vecinos.add(a.getNodo1());
        }
        return vecinos;
    }

    public List<Arista> vecinosAristas(String nodo) {
        String n = nodo.toUpperCase();
        List<Arista> vecinos = new ArrayList<>();
        for (Arista a : lista) {
            if (a.getNodo1().equals(n) || a.getNodo2().equals(n))
                vecinos.add(a);
        }
        return vecinos;
    }

    public Set<String> getNodos() {
        Set<String> nodos = new HashSet<>();
        for (Arista a : lista) {
            nodos.add(a.getNodo1());
            nodos.add(a.getNodo2());
        }
        return nodos;
    }

    public int cantidadNodos()  { return getNodos().size(); }
    public int cantidadAristas() { return lista.size(); }

    private int indiceArista(String nodo1, String nodo2) {
        String n1 = nodo1.toUpperCase();
        String n2 = nodo2.toUpperCase();
        for (int i = 0; i < lista.size(); i++) {
            Arista a = lista.get(i);
            if ((a.getNodo1().equals(n1) && a.getNodo2().equals(n2))
             || (a.getNodo1().equals(n2) && a.getNodo2().equals(n1)))
                return i;
        }
        return -1;
    }

    // ********* MENÚS Y PSEUDOINTERFAZ DE USUARIO *********

    private Scanner scanner = new Scanner(System.in);

    // ─── Menús de AGREGAR ────────────────────────────────────────────────────────
    public void menuAgregarArista() {
        System.out.print("Ingrese el nombre del primer nodo: ");
        String nodo1 = scanner.nextLine();

        System.out.print("Ingrese el nombre del segundo nodo: ");
        String nodo2 = scanner.nextLine();

        if (nodo1.equalsIgnoreCase(nodo2)) {
            System.out.println("Error: los dos nodos no pueden ser el mismo.");
            return;
        }

        int peso = -1;
        do {
            System.out.print("Ingrese el peso de la arista (debe ser >= 0): ");
            while (!scanner.hasNextInt()) {
                System.out.println("Error: ingrese un número entero válido.");
                scanner.next();
            }
            peso = scanner.nextInt();
            scanner.nextLine(); // limpiar buffer
            if (peso < 0)
                System.out.println("Error: el peso no puede ser negativo.");
        } while (peso < 0);

        if (agregar(nodo1, nodo2, peso))
            System.out.println("Arista agregada exitosamente.");
    }

    // ─── Menús de ELIMINAR ───────────────────────────────────────────────────────

    public void menuEliminarArista() {
        System.out.print("Ingrese el nombre del primer nodo: ");
        String nodo1 = scanner.nextLine();

        System.out.print("Ingrese el nombre del segundo nodo: ");
        String nodo2 = scanner.nextLine();

        if (eliminarArista(nodo1, nodo2))
            System.out.println("Arista eliminada exitosamente.");
        else
            System.out.println("Error: la arista entre '" + nodo1.toUpperCase()
                            + "' y '" + nodo2.toUpperCase() + "' no existe.");
    }

    public void menuEliminarNodo() {
        System.out.print("Ingrese el nombre del nodo a eliminar: ");
        String nodo = scanner.nextLine();

        if (!getNodos().contains(nodo.toUpperCase())) {
            System.out.println("Error: el nodo '" + nodo.toUpperCase() + "' no existe.");
            return;
        }

        eliminarNodo(nodo);
        System.out.println("Nodo '" + nodo.toUpperCase()
                        + "' y todas sus aristas eliminados exitosamente.");
    }

    // ─── Menú de ACTUALIZAR ──────────────────────────────────────────────────────

    public void menuActualizarPeso() {
        System.out.print("Ingrese el nombre del primer nodo: ");
        String nodo1 = scanner.nextLine();

        System.out.print("Ingrese el nombre del segundo nodo: ");
        String nodo2 = scanner.nextLine();

        int idx = indiceArista(nodo1, nodo2);
        if (idx == -1) {
            System.out.println("Error: la arista entre '" + nodo1.toUpperCase()
                            + "' y '" + nodo2.toUpperCase() + "' no existe.");
            return;
        }

        int nuevoPeso = -1;
        do {
            System.out.print("Ingrese el nuevo peso (debe ser >= 0): ");
            while (!scanner.hasNextInt()) {
                System.out.println("Error: ingrese un número entero válido.");
                scanner.next();
            }
            nuevoPeso = scanner.nextInt();
            scanner.nextLine();
            if (nuevoPeso < 0)
                System.out.println("Error: el peso no puede ser negativo.");
        } while (nuevoPeso < 0);

        lista.get(idx).setPeso(nuevoPeso);
        System.out.println("Peso actualizado exitosamente.");
    }

    // ─── Menús de CONSULTA ───────────────────────────────────────────────────────

    public void menuConsultarVecinos() {
        System.out.print("Ingrese el nombre del nodo: ");
        String nodo = scanner.nextLine();

        if (!getNodos().contains(nodo.toUpperCase())) {
            System.out.println("Error: el nodo '" + nodo.toUpperCase() + "' no existe.");
            return;
        }

        List<String> vecinos = vecinosString(nodo);
        if (vecinos.isEmpty()) {
            System.out.println("El nodo '" + nodo.toUpperCase() + "' no tiene vecinos.");
            return;
        }

        System.out.println("Vecinos de '" + nodo.toUpperCase() + "':");
        for (String v : vecinos)
            System.out.println("  → " + v);
    }

    public void menuConsultarPeso() {
        System.out.print("Ingrese el nombre del primer nodo: ");
        String nodo1 = scanner.nextLine();

        System.out.print("Ingrese el nombre del segundo nodo: ");
        String nodo2 = scanner.nextLine();

        int peso = getPeso(nodo1, nodo2);
        if (peso == -1)
            System.out.println("Error: la arista entre '" + nodo1.toUpperCase()
                            + "' y '" + nodo2.toUpperCase() + "' no existe.");
        else
            System.out.println("Peso de la arista: " + peso);
    }

    public void mostrarEstadoGrafo() {
        System.out.println("\n=== ESTADO DEL GRAFO ===");
        System.out.println("Nodos  : " + cantidadNodos());
        System.out.println("Aristas: " + cantidadAristas());

        if (lista.isEmpty()) {
            System.out.println("El grafo está vacío.");
            return;
        }

        System.out.println("Conexiones:");
        for (Arista a : lista)
            System.out.println("  " + a.getNodo1() + " ── " + a.getNodo2()
                            + "  (peso: " + a.getPeso() + ")");
    }

    // ─── Menú principal ──────────────────────────────────────────────────────────

    public void mostrarMenuOpciones() {
        System.out.println("\n=== MENÚ DE OPCIONES ===");
        System.out.println("── Agregar ──────────────");
        System.out.println("  1. Agregar arista");
        System.out.println("── Eliminar ─────────────");
        System.out.println("  2. Eliminar arista");
        System.out.println("  3. Eliminar nodo");
        System.out.println("── Actualizar ───────────");
        System.out.println("  4. Actualizar peso de arista");
        System.out.println("── Consultar ────────────");
        System.out.println("  5. Ver vecinos de un nodo");
        System.out.println("  6. Consultar peso de arista");
        System.out.println("  7. Ver estado del grafo");
        System.out.println("─────────────────────────");
        System.out.println("  0. Salir");
        System.out.print("Seleccione una opción: ");
    }

    public void menu() {
        int opcion;
        do {
            mostrarMenuOpciones();
            while (!scanner.hasNextInt()) {
                System.out.println("Error: ingrese un número válido.");
                scanner.next();
            }
            opcion = scanner.nextInt();
            scanner.nextLine(); // limpiar buffer

            System.out.println();
            switch (opcion) {
                case 1  -> menuAgregarArista();
                case 2  -> menuEliminarArista();
                case 3  -> menuEliminarNodo();
                case 4  -> menuActualizarPeso();
                case 5  -> menuConsultarVecinos();
                case 6  -> menuConsultarPeso();
                case 7  -> mostrarEstadoGrafo();
                case 0  -> System.out.println("Saliendo del programa...");
                default -> System.out.println("Opción no válida. Intente de nuevo.");
            }
        } while (opcion != 0);

        scanner.close();
    }

    public static class Arista {
        private final String nodo1, nodo2;
        private int peso;

        public Arista(String nodo1, String nodo2, int peso) {
            this.nodo1 = nodo1.toUpperCase();
            this.nodo2 = nodo2.toUpperCase();
            this.peso  = peso;
        }

        public String getNodo1() { return nodo1; }
        public String getNodo2() { return nodo2; }
        public int    getPeso()  { return peso;  }
        public void   setPeso(int peso) { this.peso = peso; }

        /** Retorna el extremo opuesto al nodo dado, o null si no pertenece a la arista. */
        public String getOtroExtremo(String nodo) {
            nodo = nodo.toUpperCase();
            if (nodo1.equals(nodo)) return nodo2;
            if (nodo2.equals(nodo)) return nodo1;
            return null;
        }
    }
}