package ConvexHull;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class LectorPuntos {

    public static double[][] cargarPuntos(String rutaArchivo) throws IOException {
        List<double[]> lista = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(rutaArchivo))) {
            String linea;
            while ((linea = br.readLine()) != null) {
                linea = linea.trim();
                if (linea.isEmpty()) continue;

                String[] partes = linea.split(",");
                double x = Double.parseDouble(partes[0].trim());
                double y = Double.parseDouble(partes[1].trim());

                lista.add(new double[]{x, y});
            }
        }

        // Convertir la lista a arreglo double[][]
        double[][] puntos = new double[lista.size()][2];
        for (int i = 0; i < lista.size(); i++) {
            puntos[i] = lista.get(i);
        }

        return puntos;
    }
}
