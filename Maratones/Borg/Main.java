import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.*;

public class Main {
    /*PRUEBA
2
6 5
#####
#A#A##
# # A#
#S  ##
#####
7 7
#####
#AAA###
#    A#
# S ###
#     #
#AAA###
#####
*/
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String linea = br.readLine();
        if (linea == null) return;
        // numero de laberintos
        int N = Integer.parseInt(linea.trim());
        
        while (N-- > 0) {
            String lineaDimensiones = br.readLine();
            while (lineaDimensiones != null && lineaDimensiones.trim().isEmpty()) {
                lineaDimensiones = br.readLine();
            }
            
            //final break
            if (lineaDimensiones == null) break;
            
            String[] dimensiones = lineaDimensiones.trim().split("\\s+");
            int x = Integer.parseInt(dimensiones[0]);
            int y = Integer.parseInt(dimensiones[1]);
            
            char[][] laberinto = new char[y][x];
            List<int[]> coordenadasNodos = new ArrayList<>();
            
            // Leer el laberinto y tomar las coordenadas de S y A
            for (int i = 0; i < y; i++) {
                String fila = br.readLine();
                // si es vacia no hace nada
                if (fila == null) fila = ""; 
                
                for (int j = 0; j < x; j++) {
                    if (j < fila.length()) {
                        laberinto[i][j] = fila.charAt(j);
                    } else {
                        laberinto[i][j] = ' ';
                    }
                    
                    if (laberinto[i][j] == 'S' || laberinto[i][j] == 'A') {
                        coordenadasNodos.add(new int[]{i, j});
                    }
                }
            }
            
            int numNodos = coordenadasNodos.size();
            
            ListaAdyacencia grafo = new ListaAdyacencia();
            
            // creamos nodos
            for (int i = 0; i < numNodos; i++) {
                grafo.agregarNodo(String.valueOf(i));
            }
            
            int[] dirFila = {-1, 1, 0, 0};
            int[] dirCol = {0, 0, -1, 1};
            
            // rellenar listaAdyacencia
            for (int i = 0; i < numNodos; i++) {
                int[] inicio = coordenadasNodos.get(i);
                int[][] distancias = new int[y][x];
                for (int[] filaDist : distancias) Arrays.fill(filaDist, -1);
                
                Queue<int[]> cola = new LinkedList<>();
                cola.add(inicio);
                distancias[inicio[0]][inicio[1]] = 0;
                
                while (!cola.isEmpty()) {
                    int[] actual = cola.poll();
                    int f = actual[0];
                    int c = actual[1];
                    
                    for (int d = 0; d < 4; d++) {
                        int nf = f + dirFila[d];
                        int nc = c + dirCol[d];
                        
                        if (nf >= 0 && nf < y && nc >= 0 && nc < x && laberinto[nf][nc] != '#' && distancias[nf][nc] == -1) {
                            distancias[nf][nc] = distancias[f][c] + 1;
                            cola.add(new int[]{nf, nc});
                        }
                    }
                }
                
                // Conectamos el nodo actual i, con los alcanzables
                for (int j = i + 1; j < numNodos; j++) {
                    int[] destino = coordenadasNodos.get(j);
                    int pesoCamino = distancias[destino[0]][destino[1]];
                    
                    if (pesoCamino != -1) {
                        String u = String.valueOf(i);
                        String v = String.valueOf(j);
                        
                        grafo.agregarArista(u, v, pesoCamino);
                    }
                }
            }
            
            Kruskal kruskalAlg = new Kruskal(grafo);
            
            kruskalAlg.encontrarMSP("0");
            // Imprimimos el costo total
            System.out.println(kruskalAlg.getPesoTotal());
        }
    }
}