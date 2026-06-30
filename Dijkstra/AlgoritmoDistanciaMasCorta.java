public interface AlgoritmoDistanciaMasCorta {
    public void calcularDistanciaMasCorta(String nodo_inicial);
    public String getDistancia(String nodo_inicial); //general desde un nodo
    public String getDistancia(String nodo_inicial, String nodo_destino); //de un nodo a otro, acá me aprovecho es de sobrecargar el método
    public String getCamino(String nodo_inicial);
    public String getCamino(String nodo_inicial, String nodo_destino);
}

/* NOTA IMPORTANTE: xfis eviten hacer prints desde las instancias de los algoritmos.
Los prints se hacen en el main, por eso esq estos métodos la mayoría retornan strings */