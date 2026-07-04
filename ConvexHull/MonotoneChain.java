package ConvexHull;

import java.util.Arrays;

public class MonotoneChain {

    private static long stepCount = 0;

    public static long getStepCount() {
        return stepCount;
    }

    //< 0: Los puntos hacen un giro hacia la derecha (sentido horario).
    //> 0: Los puntos hacen un giro hacia la izquierda (sentido antihorario).
    //= 0: Los tres puntos están alineados (colineales).

    public static long cross(Point p, Point c, Point n) {
        return (c.x - p.x) * (long) (n.y - p.y) -
                (c.y - p.y) * (long) (n.x - p.x);
    }

    public static Point[] convexHull(Point[] points) {

        stepCount = 0;

        if (points.length <= 1) return points;

        Point[] sortedPoints = points.clone();
        Arrays.sort(sortedPoints);

        // lista de puntos envolventes
        Point[] hull = new Point[sortedPoints.length * 2];
        int k = 0;

        // Construir la mitad inferior del casco convexo
        for (Point p : sortedPoints) {
            while (k >= 2 && cross(hull[k - 2], hull[k - 1], p) <= 0) {
                k--;
                stepCount++; //Paso de descartar punto xD
            }
            hull[k++] = p;
            stepCount++; //Paso de insertarlo xD
        }

        // k: 3

        // Construir la mitad superior del casco convexo
        for (int i = sortedPoints.length - 2, t = k + 1; i >= 0; i--) {
            Point p = sortedPoints[i];
            while (k >= t && cross(hull[k - 2], hull[k - 1], p) <= 0) {
                k--;
                stepCount++;
            }
            hull[k++] = p;
            stepCount++;
        }

        // Recortar el array para eliminar los puntos sobrantes
        Point[] result = new Point[k - 1];

        //copiar el array hull desde la posición 0 hasta la posición k-1 en el array result porque el punto final se repite al cerrar el convex hull
        return Arrays.copyOfRange(hull, 0, k - 1);
    }

    public static String printHullInfo(Point[] hull) {
        StringBuilder sb = new StringBuilder();

        sb.append("Hull (").append(hull.length).append(" puntos): ");
        for (Point p : hull) {
            sb.append(p).append(" ");
        }
        sb.append("\nPasos ejecutados: ").append(stepCount);

        return sb.toString();
    }

    public static class Point implements Comparable<Point>{
        public int x, y;

        public Point(int x, int y){
            this.x = x;
            this.y = y;
        }

        @Override
        public int compareTo(Point o) {
            if(this.x == o.x) return this.y - o.y;
            return this.x - o.x;
        }
        
        public String toString() {
            return "(" + x + "," + y + ")";
        }
    }
    // ordena de arriba pa abajo porque cuando this es A da 2 > 0 (después) y si this es B da -2 < 0 (antes)
    // entonces si están enn el mismo X pone de primeras el de más a la izquierda
    // y si está en el mismo Y pone de primeras el de más a la derecha

}