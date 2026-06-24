import math


class NodoBPlus:
    def __init__(self, hoja=False):
        self.hoja = hoja
        self.claves = []
        self.hijos = []
        self.siguiente = None
        self.anterior = None
        self.padre = None       # referencia al padre


class ArbolBPlus:
    def __init__(self, m):
        self.m = m
        self.max_claves = m - 1
        self.min_claves = math.ceil(m / 2) - 1
        self.raiz = NodoBPlus(True)

    def insertar(self, k):
        resultado = self._insertar_rec(self.raiz, k)

        if resultado is not None:

            promovida, izq, der = resultado

            nueva_raiz = NodoBPlus(False)
            nueva_raiz.claves = [promovida]
            nueva_raiz.hijos = [izq, der]
            izq.padre = nueva_raiz
            der.padre = nueva_raiz

            self.raiz = nueva_raiz

    def _insertar_rec(self, nodo, k):

        if nodo.hoja:

            i = 0

            while i < len(nodo.claves) and nodo.claves[i] <= k:
                i += 1

            nodo.claves.insert(i, k)

        else:

            i = 0

            while i < len(nodo.claves) and k >= nodo.claves[i]:
                i += 1

            resultado = self._insertar_rec(nodo.hijos[i], k)

            if resultado is not None:

                promovida, izq, der = resultado

                nodo.claves.insert(i, promovida)

                nodo.hijos[i] = izq
                nodo.hijos.insert(i + 1, der)
                izq.padre = nodo
                der.padre = nodo

        if len(nodo.claves) > self.max_claves:
            return self.dividir_overflow(nodo)

        return None

    def dividir_overflow(self, nodo):
        total = len(nodo.claves)
        medio = total // 2

        if nodo.hoja:
            # ---- División de HOJA (clave en medio queda DUPLICADA hacia arriba) ----
            izq = NodoBPlus(True)
            der = NodoBPlus(True)

            izq.claves = nodo.claves[:medio]
            der.claves = nodo.claves[medio:]   # la clave de en medio SÍ queda en der

            # tanto el puntero ENTRANTE (de la hoja anterior) como el SALIENTE.
            anterior = nodo.anterior
            siguiente = nodo.siguiente

            if anterior is not None:
                anterior.siguiente = izq
            izq.anterior = anterior

            izq.siguiente = der
            der.anterior = izq

            der.siguiente = siguiente
            if siguiente is not None:
                siguiente.anterior = der

            promovida = der.claves[0]  # se copia, no se borra de la hoja

            return promovida, izq, der

        else:
            # ---- División de NODO INTERNO (clave de en medio SÍ se quita, como en B) ----
            promovida = nodo.claves[medio]

            izq = NodoBPlus(False)
            der = NodoBPlus(False)

            izq.claves = nodo.claves[:medio]
            der.claves = nodo.claves[medio + 1:]

            izq.hijos = nodo.hijos[:medio + 1]
            der.hijos = nodo.hijos[medio + 1:]

            for h in izq.hijos:
                h.padre = izq
            for h in der.hijos:
                h.padre = der

            return promovida, izq, der

    def buscar(self, k):
        nodo = self.raiz

        while not nodo.hoja:
            i = 0
            while i < len(nodo.claves) and k >= nodo.claves[i]:
                i += 1
            nodo = nodo.hijos[i]

        for c in nodo.claves:
            if c == k:
                return nodo  # encontrada en la hoja

        return None  # no existe

    def buscar_hoja(self, k):
        """Devuelve la hoja donde DEBERÍA estar k, exista o no."""
        nodo = self.raiz

        while not nodo.hoja:
            i = 0
            while i < len(nodo.claves) and k >= nodo.claves[i]:
                i += 1
            nodo = nodo.hijos[i]

        return nodo

    # "el más a la derecha a la izquierda del eliminado"

    def eliminar(self, k):
        hoja = self.buscar_hoja(k)

        if k not in hoja.claves:
            return  # la clave no existe

        # 1) Si k aparece como clave guía en algún ancestro, se sustituye
        #    por el predecesor (mayor clave de la subrama izquierda de esa guía).
        self._reemplazar_guias(self.raiz, k)

        # 2) Borrado físico en la hoja
        idx = hoja.claves.index(k)
        hoja.claves.pop(idx)

        # 3) Rebalanceo si la hoja (o algún ancestro) quedó por debajo del mínimo
        self._rebalancear(hoja)

        # 4) Si la raíz quedó sin claves y tiene un solo hijo, ese hijo pasa a ser raíz
        if not self.raiz.hoja and len(self.raiz.claves) == 0:
            self.raiz = self.raiz.hijos[0]
            self.raiz.padre = None

    def _reemplazar_guias(self, nodo, k):
        """Recorre el árbol y, donde encuentre la clave guía k en un nodo
        interno, la sustituye por el predecesor (clave más a la derecha
        de la sub-rama inmediatamente a la izquierda de esa guía)."""

        if nodo.hoja:
            return

        for i, clave in enumerate(nodo.claves):
            if clave == k:
                pred = self._predecesor(nodo.hijos[i])
                nodo.claves[i] = pred

        # seguir bajando por el hijo correspondiente para no perder
        # otra posible ocurrencia de la guía en niveles más profundos
        i = 0
        while i < len(nodo.claves) and k >= nodo.claves[i]:
            i += 1
        self._reemplazar_guias(nodo.hijos[i], k)

    def _predecesor(self, nodo):
        """El elemento más a la derecha de la rama (el más grande)."""
        while not nodo.hoja:
            nodo = nodo.hijos[-1]
        return nodo.claves[-1]


    def _rebalancear(self, nodo):

        if nodo is self.raiz:
            return

        padre = nodo.padre

        if padre is None:
            return

        idx = padre.hijos.index(nodo)

        minimo = self.min_claves if not nodo.hoja else self.min_claves

        if len(nodo.claves) >= minimo:
            return

        # Intentar prestar del hermano izquierdo
        if idx > 0 and len(padre.hijos[idx - 1].claves) > minimo:
            self._prestar_izquierda(padre, idx)

        # Intentar prestar del hermano derecho
        elif idx < len(padre.hijos) - 1 and len(padre.hijos[idx + 1].claves) > minimo:
            self._prestar_derecha(padre, idx)

        # Fusionar con un hermano
        else:
            if idx < len(padre.hijos) - 1:
                self._fusionar(padre, idx)
            else:
                self._fusionar(padre, idx - 1)

        # Verificar recursivamente hacia arriba
        if len(padre.claves) < self.min_claves and padre is not self.raiz:
            self._rebalancear(padre)
        elif padre is self.raiz and len(padre.claves) == 0 and not padre.hoja:
            self.raiz = padre.hijos[0]
            self.raiz.padre = None

    def _actualizar_guia_ancestros(self, nodo):

        if not nodo.claves:
            return  # nodo vacío (puede pasar transitoriamente); nada que propagar

        nueva_clave = nodo.claves[0]
        actual = nodo
        padre = actual.padre

        while padre is not None:
            idx = padre.hijos.index(actual)
            if idx > 0:
                padre.claves[idx - 1] = nueva_clave
                break  # ya se actualizó la única guía que corresponde a esta rama
            actual = padre
            padre = actual.padre

    def _prestar_izquierda(self, padre, idx):
        hijo = padre.hijos[idx]
        hermano = padre.hijos[idx - 1]

        if hijo.hoja:
            # mover la última clave del hermano al frente del hijo
            clave_mov = hermano.claves.pop()
            hijo.claves.insert(0, clave_mov)
            # la guía que separa a 'hijo' de su hermano izquierdo puede
            # vivir en el padre o en un ancestro más arriba: se propaga.
            self._actualizar_guia_ancestros(hijo)
        else:
            clave_mov = hermano.claves.pop()
            hijo_mov = hermano.hijos.pop()

            hijo.claves.insert(0, padre.claves[idx - 1])
            hijo.hijos.insert(0, hijo_mov)
            hijo_mov.padre = hijo

            padre.claves[idx - 1] = clave_mov

    def _prestar_derecha(self, padre, idx):
        hijo = padre.hijos[idx]
        hermano = padre.hijos[idx + 1]

        if hijo.hoja:
            clave_mov = hermano.claves.pop(0)
            hijo.claves.append(clave_mov)
            # la primera clave del hermano cambió: su propia guía de
            # ancestro (no necesariamente la del padre inmediato) debe
            # actualizarse.
            self._actualizar_guia_ancestros(hermano)
        else:
            clave_mov = hermano.claves.pop(0)
            hijo_mov = hermano.hijos.pop(0)

            hijo.claves.append(padre.claves[idx])
            hijo.hijos.append(hijo_mov)
            hijo_mov.padre = hijo

            padre.claves[idx] = clave_mov

    def _fusionar(self, padre, idx):
        izq = padre.hijos[idx]
        der = padre.hijos[idx + 1]

        if izq.hoja:
            clave_vieja = der.claves[0] if der.claves else None
            hoja_siguiente = der.siguiente  # lo que queda después de la fusión

            izq.claves.extend(der.claves)
            izq.siguiente = der.siguiente
            if der.siguiente is not None:
                der.siguiente.anterior = izq

            padre.claves.pop(idx)
            padre.hijos.pop(idx + 1)

            if clave_vieja is not None and hoja_siguiente is not None:
                self._reparar_guia_obsoleta(clave_vieja, hoja_siguiente)
        else:
            izq.claves.append(padre.claves[idx])
            izq.claves.extend(der.claves)
            izq.hijos.extend(der.hijos)
            for h in der.hijos:
                h.padre = izq

            padre.claves.pop(idx)
            padre.hijos.pop(idx + 1)

    def _reparar_guia_obsoleta(self, clave_vieja, hoja_siguiente):
        """Busca, en los ancestros de 'hoja_siguiente', una guía cuyo
        valor sea 'clave_vieja' (la que pertenecía a la hoja que acaba
        de desaparecer en una fusión) y la actualiza para que coincida
        con la primera clave real de 'hoja_siguiente'."""

        nueva_clave = hoja_siguiente.claves[0] if hoja_siguiente.claves else None
        if nueva_clave is None:
            return

        actual = hoja_siguiente
        padre = actual.padre

        while padre is not None:
            idx = padre.hijos.index(actual)
            if idx > 0 and padre.claves[idx - 1] == clave_vieja:
                padre.claves[idx - 1] = nueva_clave
                return
            actual = padre
            padre = actual.padre



    def recorrer_hojas(self):
        """Aprovecha la lista enlazada de hojas, característica propia de B+."""
        nodo = self.raiz
        while not nodo.hoja:
            nodo = nodo.hijos[0]

        valores = []
        while nodo is not None:
            valores.extend(nodo.claves)
            nodo = nodo.siguiente
        return valores

    def imprimir(self):
        self._imprimir(self.raiz, "", True)

    def _imprimir(self, nodo, prefijo, ultimo):
        if nodo is None:
            return
        if len(nodo.claves) == 0 and not nodo.hoja:
            for i, hijo in enumerate(nodo.hijos):
                self._imprimir(hijo, prefijo, i == len(nodo.hijos) - 1)
            return

        etiqueta = "[" + "|".join(map(str, nodo.claves)) + "]"
        if nodo.hoja:
            etiqueta += " *"  # marca visual de que es hoja

        print(prefijo + ("└── " if ultimo else "├── ") + etiqueta)

        nuevo_prefijo = prefijo + ("    " if ultimo else "│   ")

        for i, hijo in enumerate(nodo.hijos):
            self._imprimir(hijo, nuevo_prefijo, i == len(nodo.hijos) - 1)


if __name__ == "__main__":
    arbol = ArbolBPlus(4)

    datos = [5, 8, 20, 3, 9, 8]

    for x in datos:
        arbol.insertar(x)

    print("Árbol inicial (B+)")
    arbol.imprimir()

    print("\nRecorrido secuencial de hojas:", arbol.recorrer_hojas())

    arbol.eliminar(9)

    print("\nDespués de eliminar 9")
    arbol.imprimir()

