package ConvexHull;

import java.util.Arrays;

public class MonotoneChain implements AlgoritmoConvexHull{

    private static int pasos = 0;

    @Override
    public int getPasos() {
        return pasos;
    }

    //< 0: Los puntos hacen un giro hacia la derecha (sentido horario).
    //> 0: Los puntos hacen un giro hacia la izquierda (sentido antihorario).
    //= 0: Los tres puntos están alineados (colineales).
    private double cross(Punto p, Punto c, Punto n) {
        return (c.x - p.x) * (n.y - p.y) -
                (c.y - p.y) * (n.x - p.x);
    }

    private Punto[] convexHull(Punto[] puntos) {

        pasos = 0;

        if (puntos.length <= 1) return puntos;

        Punto[] sortedPoints = puntos.clone();
        Arrays.sort(sortedPoints);

        // lista de puntos envolventes
        Punto[] hull = new Punto[sortedPoints.length * 2];
        int k = 0;

        // Construir la mitad inferior del casco convexo
        for (Punto p : sortedPoints) {
            while (k >= 2 && cross(hull[k - 2], hull[k - 1], p) <= 0) {
                //Reemplaza el punto de la pos K hasta que deje de dar giro a la derecha xD
                k--;
                pasos++; //Paso de descartar punto xD
            }
            hull[k++] = p;
            pasos++; //Paso de insertarlo xD
        }

        // Construir la mitad superior del casco convexo
        for (int i = sortedPoints.length - 2, t = k + 1; i >= 0; i--) {
            Punto p = sortedPoints[i];
            while (k >= t && cross(hull[k - 2], hull[k - 1], p) <= 0) {
                //Lo mismo que arriba pero con giros a la izquierda xD
                k--;
                pasos++;
            }
            hull[k++] = p;
            pasos++;
        }

        // Recortar el array para eliminar los puntos sobrantes
        Punto[] result = new Punto[k - 1];

        //copiar el array hull desde la posición 0 hasta la posición k-1 en el array result porque el punto final se repite al cerrar el convex hull
        return Arrays.copyOfRange(hull, 0, k - 1);
    }

    @Override
    public String encontrarConvexo(double[][] puntos) {
        Punto[] points = new Punto[puntos.length];
        for (int i = 0; i < puntos.length; i++) {
            points[i] = new Punto(puntos[i][0], puntos[i][1]);
        }

        Punto[] hull = convexHull(points);

        if (hull.length < 3) {
            return "Error: no se tienen suficientes puntos(más de 3, para una figura convexa";
        }
        return getTexto(hull);
    }

    private String getTexto(Punto[] hull) {
        StringBuilder sb = new StringBuilder();
        sb.append("Cantidad de pasos: ").append(getPasos()).append("\n");
        sb.append("Cantidad de vértices: ").append(hull.length).append("\n");
        sb.append("Orden: ");
        for (Punto p : hull) {
            sb.append(p).append(" ");
        }
        sb.append("\n");
        return sb.toString();
    }

    @Override
    public String getTextoPuntosEntrada(double[][] puntos) {
        StringBuilder texto = new StringBuilder();
        texto.append("Puntos dados (").append(puntos.length).append("):\n");
        for (int i = 0; i < puntos.length; i++) {
            texto.append(i + 1).append(". (")
                .append(puntos[i][0]).append(", ")
                .append(puntos[i][1]).append(")\n");
        }
        return texto.toString();
    }

}