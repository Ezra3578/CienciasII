package FlujoMaximo;

public interface RepresentacionGrafo {
    public void agregarNodo(String nombre_nodo);
    public void eliminarNodo(String nombre_nodo);
    public void agregarArista(String nombre_nodo1, String nombre_nodo2, int peso);
    public void eliminarArista(String nodo_origen, String nodo_destino);
    public void actualizarPesoArista(String nodo_origen, String nodo_destino, int nuevo_peso);

    //estas de acá las pongo pq yo las hice en lista de adyacencia, pero si es muy engorroso para los demás entonces las comentamos y no es necesario que las sobreescriban o las usen

    public boolean existeNodo(String nodo);
    public boolean existeArista(String nodo1, String nodo2);
}
