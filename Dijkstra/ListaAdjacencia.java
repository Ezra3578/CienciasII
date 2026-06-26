import java.util.HashMap;
import java.util.*;

public class ListaAdjacencia{

    //ESTRUCTURA DE ESTE COSO
    //{nodo con conexión: {nodo conectado: peso} }
                //Ejemplo: {"A": {"B": 5, "C": 10}, "B": {"A": 5, "C": 3}, "C": {"A": 10, "B": 3}}
    private HashMap<String, HashMap<String, Integer>> adjList;

    ListaAdjacencia(){
        this.adjList = new HashMap<>();
    }

    public boolean agregarNodo(String nodo) {
        if(!adjList.containsKey(nodo)){
            adjList.put(nodo, new HashMap<>());
            return true;
        }
        else{
            System.out.println("Error: El nodo ya existe en la lista de adyacencia.");
            return false;
        }

    }

    public void agregarArista(String nodo1, String nodo2, int peso) {
        adjList.get(nodo1).put(nodo2, peso);
        adjList.get(nodo2).put(nodo1, peso);
    }

   public void menuAgregarNodo() {
    do{
        Scanner scanner = new Scanner(System.in);
        System.out.print("Ingrese el nombre del nodo: ");
        String nodo = scanner.nextLine();       
       }while(!agregarNodo(nodo);) //tomar con pinzas, tal vez esto de acá pueda dar fallos
   }

   public void menuAgregarArista() { //ponerle excepciones como que nos nodos no existen, los ponderados son negativos etc
        Scanner scanner = new Scanner(System.in);
        System.out.print("Ingrese el nombre del primer nodo: ");
        String nodo1 = scanner.nextLine();
        System.out.print("Ingrese el nombre del segundo nodo: ");
        String nodo2 = scanner.nextLine();
        System.out.print("Ingrese el peso de la arista: ");
        int peso = scanner.nextInt();
        agregarArista(nodo1, nodo2, peso);
    }

    public void mostrarMenuOpciones(){ //Las opcioncitas del menucito, esto solo las imprime
        System.out.println("=== MENÚ DE OPCIONES ===");
        System.out.println("1. Agregar nodo");
        System.out.println("2. Agregar arista");
        System.out.println("3. Salir");
        System.out.println("Seleccione una opción: ");
    }

    public void menu(){ //ya se puede seleccionar las opciones acá
        boolean estado=true;
        Scanner scanner = new Scanner(System.in);
        int opcion;

        do{
            mostrarMenuOpciones();
            opcion = scanner.nextInt();
            switch(opcion){
                case 1:
                    menuAgregarNodo();
                    break;
                case 2:
                    menuAgregarArista();
                    break;
                case 3:
                    System.out.println("Saliendo del programa...");
                    estado=false;
                    break;
                default:
                    System.out.println("Opción no válida. Intente de nuevo.");
            }
        }while(estado);
    }
}