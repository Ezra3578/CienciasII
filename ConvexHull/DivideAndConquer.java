package ConvexHull;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class DivideAndConquer implements AlgoritmoConvexHull{

    private int pasos = 0;

    // > 0: c está a la izquierda de a->b (giro antihorario)
    // < 0: c está a la derecha de a->b (giro horario)
    // = 0: colineales
    private double cross(Punto a, Punto b, Punto c) {
        return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
    }


    private int indexMaxX(Punto[] p) {
        int idx = 0;
        for (int i = 1; i < p.length; i++) {
            pasos++;
            if (p[i].x > p[idx].x) idx = i;
        }
        return idx;
    }

    private int indexMinX(Punto[] p) {
        int idx = 0;
        for (int i = 1; i < p.length; i++) {
            pasos++;
            if (p[i].x < p[idx].x) idx = i;
        }
        return idx;
    }

    private double distanciaCuadrada(Punto a, Punto b) {
        double dx = a.x - b.x, dy = a.y - b.y;
        return dx * dx + dy * dy;
    }

    //Hasta 3 puntos ordenados por X xD
    //Básicamente un Fuerza Bruta pero para un conjunto chiquito
    private Punto[] casoBase(Punto[] puntos) {
        if (puntos.length <= 2) {
            return puntos;
        }

        Punto pivote = puntos[0];
        for (Punto p : puntos) {
            pasos++;
            if (p.y < pivote.y || (p.y == pivote.y && p.x < pivote.x)) {
                pivote = p;
            }
        }

        List<Punto> hull = new ArrayList<>();
        Punto actual = pivote;
        do {
            hull.add(actual);
            Punto candidato = null;
            for (Punto p : puntos) {
                if (p == actual) continue;
                if (candidato == null) {
                    candidato = p;
                    continue;
                }
                double giro = cross(actual, candidato, p);
                pasos++;
                if (giro < 0 || (giro == 0 && distanciaCuadrada(actual, p) > distanciaCuadrada(actual, candidato))) {
                    candidato = p;
                }
            }
            actual = candidato;
        } while (actual != pivote && hull.size() <= puntos.length);

        return hull.toArray(new Punto[0]);
    }

    //La mezcla de los 2 envolventes convexos
    private Punto[] merge(Punto[] a, Punto[] b) {
        int n1 = a.length, n2 = b.length;

        int ia = indexMaxX(a); // punto más a la derecha de a
        int ib = indexMinX(b); // punto más a la izquierda de b

        // --- Tangente superior ---
        int inda = ia, indb = ib;
        boolean done = false;
        while (!done) {
            done = true;
            while (cross(b[indb], a[inda], a[(inda + 1) % n1]) <= 0) {
                inda = (inda + 1) % n1;
                pasos++;
            }
            while (cross(a[inda], b[indb], b[(indb - 1 + n2) % n2]) >= 0) {
                indb = (indb - 1 + n2) % n2;
                pasos++;
                done = false;
            }
        }
        int uppera = inda, upperb = indb;

        // --- Tangente inferior ---
        inda = ia;
        indb = ib;
        done = false;
        while (!done) {
            done = true;
            while (cross(a[inda], b[indb], b[(indb + 1) % n2]) <= 0) {
                indb = (indb + 1) % n2;
                pasos++;
            }
            while (cross(b[indb], a[inda], a[(inda - 1 + n1) % n1]) >= 0) {
                inda = (inda - 1 + n1) % n1;
                pasos++;
                done = false;
            }
        }
        int lowera = inda, lowerb = indb;

        // --- Ensamblar el hull combinado ---
        List<Punto> resultado = new ArrayList<>();
        int ind = uppera;
        resultado.add(a[uppera]);
        while (ind != lowera) {
            ind = (ind + 1) % n1;
            resultado.add(a[ind]);
            pasos++;
        }
        ind = lowerb;
        resultado.add(b[lowerb]);
        while (ind != upperb) {
            ind = (ind + 1) % n2;
            resultado.add(b[ind]);
            pasos++;
        }

        return resultado.toArray(new Punto[0]);
    }

    //Función Recursiva que divide el conjunto xD
    //(Aquí se puede elegir el mínimo de puntos por "subgrafo")
    private Punto[] dividir(Punto[] puntos) {
        pasos++;
        if (puntos.length <= 5) {
            return casoBase(puntos);
        }
        int mitad = puntos.length / 2;
        Punto[] izquierda = Arrays.copyOfRange(puntos, 0, mitad);
        Punto[] derecha = Arrays.copyOfRange(puntos, mitad, puntos.length);

        Punto[] hullIzq = dividir(izquierda);
        Punto[] hullDer = dividir(derecha);

        return merge(hullIzq, hullDer);
    }

    @Override
    public String encontrarConvexo(double[][] puntos) {
        pasos = 0;

        Punto[] points = new Punto[puntos.length];
        for (int i = 0; i < puntos.length; i++) {
            points[i] = new Punto(puntos[i][0], puntos[i][1]);
        }
        Arrays.sort(points);

        if (points.length < 3) {
            return "Error: no se tienen suficientes puntos(más de 3, para una figura convexa)";
        }

        Punto[] hull = dividir(points);

        if (hull.length < 3) {
            return "Error: no se tienen suficientes puntos(más de 3, para una figura convexa)";
        }

        return getTexto(hull);
    }

    private String getTexto(Punto[] hull) {
        StringBuilder texto = new StringBuilder();
        texto.append("Cantidad de pasos: ").append(getPasos()).append("\n");
        texto.append("Cantidad de vértices: ").append(hull.length).append("\n");
        texto.append("Orden (sentido antihorario):\n");
        for (int i = 0; i < hull.length; i++) {
            texto.append(i + 1).append(". ").append(hull[i]).append("\n");
        }
        return texto.toString();
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

    @Override
    public int getPasos() {
        return pasos;
    }
    
}
