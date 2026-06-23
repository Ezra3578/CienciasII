
package binaria;

public class Binaria {
    public static void main(String[] args) {
        NumAleatorio num=new NumAleatorio(12,7,4,12); //semilla inicial, multiplicador, incSr, mod
        num.iteracionesConst(20);
        System.out.println("--------");
        num.iteracionesSeg(20);
    }
}