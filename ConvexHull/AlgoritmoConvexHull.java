package ConvexHull;

import ConvexHull.GrahamScan.Punto;
import java.util.Stack;

public interface AlgoritmoConvexHull {
    public String encontrarConvexo(double[][] puntos);

    public String getTexto(Stack<Punto> pila);

    public int getPasos();
    
    public String getTextoPuntosEntrada(double[][] puntos);
}
