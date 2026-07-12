import math

#Comentarios para los que usen esta clase:
#Pueden usar directamente: getMatrizDistancias() para obtener el dict de todas las distancias con el formato indicado en el método
#getDistancia(self, nodo_inicial, nodo_destino=None) Obtiene las distancias del nodo indicado a cualquier otro o un destino
#getCamino obtiene el camino hallado por el algoritmo (este camino se halla con getCaminoLista xD)

class FloydWarshall:
    
    def __init__(self, grafo):
        self.grafo = grafo  #Es el grafo que recibe del front generado xD
        self.nodos = [] #Lista de los nodos del grafo
        self.distancias = {}    #Son las distancias que retornara entre los nodos xD. Notación -> distancia[i][j] nodo i al nodo j
        self.siguiente = {}   #Maneja los próximos nodos para el camino más corto en el alg. xD
        self.pasos = 0  #Contador de pasos
        
        self.calculado = False  #Flag para saber si ya se usó o no xD

    #Método principal del alg.
    def calcularTodasLasDistancias(self):
        self.nodos = list(self.grafo.getMatriz())   #Se llena la lista con los nodos
        nodos_dict = self.grafo.getNodos()  #Se hace un diccionario de los nodos
        self.pasos = 0  #Reiniciar pasos xD


        #---Aquí se inicializa todo xD para el alg --- (distancias con vecinos, propias y no directas)

        #Se inicializan las distancias según las conexiones, para cada nodo crea un dict y pone todo en inf
        self.distancias = {i: {j: math.inf for j in self.nodos} for i in self.nodos}
        self.siguiente = {i: {j: None for j in self.nodos} for i in self.nodos} #Lo mismo pero pone todo en None (sin siguiente xD)

        for i in self.nodos:
            self.distancias[i][i] = 0   #Pone la distancia del nodo consigo mismo en 0
            self.siguiente[i][i] = i    #El siguiente nodo de si mismo, es "el mismo" (suena raro pero ajá xD)

            for vecino, peso in nodos_dict.get(i, {}).items():  #Obtiene los pesos para cada vecino como tuplas
                if vecino in self.distancias[i]:                #Si el vecino está guardado
                    self.distancias[i][vecino] = peso           #Le asigna el peso a la conexión
                    self.siguiente[i][vecino] = vecino          #Ubica esta arista como el mejor paso hasta el momento xD

        #Parte principal del algoritmo xD
        #k es un nodo intermedio, que comprueba si es mejor este paso desde i hacia j
        for k in self.nodos:
            for i in self.nodos:
                for j in self.nodos:
                    self.pasos += 1

                    #Si la distancia de i->k + la distancia de k->j es menor que la actual registrada
                    if self.distancias[i][k] + self.distancias[k][j] < self.distancias[i][j]:
                        self.distancias[i][j] = self.distancias[i][k] + self.distancias[k][j]   #Se cambia la distancia actual por esta nueva
                        self.siguiente[i][j] = self.siguiente[i][k] #Se pone este nodo como el siguiente para i->j
 
        self._calculado = True  #Acabo el algoritmo :D

    #Para ejecutar el algoritmo si aun no lo está (evitar errorcitos) xD
    def _asegurarCalculado(self):
        if not self._calculado:
            self.calcularTodasLasDistancias()

    #Retorna la "matriz" de las distancias (es un dict de la siguiente forma:
    #{origen: {destino: distancia, ...}, ...})
    def getMatrizDistancias(self):
        self._asegurarCalculado()
        return self.distancias
    
    #Obtiene una distancia especifica o todas las del nodo indicado
    def getDistancia(self, nodo_inicial, nodo_destino=None):
        
        #Si el nodo no existe xD
        if not self.grafo.existeNodo(nodo_inicial):
            return "Error: El nodo de inicio no existe en el grafo."

        #Si el destino no existe xD
        if nodo_destino is not None and not self.grafo.existeNodo(nodo_destino):
            return "Error: Al menos uno de sus nodos no existe en el grafo."

        #Ejecuta el algoritmo en caso de que no lo esté aún
        self._asegurarCalculado()

        #Si no hay destino, devuelve todas las distancias de el nodo indicado
        if nodo_destino is None:
            resultado = f"Distancias desde el nodo {nodo_inicial}:\n"
            for nodo in self.nodos:
                dist = self.distancias[nodo_inicial][nodo]
                if dist == math.inf:
                    resultado += f"{nodo}: INFINITO (no alcanzable)\n"
                else:
                    resultado += f"{nodo}: {dist}\n"
            return resultado

        #Si no devuelve su distancia o inf
        dist = self.distancias[nodo_inicial][nodo_destino]
        if dist == math.inf:
            return f"No existe camino entre {nodo_inicial} y {nodo_destino}."
        return f"Distancia entre {nodo_inicial} y {nodo_destino}: {dist}"
    
    def getCaminoLista(self, nodo_inicial, nodo_destino):
        """
        Igual que en Dijkstra.py: devuelve el camino como lista de nombres
        ['A', 'B', 'C'] en vez de string. Reconstruye usando la matriz
        `siguiente` (estándar para Floyd-Warshall, ya que no hay
        "predecesores" de un único origen sino de cada par).
        """
        if not self.grafo.existeNodo(nodo_inicial) or not self.grafo.existeNodo(nodo_destino):
            return []
 
        self._asegurarCalculado()
 
        if self.siguiente[nodo_inicial][nodo_destino] is None:
            return []
 
        camino = [nodo_inicial]
        actual = nodo_inicial
        while actual != nodo_destino:
            actual = self.siguiente[actual][nodo_destino]
            camino.append(actual)
        return camino
    

    #Estos métodos son para obtener el camino que conforma dicha ruta más corta xD
    #Formato: Nodo_origen -> Nodo_destino : Nodo_origen -> Nodo_paso1 -> ... -> Nodo_pasoN -> Nodo_destino
    def getCamino(self, nodo_inicial, nodo_destino=None):
        """
        Igual firma/comportamiento que Dijkstra.getCamino:
        - getCamino(nodo_inicial)                -> todos los caminos desde nodo_inicial
        - getCamino(nodo_inicial, nodo_destino)   -> un camino puntual
        """
        if not self.grafo.existeNodo(nodo_inicial):
            return "Error: El nodo de inicio no existe en el grafo."
        if nodo_destino is not None and not self.grafo.existeNodo(nodo_destino):
            return "Error: Al menos uno de sus nodos no existe en el grafo."
 
        self._asegurarCalculado()
 
        if nodo_destino is None:
            resultado = ""
            for nodo in self.nodos:
                if nodo == nodo_inicial:
                    continue
                camino = self.getCaminoLista(nodo_inicial, nodo)
                texto_camino = " -> ".join(camino) if camino else "No existe camino"
                resultado += f"{nodo_inicial} -> {nodo}: {texto_camino}\n"
            return resultado
 
        camino = self.getCaminoLista(nodo_inicial, nodo_destino)
        return " -> ".join(camino) if camino else "No existe camino"
    
    def getPasos(self):
        return self.pasos