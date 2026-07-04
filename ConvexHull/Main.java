package ConvexHull;


public class Main {
    public static void main(String[] args) {
        double[][] puntos = {
            {0, 0}, {6, 0}, {8, 4}, {5, 8}, {1, 7},
            {2, 0}, {4, 0},{1,1}, {3,3}, {7, 2},
            {3, 3}, {4, 4}, {5, 5}, {2, 5}, {6, 6}, {3, 6}
        };
        // ================================
            // 1. GRAHAM SCAN
        // ================================
        GrahamScan grafo1= new GrahamScan();
        System.out.println(grafo1.getTextoPuntosEntrada(puntos));
        System.out.println("=== Casco Convexo (Graham Scan) ===");

        try {
            System.out.println(grafo1.encontrarConvexo(puntos));
        } catch (IllegalArgumentException | IllegalStateException e) {
            System.out.println("Error: " + e.getMessage());
        }

        // ================================
            // 2. MONOTONE CHAIN
        // ================================

        System.out.println("\n=== Casco Convexo (Monotone Chain) ===");
        MonotoneChain monChain = new MonotoneChain();
        System.out.println(monChain.encontrarConvexo(puntos));
    }

    
}
