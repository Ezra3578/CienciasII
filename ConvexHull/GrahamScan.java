package ConvexHull;

import java.util.*;

public class GrahamScan implements AlgoritmoConvexHull{

    private int pasos=0;
    static class Punto{
        double x, y;

        // Constructor de punto
        Punto(double x, double y) {
            this.x = x;
            this.y = y;
        }
        @Override
        public String toString() {
            return String.format("(%.2f, %.2f)", x, y);
        }
    }
    
    private double orientacion (Punto punto1, Punto punto2, Punto punto3) {
        double productox=(punto1.x*(punto2.y-punto3.y)+punto2.x*(punto3.y-punto1.y)+punto3.x*(punto1.y-punto2.y));
        if(productox>0){
             return 1;
        }
        if(productox<0){
            return -1;
        }
        return 0;
    }
    private double compara (Punto punto1, Punto punto2, Punto puntoRef) {
        double orientacion=orientacion(punto1, punto2, puntoRef);
        if(orientacion==0){
            return distanciaCuadrada(puntoRef, punto1)-distanciaCuadrada(puntoRef, punto2);
        }
        return orientacion;
    }
    @Override
    public int getPasos() {
        return pasos;
    }
    private double distanciaCuadrada(Punto p1, Punto p2) {
        double deltaX = p1.x - p2.x;
        double deltaY = p1.y - p2.y;
        return (deltaX * deltaX) + (deltaY * deltaY);
    }
    private ArrayList<Punto> removerColineales(ArrayList<Punto> listaPuntos, Punto puntoRef) {
        final Punto puntoRefFinal = puntoRef;
        listaPuntos.sort((punto1,punto2) -> (int)compara(punto1,punto2,puntoRefFinal));
        //remover colineales
        int tamano = listaPuntos.size();
        int m=1;
        for (int j=0 ; j<tamano ; j++) {
            while (j<tamano-1 && orientacion(puntoRefFinal,listaPuntos.get(j), listaPuntos.get(j+1))==0){
                j++;
            }
            
            listaPuntos.set(m, listaPuntos.get(j));
            m++;
        }

        return new ArrayList<>(listaPuntos.subList(0, m));
    }
    @Override
    public String encontrarConvexo(double[][] puntos) {
        ArrayList<Punto> listaPuntos = new ArrayList<>();
        for (double[] p : puntos) {
            listaPuntos.add(new Punto(p[0], p[1]));
        }
        Punto puntoRef = listaPuntos.get(0);
        for (Punto p : listaPuntos) {
            if (p.y < puntoRef.y || (p.y == puntoRef.y && p.x < puntoRef.x)) {
                puntoRef = p;
            }
        }
        listaPuntos=removerColineales(listaPuntos, puntoRef);
        
        Stack<Punto> pila = new Stack<>();

        for (Punto p : listaPuntos) {

            // si el punto esta de forma contra reloj lo elimina
            while (pila.size() > 1 && orientacion(pila.get(pila.size() - 2), pila.peek(), p) >= 0){
                pila.pop();
            }
            //agregar punto
            pila.push(p);
        }
        if(pila.size()<3){
            return "Error: no se tienen suficientes puntos(más de 3, para una figura convexa";
        }else{

            return getTexto(pila);
        }
              
    }
    @Override
    public String getTexto(Stack<Punto> pila){
        int tamano=pila.size();
        StringBuilder texto = new StringBuilder();
        texto.append("Cantidad de pasos: ").append(getPasos()).append("\n");
        texto.append("Cantidad de vértices: ").append(tamano).append("\n");
        texto.append("Orden (sentido antihorario, empezando por el pivote):\n"); 
        for (int i = 0; i < tamano; i++) {
            texto.append(i + 1).append(". ").append(pila.get(i)).append("\n");
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
        
}
