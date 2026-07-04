package ConvexHull;

import java.util.Stack;

import ConvexHull.GrahamScan.Punto;

public interface AlgoritmoConvexHull {
    public String encontrarConvexo(double[][] puntos);

    public String getTexto(Stack<Punto> pila);

    public int getPasos();
    
    public String getTextoPuntosEntrada(double[][] puntos);
}
