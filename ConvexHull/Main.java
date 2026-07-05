package ConvexHull;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Main {

        public static double[][] cargarPuntos(String rutaArchivo) throws IOException {
        List<double[]> lista = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(rutaArchivo))) {
            String linea;
            while ((linea = br.readLine()) != null) {
                linea = linea.trim();
                if (linea.isEmpty()) continue;

                String[] partes = linea.split(",");
                double x = Double.parseDouble(partes[0].trim());
                double y = Double.parseDouble(partes[1].trim());

                lista.add(new double[]{x, y});
            }
        }

        // Convertir la lista a arreglo double[][]
        double[][] puntos = new double[lista.size()][2];
        for (int i = 0; i < lista.size(); i++) {
            puntos[i] = lista.get(i);
        }

        return puntos;
    }

    public static void main(String[] args) throws IOException {
        double[][] puntos = {{0,0}}; //esto es pa k no joda ese java
        try {
            puntos = cargarPuntos("/workspaces/CienciasII/ConvexHull/puntos.csv");
            System.out.println("Puntos cargados: " + puntos.length);
            System.out.println("Primer punto: (" + puntos[0][0] + ", " + puntos[0][1] + ")");
            System.out.println("Último punto: (" + puntos[puntos.length - 1][0] + ", " + puntos[puntos.length - 1][1] + ")");
        } catch (IOException e) {
            System.err.println("pailas: " + e.getMessage());
        }
        
        // ================================
            // 1. GRAHAM SCAN
        // ================================
        GrahamScan grafo1= new GrahamScan();
        //System.out.println(grafo1.getTextoPuntosEntrada(puntos));
        System.out.println("=== Casco Convexo (Graham Scan) ===");

        try {
            String puntosGraham=grafo1.encontrarConvexo(puntos);
            guardarCSV(puntosGraham);
            System.out.println(puntosGraham);
            System.out.println("Pasos totales (Graham Scan): " + grafo1.getPasos());
        } catch (IllegalArgumentException | IllegalStateException e) {
            System.out.println("Error: " + e.getMessage());
        }

        // ================================
        // 2. MONOTONE CHAIN
        // ================================

        System.out.println("\n=== Casco Convexo (Monotone Chain) ===");
        MonotoneChain monChain = new MonotoneChain();
        String puntosMonChain=monChain.encontrarConvexo(puntos);
        guardarCSV(puntosMonChain);
        System.out.println(puntosMonChain);
        System.out.println("Pasos totales (Monotone Chain): " + monChain.getPasos());

        // ================================
        // 3. DIVIDE AND CONQUER
        // ================================

        System.out.println("\n=== Casco Convexo (Divide y Vencerás) ===");
        DivideAndConquer divAndCon = new DivideAndConquer();
        String puntosDivAndCon=divAndCon.encontrarConvexo(puntos);
        guardarCSV(puntosDivAndCon);
        System.out.println(puntosDivAndCon);
        System.out.println("Pasos totales (Divide y Vencerás): " + divAndCon.getPasos());
    }

    // Guarda una cadena con pares "x,y" en un CSV con nombre vertices_chN.csv
    // Si existe vertices_ch1.csv, usa vertices_ch2.csv, etc.
    public static String guardarCSV(String contenido) throws IOException {
        int n = 1;
        File f;
        do {
            f = new File(String.format("vertices_ch%d.csv", n));
            n++;
        } while (f.exists());

        try (BufferedWriter bw = new BufferedWriter(new FileWriter(f))) {
            // si la cadena no contiene cabecera, se asume que ya viene con líneas x,y
            bw.write(contenido);
            if (!contenido.endsWith(System.lineSeparator())) bw.newLine();
        }

        return f.getName();
    }

}

