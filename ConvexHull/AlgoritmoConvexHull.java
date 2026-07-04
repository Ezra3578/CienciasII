package ConvexHull;

public interface AlgoritmoConvexHull {
    String encontrarConvexo(double[][] puntos);
    int getPasos();
    String getTextoPuntosEntrada(double[][] puntos);
}