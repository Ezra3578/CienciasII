package ConvexHull;

public class Punto implements Comparable<Punto> {
    public final double x, y;

    public Punto(double x, double y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public int compareTo(Punto o) {
        if (this.x != o.x) return Double.compare(this.x, o.x);
        return Double.compare(this.y, o.y);
    }
    // ordena de arriba pa abajo porque cuando this es A da 2 > 0 (después) y si this es B da -2 < 0 (antes)
    // entonces si están enn el mismo X pone de primeras el de más a la izquierda
    // y si está en el mismo Y pone de primeras el de más a la derecha

    @Override
    public String toString() {
        return String.format("(%.2f, %.2f)", x, y);
    }
}