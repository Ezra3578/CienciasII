
package binaria;

public class Binaria {
    public static void main(String[] args) {
        NumAleatorio num=new NumAleatorio(12,11927,4,31); //semilla inicial, multiplicador, incSr, mod
        //num.iteracionesConst(500);
        System.out.println("--------");
        num.iteracionesSeg(500);

    }
}