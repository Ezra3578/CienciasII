import math


class NodoB:
    def __init__(self, hoja=False):   # FIX: _init_ → __init__
        self.hoja = hoja
        self.claves = []
        self.hijos = []


class ArbolB:
    def __init__(self, m):            # FIX: _init_ → __init__
        self.m = m
        self.raiz = NodoB(True)

    # =====================================================
    # UTILIDADES
    # =====================================================
    def max_claves(self):
        return self.m - 1

    def min_claves(self):
        # FIX: math.ceil(m/2)-1 cubre correctamente m par e impar
        return math.ceil(self.m / 2) - 1

    # =====================================================
    # BÚSQUEDA
    # =====================================================
    def buscar(self, clave, nodo=None):
        if nodo is None:
            nodo = self.raiz

        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1

        if i < len(nodo.claves) and nodo.claves[i] == clave:
            return True

        if nodo.hoja:
            return False

        return self.buscar(clave, nodo.hijos[i])

    # =====================================================
    # INSERCIÓN
    # =====================================================
    def insertar(self, clave):
        raiz = self.raiz

        if len(raiz.claves) == self.max_claves():
            nueva = NodoB(False)
            nueva.hijos.append(raiz)
            self.raiz = nueva
            self.dividir_hijo(nueva, 0)
            self.insertar_no_lleno(nueva, clave)
        else:
            self.insertar_no_lleno(raiz, clave)

    def insertar_no_lleno(self, nodo, clave):
        i = len(nodo.claves) - 1

        if nodo.hoja:
            nodo.claves.append(None)
            # Duplicados van a la derecha: se avanza solo con '<' estricto
            while i >= 0 and clave < nodo.claves[i]:
                nodo.claves[i + 1] = nodo.claves[i]
                i -= 1
            nodo.claves[i + 1] = clave

        else:
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            i += 1

            if len(nodo.hijos[i].claves) == self.max_claves():
                self.dividir_hijo(nodo, i)
                # Duplicados van a la derecha: se avanza con '>='
                if clave >= nodo.claves[i]:
                    i += 1

            self.insertar_no_lleno(nodo.hijos[i], clave)

    def dividir_hijo(self, padre, i):
        m = self.m
        nodo = padre.hijos[i]
        nuevo = NodoB(nodo.hoja)

        medio = nodo.claves[m // 2]

        nuevo.claves = nodo.claves[m // 2 + 1:]
        nodo.claves = nodo.claves[:m // 2]

        if not nodo.hoja:
            nuevo.hijos = nodo.hijos[m // 2 + 1:]
            nodo.hijos = nodo.hijos[:m // 2 + 1]

        padre.claves.insert(i, medio)
        padre.hijos.insert(i + 1, nuevo)

    # =====================================================
    # ELIMINACIÓN
    # =====================================================
    def eliminar(self, clave):
        """Elimina 'clave' del árbol B.  Si hay duplicados, elimina una ocurrencia."""
        if not self.buscar(clave):
            print(f"  Clave {clave} no encontrada.")
            return
        self._eliminar(self.raiz, clave)

        # Si la raíz queda vacía y tiene un hijo, ese hijo pasa a ser la nueva raíz
        if len(self.raiz.claves) == 0 and not self.raiz.hoja:
            self.raiz = self.raiz.hijos[0]

    def _eliminar(self, nodo, clave):
        t = self.min_claves() + 1          # mínimo de claves + 1 = ceil(m/2)
        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1

        #Caso 1: la clave está en este nodo 
        if i < len(nodo.claves) and nodo.claves[i] == clave:

            if nodo.hoja:
                #Caso 1a: nodo hoja → eliminar directamente
                nodo.claves.pop(i)

            else:
                #Caso 1b: nodo interno → reemplazar con el predecesor
                # (nodo más a la DERECHA del subárbol IZQUIERDO)
                predecesor = self._predecesor(nodo.hijos[i])
                nodo.claves[i] = predecesor
                self._eliminar(nodo.hijos[i], predecesor)

        #Caso 2: la clave NO está en este nodo (no es hoja)
        else:
            if nodo.hoja:
                # No debería llegar aquí si buscar() funcionó, pero por si las moscas:
                return

            # ¿El hijo por donde bajar tiene suficientes claves?
            if len(nodo.hijos[i].claves) < t:
                self._rellenar(nodo, i)
                # Después de rellenar, el índice puede cambiar si se fusionó con el
                # hermano izquierdo (i se desplaza -1) o la clave subió/bajó.
                # Re-buscamos la posición correcta:
                i = 0
                while i < len(nodo.claves) and clave > nodo.claves[i]:
                    i += 1
                # Si la clave ahora está en nodo (fue traída al rellenar) la eliminamos aquí
                if i < len(nodo.claves) and nodo.claves[i] == clave:
                    if nodo.hoja:
                        nodo.claves.pop(i)
                        return
                    else:
                        predecesor = self._predecesor(nodo.hijos[i])
                        nodo.claves[i] = predecesor
                        self._eliminar(nodo.hijos[i], predecesor)
                        return

            self._eliminar(nodo.hijos[i], clave)

    def _predecesor(self, nodo):
        """Devuelve la clave más a la derecha del subárbol con raíz 'nodo'."""
        while not nodo.hoja:
            nodo = nodo.hijos[-1]
        return nodo.claves[-1]

    def _rellenar(self, padre, i):
        """Garantiza que padre.hijos[i] tenga al menos ceil(m/2) claves."""
        t = self.min_claves() + 1   # ceil(m/2)

        # Intentar rotar desde el hermano izquierdo
        if i > 0 and len(padre.hijos[i - 1].claves) >= t:
            self._rotar_derecha(padre, i)

        # Intentar rotar desde el hermano derecho
        elif i < len(padre.hijos) - 1 and len(padre.hijos[i + 1].claves) >= t:
            self._rotar_izquierda(padre, i)

        # Fusionar con un hermano
        else:
            if i < len(padre.hijos) - 1:
                self._fusionar(padre, i)
            else:
                self._fusionar(padre, i - 1)

    def _rotar_derecha(self, padre, i):
        """Presta una clave del hermano izquierdo (padre.hijos[i-1]) al hijo padre.hijos[i]."""
        hijo   = padre.hijos[i]
        herm   = padre.hijos[i - 1]

        # La clave separadora del padre baja al frente del hijo
        hijo.claves.insert(0, padre.claves[i - 1])

        # El último hijo del hermano pasa al frente del hijo (si no es hoja)
        if not herm.hoja:
            hijo.hijos.insert(0, herm.hijos.pop())

        # La clave más a la derecha del hermano sube al padre
        padre.claves[i - 1] = herm.claves.pop()

    def _rotar_izquierda(self, padre, i):
        """Presta una clave del hermano derecho (padre.hijos[i+1]) al hijo padre.hijos[i]."""
        hijo  = padre.hijos[i]
        herm  = padre.hijos[i + 1]

        # La clave separadora del padre baja al final del hijo
        hijo.claves.append(padre.claves[i])

        # El primer hijo del hermano pasa al final del hijo (si no es hoja)
        if not herm.hoja:
            hijo.hijos.append(herm.hijos.pop(0))

        # La clave más a la izquierda del hermano sube al padre
        padre.claves[i] = herm.claves.pop(0)

    def _fusionar(self, padre, i):
        """Fusiona padre.hijos[i] y padre.hijos[i+1], tomando padre.claves[i] como separador."""
        izq  = padre.hijos[i]
        der  = padre.hijos[i + 1]

        # La clave separadora del padre baja al nodo izquierdo
        izq.claves.append(padre.claves.pop(i))

        # Todas las claves e hijos del nodo derecho pasan al izquierdo
        izq.claves.extend(der.claves)
        izq.hijos.extend(der.hijos)

        # Eliminar el hijo derecho del padre
        padre.hijos.pop(i + 1)

    # =====================================================
    # IMPRESIÓN CON RAMAS
    # =====================================================
    # FIX: imprimir/_imprimir estaban fuera de la clase por indentación incorrecta
    def imprimir(self):
        self._imprimir(self.raiz, "", True)

    def _imprimir(self, nodo, prefijo, ultimo):
        if nodo is None or len(nodo.claves) == 0:
            return

        print(prefijo + ("└── " if ultimo else "├── ") +
              "[" + "|".join(map(str, nodo.claves)) + "]")

        nuevo_prefijo = prefijo + ("    " if ultimo else "│   ")

        for i, hijo in enumerate(nodo.hijos):
            self._imprimir(hijo, nuevo_prefijo, i == len(nodo.hijos) - 1)


# =====================================================
# PRUEBA
# =====================================================
if __name__ == "__main__":    # FIX: _name_ / _main_ → __name__ / "__main__"
    arbol = ArbolB(m=6)

    datos = [
        10, 20, 5, 6, 12,
        30, 7, 17, 20, 20,
        40, 50, 60, 70, 80
    ]

    print("INSERTANDO:")
    print("-" * 40)
    for d in datos:
        arbol.insertar(d)
        print(f"  Insertar {d:>3} -> raíz: {arbol.raiz.claves}")

    print("\nÁRBOL B:")
    arbol.imprimir()

    print("\nELIMINANDO:")
    print("-" * 40)
    for clave in [20, 6, 50, 10, 80]:
        print(f"\n  Eliminar {clave}:")
        arbol.eliminar(clave)
        arbol.imprimir()

    print("\nBÚSQUEDA:")
    print("-" * 40)
    for c in [17, 20, 99]:
        resultado = arbol.buscar(c)
        print(f"  buscar({c}) ->{'sí' if resultado else 'n0'}")
