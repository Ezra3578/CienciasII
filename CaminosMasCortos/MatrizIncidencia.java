import java.util.ArrayList;
import java.util.Arrays;

public class MatrizIncidencia {

    private int numVertices;

    // Cada elemento representa una arista
    private ArrayList<int[]> matrizInc;

    // Nombres de vértices
    private ArrayList<String> nombresVertices;

    // Nombres de aristas
    private ArrayList<String> nombresAristas;

    // Constructor con cantidad de vértices
    public MatrizIncidencia(int numVertices) {
        this.numVertices = numVertices;
        this.matrizInc = new ArrayList<>();
        this.nombresVertices = new ArrayList<>();
        this.nombresAristas = new ArrayList<>();

        for (int i = 0; i < numVertices; i++) {
            nombresVertices.add("V" + i);
        }
    }

    // Constructor con nombres de vértices
    public MatrizIncidencia(String[] vertices) {
        this.numVertices = vertices.length;
        this.matrizInc = new ArrayList<>();
        this.nombresVertices = new ArrayList<>();
        this.nombresAristas = new ArrayList<>();

        for (String v : vertices) {
            nombresVertices.add(v);
        }
    }

    // ADICIONAR ARISTA
    public void adicionarArista(String nombreArista,String origen,String destino,int peso) {

    int idxOrigen = nombresVertices.indexOf(origen);
    int idxDestino = nombresVertices.indexOf(destino);

    if (idxOrigen == -1 || idxDestino == -1) {

        System.out.println("Error: uno o ambos vértices no existen.");
        return;
    }

    int[] nuevaArista = new int[numVertices];

    nuevaArista[idxOrigen] = peso;
    nuevaArista[idxDestino] = peso;

    matrizInc.add(nuevaArista);
    nombresAristas.add(nombreArista);

    System.out.println(
            "Arista " + nombreArista +
            " añadida entre " +
            origen + " y " +
            destino +
            " con peso " + peso
    );
    
    }
    // ELIMINAR ARISTA
    public void eliminarArista(int origen, int destino) {

        int indiceEliminar = -1;

        for (int i = 0; i < matrizInc.size(); i++) {

            int[] arista = matrizInc.get(i);

            if (arista[origen] != 0 &&
                arista[destino] != 0) {

                indiceEliminar = i;
                break;
            }
        }

        if (indiceEliminar != -1) {

            String nombreArista =
                    nombresAristas.get(indiceEliminar);

            matrizInc.remove(indiceEliminar);
            nombresAristas.remove(indiceEliminar);

            System.out.println(
                    "Arista eliminada: " + nombreArista
            );
        } else {
            System.out.println("Arista no encontrada.");
        }
    }

    // ACTUALIZAR PESO
    public void actualizarPeso(String origen,String destino,int nuevoPeso) {

    int idxOrigen = nombresVertices.indexOf(origen);
    int idxDestino = nombresVertices.indexOf(destino);

    if (idxOrigen == -1 || idxDestino == -1) {

        System.out.println("Error: uno o ambos vértices no existen.");
        return;
    }

    boolean encontrada = false;

    for (int[] arista : matrizInc) {

        if (arista[idxOrigen] != 0 &&
            arista[idxDestino] != 0) {

            arista[idxOrigen] = nuevoPeso;
            arista[idxDestino] = nuevoPeso;

            encontrada = true;

            System.out.println(
                    "Peso actualizado entre " +
                    origen + " y " +
                    destino +
                    " a " + nuevoPeso
            );

            break;
        }
    }

    if (!encontrada) {

        System.out.println(
                "No existe una arista entre " +
                origen + " y " +
                destino
        );
    }
}

    // ADICIONAR VÉRTICE
    public void adicionarVertice(String nombre) {

        numVertices++;

        for (int i = 0; i < matrizInc.size(); i++) {

            matrizInc.set(
                    i,
                    Arrays.copyOf(
                            matrizInc.get(i),
                            numVertices
                    )
            );
        }

        nombresVertices.add(nombre);

        System.out.println(
                "Vertice agregado: " + nombre
        );
    }


    // ELIMINAR VÉRTICE
    public void eliminarVertice(String nombreVertice) {
        int verticeAEliminar = nombresVertices.indexOf(nombreVertice);

        if (verticeAEliminar == -1) {
            System.out.println(
            "No existe el vértice: " +
            nombreVertice
        );
            return;
        }

        // Eliminar aristas incidentes
        for (int i = matrizInc.size() - 1; i >= 0; i--) {

            if (matrizInc.get(i)[verticeAEliminar] != 0) {
                matrizInc.remove(i);
                nombresAristas.remove(i);
            }
        }

        // Redimensionar las aristas restantes
        for (int i = 0; i < matrizInc.size(); i++) {

            int[] vieja = matrizInc.get(i);

            int[] nueva = new int[numVertices - 1];

        int indice = 0;

        for (int j = 0; j < numVertices; j++) {

            if (j != verticeAEliminar) {
                nueva[indice++] = vieja[j];
            }
        }
            matrizInc.set(i, nueva);
        }

        nombresVertices.remove(verticeAEliminar);

        numVertices--;

            System.out.println(
            "Vertice eliminado: " +
            nombreVertice
        );
        }


    // MOSTRAR MATRIZ
    public void mostrarMatriz() {

        System.out.println(
                "\n========== MATRIZ DE INCIDENCIA =========="
        );

        // Encabezado
        System.out.printf("%-15s", "");

        for (String nombre : nombresVertices) {
            System.out.printf("%-15s", nombre);
        }

        System.out.println();

        // Filas (aristas)
        for (int i = 0; i < matrizInc.size(); i++) {

            System.out.printf(
                    "%-15s",
                    nombresAristas.get(i)
            );

            int[] arista = matrizInc.get(i);

            for (int valor : arista) {
                System.out.printf(
                        "%-15d",
                        valor
                );
            }

            System.out.println();
        }

        System.out.println();
    }

    // OBTENER CANTIDAD DE VÉRTICES
    public int getNumVertices() {
        return numVertices;
    }

    // OBTENER CANTIDAD DE ARISTAS
    public int getNumAristas() {
        return matrizInc.size();
    }
    
    //OBTENER EL INDICE DEL VERTICE POR EL NOMBRE
    private int obtenerIndiceVertice(String nombre) {

    int indice = nombresVertices.indexOf(nombre);

    if (indice == -1) {

        throw new IllegalArgumentException(
                "No existe el vértice: " + nombre
        );
    }

    return indice;
    }

}
