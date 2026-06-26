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


    // *********FUNCIONES DE NODOS Y ARISTAS*********

    //Agregaciones:

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
        if(!existeNodo(nodo1) || !existeNodo(nodo2)){
            System.out.println("Error: Uno o ambos nodos no existen en la lista de adyacencia.");
            return;
        }

        else if(nodo1 == nodo2){
            System.out.println("Error: No se puede agregar una arista entre un nodo y sí mismo.");
            return;
        }

        else{
            if(peso < 0){
                System.out.println("Error: El peso de la arista no puede ser negativo.");
                return;
            }
        adjList.get(nodo1).put(nodo2, peso);
        adjList.get(nodo2).put(nodo1, peso);
        }
    }



    // Eliminaciones:

    public void eliminarNodo(String nodo) {
        if(!existeNodo(nodo)){
            System.out.println("Error: El nodo no existe en la lista de adyacencia.");
            return;
        }
        else{
            adjList.remove(nodo);
            for(HashMap<String, Integer> conexiones : adjList.values()) {
                conexiones.remove(nodo);
            }
        }
    }

    public void eliminarArista(String nodo1, String nodo2) {
        if(!existeNodo(nodo1) || !existeNodo(nodo2)){
            System.out.println("Error: Uno o ambos nodos no existen en la lista de adyacencia.");
            return;
        }
        if(!existeArista(nodo1, nodo2)){
            System.out.println("Error: La arista no existe en la lista de adyacencia.");
            return;
        }
        adjList.get(nodo1).remove(nodo2);
        adjList.get(nodo2).remove(nodo1);
    }



    // Actualizaciones:

    public void actualizarPesoArista(String nodo1, String nodo2, int nuevoPeso) {
        if(!existeNodo(nodo1) || !existeNodo(nodo2)){
            System.out.println("Error: Uno o ambos nodos no existen en la lista de adyacencia.");
            return;
        }
        if(!existeArista(nodo1, nodo2)){
            System.out.println("Error: La arista no existe en la lista de adyacencia.");
            return;
        }
        if(nuevoPeso < 0){
            System.out.println("Error: El peso de la arista no puede ser negativo.");
            return;
        }
        adjList.get(nodo1).replace(nodo2, nuevoPeso);
        adjList.get(nodo2).replace(nodo1, nuevoPeso);
    }


    //Verificaciones:

    public boolean existeNodo(String nodo) {
        return adjList.containsKey(nodo);
    }

    public boolean existeArista(String nodo1, String nodo2) {
        return adjList.get(nodo1).containsKey(nodo2);
    }

    //getters:

    public HashMap<String, HashMap<String, Integer>> getAdjList() {
        return adjList;
    }

    public HashMap<String, Integer> getConexiones(String nodo) {
        return adjList.get(nodo);
    }

    public Integer getPesoArista(String nodo1, String nodo2) {
        return adjList.get(nodo1).get(nodo2);
    }

    public int getGrado(String nodo) {
        return adjList.get(nodo).size();
    }

    public Set<String> getNodos(){
        return adjList.keySet();
    }

    public Set<String> getAristasDeUnNodo(String nodo){
        return adjList.get(nodo).keySet();
    }

    //imprimir cosas:

    public void imprimirListaNodos(){
        for(String nodo : getNodos()){
            System.out.println(nodo);
        }
    }

    public void imprimirAristasDeUnNodo(String nodo){
        for(String arista : getAristasDeUnNodo(nodo)){
            System.out.println(arista);
        }
    }

    public void imprimirPesoAristasDeUnNodo(String nodo){
        for(String arista : getAristasDeUnNodo(nodo)){
            System.out.println("Peso de la arista " + arista + ": " + getPesoArista(nodo, arista));
        }
    }

    public void imprimirGradoDeUnNodo(String nodo){
        System.out.println("Grado del nodo " + nodo + ": " + getGrado(nodo));
    }

    public void imprimirListaAdjacencia(){
        for(String nodo : getNodos()){
            System.out.println("Nodo: " + nodo);
            imprimirAristasDeUnNodo(nodo);
        }
    }

    public void imprimirConexiones(){
        for(String nodo : getNodos()){
            System.out.println("Nodo: " + nodo);
            imprimirPesoAristasDeUnNodo(nodo);
        }
    }

    // *********MENUS Y COSAS DE PSEUDOINTERFAZ DE USUARIO*********

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

    //hacer menus de eliminaciones y actualizaciones (de act solo el cambio de peso de una arista)

    public void mostrarMenuOpciones(){ //Las opcioncitas del menucito, esto solo las imprime, añadir las de eliminación y actialuzación
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