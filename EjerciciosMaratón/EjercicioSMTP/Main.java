import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer in = new StreamTokenizer(br);
        StringBuilder sb = new StringBuilder();

        in.nextToken();
        int N = (int) in.nval;

        for (int caso = 1; caso <= N; caso++) {
            in.nextToken(); int n = (int) in.nval;
            in.nextToken(); int m = (int) in.nval;
            in.nextToken(); int S = (int) in.nval;
            in.nextToken(); int T = (int) in.nval;

            ListaAdyacencia grafo = new ListaAdyacencia();

            // Agregar todos los nodos (0..n-1) como Strings
            for (int i = 0; i < n; i++) {
                grafo.agregarNodo(String.valueOf(i));
            }

            for (int i = 0; i < m; i++) {
                in.nextToken(); int u = (int) in.nval;
                in.nextToken(); int v = (int) in.nval;
                in.nextToken(); int w = (int) in.nval;

                String su = String.valueOf(u);
                String sv = String.valueOf(v);

                if (!grafo.existeArista(su, sv)) {
                    grafo.agregarArista(su, sv, w);
                } else {
                    // Manejo de aristas paralelas: quedarse con el menor peso
                    int pesoActual = grafo.getPesoArista(su, sv);
                    if (w < pesoActual) {
                        grafo.actualizarPesoArista(su, sv, w);
                    }
                }
            }

            Dijkstra dijkstra = new Dijkstra(grafo);
            String resultado = dijkstra.getDistancia(String.valueOf(S), String.valueOf(T));

            sb.append("Case #").append(caso).append(": ").append(resultado).append("\n");
        }

        System.out.print(sb);
    }
}