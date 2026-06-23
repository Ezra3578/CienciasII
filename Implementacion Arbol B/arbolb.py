import math
import sys

sys.stdout.reconfigure(encoding='utf-8')
class NodoB:
    def __init__(self, hoja=False):
        self.hoja = hoja
        self.claves = []
        self.hijos = []


class ArbolB:
    def __init__(self, m):
        self.m = m
        self.max_claves = m - 1
        self.min_claves = math.ceil(m / 2) - 1
        self.raiz = NodoB(True)

    # ---------------- INSERTAR ----------------

    def insertar(self, k):
        resultado = self._insertar_rec(self.raiz, k)

        if resultado is not None:

            promovida, izq, der = resultado

            nueva_raiz = NodoB(False)
            nueva_raiz.claves = [promovida]
            nueva_raiz.hijos = [izq, der]

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

        if len(nodo.claves) > self.max_claves:
            return self.dividir_overflow(nodo)

        return None


    def dividir_overflow(self, nodo):
        total = len(nodo.claves)
        medio = total // 2
        promovida = nodo.claves[medio]

        izq = NodoB(nodo.hoja)
        der = NodoB(nodo.hoja)

        izq.claves = nodo.claves[:medio]
        der.claves = nodo.claves[medio + 1:]

        if not nodo.hoja:
            izq.hijos = nodo.hijos[:medio + 1]
            der.hijos = nodo.hijos[medio + 1:]

        return promovida, izq, der

    # ---------------- BUSCAR ----------------

    def buscar(self, k, nodo=None):

        if nodo is None:
            nodo = self.raiz

        i = 0

        while i < len(nodo.claves) and k > nodo.claves[i]:
            i += 1

        if i < len(nodo.claves) and nodo.claves[i] == k:
            return nodo

        if nodo.hoja:
            return None

        return self.buscar(k, nodo.hijos[i])

    # ---------------- ELIMINAR ----------------

    # def eliminar(self, k):
    #     self._eliminar(self.raiz, k)

    #     if len(self.raiz.claves) == 0 and not self.raiz.hoja:
    #         self.raiz = self.raiz.hijos[0]
        
    #     # Limpiar nodos internos vacíos que quedaron inconsistentes
    #     self._limpiar_nodos_vacios(self.raiz)

    # def _limpiar_nodos_vacios(self, nodo):
    #     """
    #     Elimina nodos internos vacíos (sin claves) que tengan un único hijo.
    #     Esto restaura la propiedad de que todas las hojas están al mismo nivel.
        
    #     Se ejecuta después de eliminar para garantizar consistencia del árbol.
    #     """
    #     if nodo.hoja:
    #         return
        
    #     # Recorrer hijos en orden inverso para evitar problemas de índice
    #     for i in range(len(nodo.hijos) - 1, -1, -1):
    #         hijo = nodo.hijos[i]
            
    #         # Si el hijo es un nodo interno vacío con un único hijo,
    #         # reemplazarlo por su único hijo
    #         if not hijo.hoja and len(hijo.claves) == 0 and len(hijo.hijos) == 1:
    #             print(f"  ⚠ Limpiando nodo interno vacío en posición {i}")
    #             nodo.hijos[i] = hijo.hijos[0]
    #             hijo = nodo.hijos[i]
            
    #         # Limpiar recursivamente todos los hijos
    #         self._limpiar_nodos_vacios(hijo)

    # def _eliminar(self, nodo, k, padre=None, idx_en_padre=None):

    #     idx = 0

    #     while idx < len(nodo.claves) and nodo.claves[idx] < k:
    #         idx += 1

    #     # Caso 1: clave encontrada
    #     if idx < len(nodo.claves) and nodo.claves[idx] == k:

    #         if nodo.hoja:
    #             # Si es hoja, verificar hermanos ANTES de eliminar si quedará por debajo del mínimo
    #             if padre is not None and len(nodo.claves) == self.min_claves:
    #                 print(f"  → Verificando rotación ANTES de eliminar {k}")
    #                 self.llenar(padre, idx_en_padre)
    #                 # Buscar nuevamente la clave después de la posible rotación/fusión
    #                 idx = 0
    #                 while idx < len(nodo.claves) and nodo.claves[idx] < k:
    #                     idx += 1
                
    #             if idx < len(nodo.claves) and nodo.claves[idx] == k:
    #                 print(f"  → Eliminando {k} de la hoja")
    #                 self.eliminar_en_hoja(nodo, idx)

    #         else:
    #             self.eliminar_interno(nodo, k, idx)

    #     else:

    #         if nodo.hoja:
    #             return

    #         bandera = (idx == len(nodo.claves))

    #         if len(nodo.hijos[idx].claves) < self.min_claves:
    #             self.llenar(nodo, idx)

    #         if bandera and idx > len(nodo.claves):
    #             self._eliminar(nodo.hijos[idx - 1], k, nodo, idx - 1)
    #         else:
    #             self._eliminar(nodo.hijos[idx], k, nodo, idx)

    # def eliminar_en_hoja(self, nodo, idx):
    #     """
    #     Elimina una clave en una hoja.
        
    #     Parámetros:
    #         nodo: Nodo hoja donde se elimina la clave
    #         idx: Índice de la clave a eliminar
    #     """
    #     nodo.claves.pop(idx)

    # def _eliminar_con_validacion_hoja(self, padre, nodo, k, idx_en_padre):
    #     """
    #     Elimina una clave de una hoja con validación previa del hermano izquierdo.
        
    #     Estrategia:
    #     1. Si la hoja tiene el mínimo de claves, verifica primero el hermano izquierdo
    #     2. Si el hermano izquierdo tiene claves extra, realiza rotación ANTES de eliminar
    #     3. Si no puede rotar, intenta fusionar
    #     4. Finalmente elimina la clave
        
    #     Parámetros:
    #         padre: Nodo padre
    #         nodo: Nodo hoja donde se elimina
    #         k: Clave a eliminar
    #         idx_en_padre: Índice del nodo en su padre
    #     """
    #     # Encontrar el índice de la clave a eliminar
    #     idx_clave = 0
    #     while idx_clave < len(nodo.claves) and nodo.claves[idx_clave] < k:
    #         idx_clave += 1

    #     # Verificar si la clave existe
    #     if idx_clave >= len(nodo.claves) or nodo.claves[idx_clave] != k:
    #         return False

    #     # Si la hoja tiene exactamente el mínimo de claves
    #     if len(nodo.claves) == self.min_claves + 1:
    #         print(f"  Hoja tiene mínimo de claves. Verificando hermano izquierdo...")

    #         # Verificar hermano izquierdo
    #         if idx_en_padre > 0:
    #             hermano_izq = padre.hijos[idx_en_padre - 1]
    #             if len(hermano_izq.claves) > self.min_claves:
    #                 print(f"  ✓ Hermano izquierdo tiene claves extra. Realizando rotación...")
    #                 self.prestar_izquierda(padre, idx_en_padre)
    #                 # Después de la rotación, la posición de la clave pudo cambiar
    #                 idx_clave = 0
    #                 while idx_clave < len(nodo.claves) and nodo.claves[idx_clave] < k:
    #                     idx_clave += 1

    #         # Si no se pudo rotar con izquierdo, verificar hermano derecho
    #         elif idx_en_padre < len(padre.hijos) - 1:
    #             hermano_der = padre.hijos[idx_en_padre + 1]
    #             if len(hermano_der.claves) > self.min_claves:
    #                 print(f"  ✓ Hermano derecho tiene claves extra. Realizando rotación...")
    #                 self.prestar_derecha(padre, idx_en_padre)
    #                 idx_clave = 0
    #                 while idx_clave < len(nodo.claves) and nodo.claves[idx_clave] < k:
    #                     idx_clave += 1

    #     # Eliminar la clave
    #     nodo.claves.pop(idx_clave)
    #     print(f"  ✓ Clave {k} eliminada")
    #     return True

    # def eliminar_interno(self, nodo, k, idx):

    #     hijo_izq = nodo.hijos[idx]
    #     hijo_der = nodo.hijos[idx + 1]

    #     if len(hijo_izq.claves) > self.min_claves:

    #         pred = self.obtener_predecesor(hijo_izq)

    #         nodo.claves[idx] = pred

    #         self._eliminar(hijo_izq, pred, nodo, idx)

    #     elif len(hijo_der.claves) > self.min_claves:

    #         suc = self.obtener_sucesor(hijo_der)

    #         nodo.claves[idx] = suc

    #         self._eliminar(hijo_der, suc, nodo, idx + 1)

    #     else:

    #         self.fusionar(nodo, idx)

    #         self._eliminar(hijo_izq, k, nodo, idx)

    # def obtener_predecesor(self, nodo):

    #     while not nodo.hoja:
    #         nodo = nodo.hijos[-1]

    #     return nodo.claves[-1]

    # def obtener_sucesor(self, nodo):

    #     while not nodo.hoja:
    #         nodo = nodo.hijos[0]

    #     return nodo.claves[0]

    # def llenar(self, nodo, idx):
    #     """
    #     Llena un nodo que tiene menos claves que el mínimo requerido.
        
    #     Estrategia de reparación (en orden de prioridad):
    #     1. Verifica el hermano IZQUIERDO (más a la derecha): si tiene claves extra,
    #        realiza una ROTACIÓN derecha (el hermano izquierdo cede una clave al padre,
    #        el padre cede una clave al nodo actual)
    #     2. Si el hermano izquierdo no puede prestar, verifica el hermano DERECHO:
    #        si tiene claves extra, realiza una ROTACIÓN izquierda
    #     3. Si ningún hermano tiene claves extra, FUSIONA el nodo con su hermano
        
    #     Parámetros:
    #         nodo: Nodo padre
    #         idx: Índice del hijo deficiente
    #     """
    #     # PASO 1: Intentar ROTACIÓN CON HERMANO IZQUIERDO
    #     if idx != 0 and len(nodo.hijos[idx - 1].claves) > self.min_claves:
    #         print(f"  → Rotación con hermano izquierdo en posición {idx - 1}")
    #         self.prestar_izquierda(nodo, idx)

    #     # PASO 2: Intentar ROTACIÓN CON HERMANO DERECHO
    #     elif idx != len(nodo.hijos) - 1 and \
    #             len(nodo.hijos[idx + 1].claves) > self.min_claves:
    #         print(f"  → Rotación con hermano derecho en posición {idx + 1}")
    #         self.prestar_derecha(nodo, idx)

    #     # PASO 3: FUSIONAR si no hay rotación posible
    #     else:
    #         if idx != len(nodo.hijos) - 1:
    #             print(f"  → Fusionando nodo {idx} con hermano derecho")
    #             self.fusionar(nodo, idx)
    #         else:
    #             print(f"  → Fusionando nodo {idx} con hermano izquierdo")
    #             self.fusionar(nodo, idx - 1)

    # def prestar_izquierda(self, nodo, idx):
    #     """
    #     ROTACIÓN DERECHA: El hijo izquierdo (más a la derecha) presta una clave.
        
    #     Flujo:
    #     1. La clave más grande del hermano izquierdo sube al padre
    #     2. La clave del padre baja al nodo deficiente
    #     3. Si no es hoja, el hijo más derecho del hermano izquierdo se traslada
    #        al nodo deficiente
        
    #     Parámetros:
    #         nodo: Nodo padre
    #         idx: Índice del hijo que recibe la clave
    #     """
    #     hijo = nodo.hijos[idx]
    #     hermano = nodo.hijos[idx - 1]

    #     # La clave del padre baja al nodo deficiente por la izquierda
    #     hijo.claves.insert(0, nodo.claves[idx - 1])

    #     # Si no es hoja, traslada el hijo más derecho del hermano
    #     if not hijo.hoja:
    #         hijo.hijos.insert(0, hermano.hijos.pop())

    #     # La clave más grande del hermano sube al padre
    #     nodo.claves[idx - 1] = hermano.claves.pop()

    # def prestar_derecha(self, nodo, idx):
    #     """
    #     ROTACIÓN IZQUIERDA: El hijo derecho presta una clave.
        
    #     Flujo:
    #     1. La clave más pequeña del hermano derecho sube al padre
    #     2. La clave del padre baja al nodo deficiente
    #     3. Si no es hoja, el hijo más izquierdo del hermano derecho se traslada
    #        al nodo deficiente
        
    #     Parámetros:
    #         nodo: Nodo padre
    #         idx: Índice del hijo que recibe la clave
    #     """
    #     hijo = nodo.hijos[idx]
    #     hermano = nodo.hijos[idx + 1]

    #     # La clave del padre baja al nodo deficiente por la derecha
    #     hijo.claves.append(nodo.claves[idx])

    #     # Si no es hoja, traslada el hijo más izquierdo del hermano
    #     if not hijo.hoja:
    #         hijo.hijos.append(hermano.hijos.pop(0))

    #     # La clave más pequeña del hermano sube al padre
    #     nodo.claves[idx] = hermano.claves.pop(0)

    # def fusionar(self, nodo, idx):

    #     hijo = nodo.hijos[idx]
    #     hermano = nodo.hijos[idx + 1]

    #     hijo.claves.append(nodo.claves[idx])

    #     hijo.claves.extend(hermano.claves)

    #     if not hijo.hoja:
    #         hijo.hijos.extend(hermano.hijos)

    #     nodo.claves.pop(idx)
    #     nodo.hijos.pop(idx + 1)

    # ---------------- MOSTRAR ----------------

    def imprimir(self):
        self._imprimir(self.raiz, "", True)

    def _imprimir(self, nodo, prefijo, ultimo):
      if nodo is None:
          return
      if len(nodo.claves) == 0:
        for i, hijo in enumerate(nodo.hijos):
            self._imprimir(hijo, prefijo, i == len(nodo.hijos) - 1)
        return

      print(prefijo + ("└── " if ultimo else "├── ") +
            "[" + "|".join(map(str, nodo.claves)) + "]")

      nuevo_prefijo = prefijo + ("    " if ultimo else "│   ")

      for i, hijo in enumerate(nodo.hijos):
          self._imprimir(hijo, nuevo_prefijo, i == len(nodo.hijos) - 1)


# ================= PRUEBA =================

arbol = ArbolB(4)

datos = [5, 8, 20, 3, 9, 8, 4, 10, 1, 2, 2]

print("=== INSERTANDO DATOS ===")
for x in datos:
    arbol.insertar(x)

print("\n=== ÁRBOL INICIAL ===")
arbol.imprimir()

# print("\n=== ELIMINANDO 20 ===")
# arbol.eliminar(20)
# arbol.imprimir()

# print("\n=== ELIMINANDO 3 ===")
# arbol.eliminar(3)
# arbol.imprimir()

# print("\n=== ELIMINANDO 9 ===")
# arbol.eliminar(9)
# arbol.imprimir()
