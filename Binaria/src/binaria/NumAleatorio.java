package binaria;

import java.time.LocalDateTime;

public class NumAleatorio {
    
    private int semilla;
    private int multiplicador; //estatico o con segs
    private int incremento;
    private int modulo; 
    
    NumAleatorio(){
        semilla=5;
        multiplicador=3;
        incremento=1;
        modulo=30;
    }
    
    NumAleatorio(int semilla, int multiplicador, int incremento, int modulo){
        this.semilla=semilla;
        this.multiplicador=multiplicador;
        this.incremento=incremento;
        this.modulo=modulo;
    }

    public int getSemilla() {
        return semilla;
    }

    public int getMultiplicador() {
        return multiplicador;
    }

    public int getIncremento() {
        return incremento;
    }

    public int getModulo() {
        return modulo;
    }

    public void setSemilla(int semilla) {
        this.semilla = semilla;
    }

    public void setMultiplicador(int multiplicador) {
        this.multiplicador = multiplicador;
    }

    public void setIncremento(int incremento) {
        this.incremento = incremento;
    }

    public void setModulo(int modulo) {
        this.modulo = modulo;
    }
 
    private int obtenerSegundos(){
        LocalDateTime ya=LocalDateTime.now();
        int segundos=ya.getSecond();
        return segundos;
    }
    
    private int cifradoConstante(int semilla){
        int num_generado=(semilla*multiplicador+incremento)%modulo;
        return num_generado;
    }
    
    public void iteracionesConst(int n){
        for(int i=0; i<n; i++){
            int num=cifradoConstante(this.semilla);
            System.out.println(num);
            setSemilla(num);
        }
    }

    //Esta parte es porque se nos ocurrió variar uno de los parametros (el multiplicador) en base a los segundos actuales.
    
    private int cifradoSeg(int semilla){
        int num_generado=(semilla*obtenerSegundos()+ incremento)%modulo;
        return num_generado;
    }    
    
    public void iteracionesSeg(int n){
        for(int i=0; i<n; i++){
            int num=cifradoSeg(this.semilla);
            System.out.println(num);
            setSemilla(num);
            //setModulo(num/2+1);
            setIncremento(incremento+1);
        }
    }
    
}
