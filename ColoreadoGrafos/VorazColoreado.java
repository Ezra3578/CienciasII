package ColoreadoGrafos;

import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class VorazColoreado implements AlgoritmoColoreadoGrafos{
    private int pasos;
    private int numColores;
    ListaAdyacencia grafo;
    private Map<String, Integer> grafoColoreado;
    
    public VorazColoreado(ListaAdyacencia grafo){
        this.grafo=grafo;
        this.pasos=0;
    }
    @Override
    public void colorear(){
        this.grafoColoreado=new HashMap<>();
        //initializacion en valores 0
        for (String v : this.grafo.getNodos()) {
            this.grafoColoreado.put(v, 0);
        }
        for(String n: this.grafo.getNodos()){
            Set<Integer> coloresVecinos = new HashSet<>();
            for(String vecino: this.grafo.getConexiones(n).keySet()){
                int colorTemp=this.grafoColoreado.get(vecino);
                pasos++;
                if(colorTemp!=0){
                    coloresVecinos.add(colorTemp);
                }
            }
            int i;
            for(i=1;coloresVecinos.contains(i);i++ ){
                pasos++;
            }
            this.grafoColoreado.put(n,i);
        }
        this.numColores=Collections.max(this.grafoColoreado.values());
    }    
    @Override
    public int getPasos(){
        return pasos;
    }
    public String imprimir(){
        if (this.grafoColoreado == null) {
            return "Aún no se ha ejecutado el algoritmo de coloración.";
        }

        StringBuilder sb = new StringBuilder();
        sb.append("Coloración obtenida con el algoritmo Secuencial Básico:\n");

        for (String nodo : this.grafo.getNodos()) {
            sb.append("Nodo ").append(nodo);
            sb.append(" -> Color ").append(this.grafoColoreado.get(nodo));
            sb.append("\n");
        }

        sb.append("Número colores: ").append(this.numColores);
        sb.append("\n");
        sb.append("Número de pasos: ").append(this.getPasos());

        return sb.toString();
    }
}
