def volverNum(codigo):
    return ord(codigo) - 64

def volverLetra(codigo):
    return chr(codigo + 64)

ROTOR_1 = {
    1: 7, 2: 15, 3: 10, 4: 26, 5: 14, 6: 23, 7: 5, 8: 21, 9: 3, 10: 16,
    11: 6, 12: 19, 13: 11, 14: 13, 15: 22, 16: 24, 17: 1, 18: 25, 19: 9,
    20: 2, 21: 20, 22: 18, 23: 17, 24: 12, 25: 4, 26: 8,
}

ROTOR_2 = {
    1: 12, 2: 20, 3: 15, 4: 5, 5: 19, 6: 2, 7: 10, 8: 26, 9: 8, 10: 21,
    11: 11, 12: 24, 13: 16, 14: 18, 15: 1, 16: 3, 17: 6, 18: 4, 19: 14, 20: 7,
    21: 25, 22: 23, 23: 22, 24: 17, 25: 9, 26: 13,
}

ROTOR_3 = {
    1: 16, 2: 24, 3: 19, 4: 9, 5: 23, 6: 6, 7: 14, 8: 4, 9: 12, 10: 25,
    11: 15, 12: 2, 13: 20, 14: 22, 15: 5, 16: 7, 17: 10, 18: 8, 19: 18, 20: 11,
    21: 3, 22: 1, 23: 26, 24: 21, 25: 13, 26: 17,
}

ROTOR_4 = {
    1: 21, 2: 3, 3: 24, 4: 14, 5: 2, 6: 11, 7: 19, 8: 9, 9: 17, 10: 4,
    11: 20, 12: 7, 13: 25, 14: 1, 15: 10, 16: 12, 17: 15, 18: 13, 19: 23, 20: 16,
    21: 8, 22: 6, 23: 5, 24: 26, 25: 18, 26: 22,
}

ROTOR_5 = {
    1: 26, 2: 8, 3: 3, 4: 19, 5: 7, 6: 16, 7: 24, 8: 14, 9: 22, 10: 9,
    11: 25, 12: 12, 13: 4, 14: 6, 15: 15, 16: 17, 17: 20, 18: 18, 19: 2, 20: 21,
    21: 13, 22: 11, 23: 10, 24: 5, 25: 23, 26: 1,
}

WIRINGS = {
    1: ROTOR_1,
    2: ROTOR_2,
    3: ROTOR_3,
    4: ROTOR_4,
    5: ROTOR_5,
}


WIRINGS_INVERSAS = {
    tipo: {salida: entrada for entrada, salida in wiring.items()}
    for tipo, wiring in WIRINGS.items()
}


# ---------------------------------------------------------------------------
# REFLECTORES
# ---------------------------------------------------------------------------
def _construir_reflector_desde_pares(pares):
    """Construye un diccionario reflector (involución) a partir de una lista
    de pares de números. Cada par (a, b) genera a->b y b->a."""
    mapa = {}
    for a, b in pares:
        mapa[a] = b
        mapa[b] = a
    return mapa


# Reflector B: equivale a la constante original (27 - codigo).
# Empareja 1<->26, 2<->25, 3<->24, ... 13<->14.
REFLECTOR_B = {codigo: 27 - codigo for codigo in range(1, 27)}

# Reflector C: ejemplo adicional. También es una involución sin puntos fijos.
REFLECTOR_C = _construir_reflector_desde_pares([
    (1, 6), (2, 14), (3, 11), (4, 19), (5, 22), (7, 24), (8, 17),
    (9, 20), (10, 26), (12, 16), (13, 25), (15, 23), (18, 21),
])

REFLECTORES = {
    'B': REFLECTOR_B,
    'C': REFLECTOR_C,
}


class Clavijero:
    def __init__(self, pares=None):
        self.mapa = {}
        if pares:
            for letra_a, letra_b in pares:
                a = volverNum(letra_a.upper())
                b = volverNum(letra_b.upper())
                self.mapa[a] = b
                self.mapa[b] = a

    def pasar(self, codigo):
        # Si la letra tiene cable, la intercambia; si no, la deja igual.
        return self.mapa.get(codigo, codigo)


# ---------------------------------------------------------------------------
# REFLECTOR
# ---------------------------------------------------------------------------
class Reflector:
    def __init__(self, tipoReflector='B'):
        if tipoReflector not in REFLECTORES:
            raise ValueError(
                f"Reflector '{tipoReflector}' no existe. "
                f"Opciones: {list(REFLECTORES.keys())}"
            )
        self.tipoReflector = tipoReflector
        self.mapa = REFLECTORES[tipoReflector]

    def pasar(self, codigo):
        return self.mapa[codigo]


# ---------------------------------------------------------------------------
# ROTOR
# ---------------------------------------------------------------------------
class Rotor:
    def __init__(self, tipoRotor, posicionInicial):
        self.tipoRotor = tipoRotor
        self.posicionInicial = posicionInicial
        self.posicion = posicionInicial
        self.pasos = 0
        self.wiring = WIRINGS[tipoRotor]
        self.wiring_inverso = WIRINGS_INVERSAS[tipoRotor]

    def girar(self):
        self.posicion = (self.posicion % 26) + 1
        self.pasos += 1

    def reset(self):
        """Vuelve el rotor a su posición inicial. Necesario para poder
        descifrar."""
        self.posicion = self.posicionInicial
        self.pasos = 0

    @staticmethod
    def _envolverRotor(codigo):
        while codigo > 26:
            codigo -= 26
        while codigo < 1:
            codigo += 26
        return codigo

    def pasar_ida(self, codigo):
        entrada_desplazada = self._envolverRotor(codigo + self.posicion)
        return self.wiring[entrada_desplazada]

    def pasar_vuelta(self, codigo):
        salida_wiring = self.wiring_inverso[codigo]
        return self._envolverRotor(salida_wiring - self.posicion)


class EnigmaMachine:
    def __init__(self, rotor1_type, rotor2_type, rotor3_type,
                 posicion1, posicion2, posicion3,
                 pares_clavijero=None, charPorChar=True,
                 reflector='B'):
        self.r1 = Rotor(rotor1_type, posicion1)
        self.r2 = Rotor(rotor2_type, posicion2)
        self.r3 = Rotor(rotor3_type, posicion3)
        self.clavijero = Clavijero(pares_clavijero)
        self.charPorChar = charPorChar
        # Acepta tanto un tipo ('B', 'C') como un objeto Reflector ya construido.
        if isinstance(reflector, Reflector):
            self.reflector = reflector
        else:
            self.reflector = Reflector(reflector)

    def reset(self):
        """Reinicia los 3 rotores a su posición inicial, para reutilizar
        la misma máquina para descifrar."""
        self.r1.reset()
        self.r2.reset()
        self.r3.reset()

    def _avanzar_rotores(self):
        if self.r1.pasos > 0 and self.r1.pasos % 26 == 0:
            if self.r2.pasos > 0 and self.r2.pasos % 26 == 0:
                self.r3.girar()
            self.r2.girar()
        self.r1.girar()

    def _procesar_char(self, char):
        if not char.isalpha():
            return char

        self._avanzar_rotores()

        codigo = volverNum(char.upper())

        # --- CAMINO DE IDA: clavijero -> r1 -> r2 -> r3 ---
        codigo = self.clavijero.pasar(codigo)
        codigo = self.r1.pasar_ida(codigo)
        codigo = self.r2.pasar_ida(codigo)
        codigo = self.r3.pasar_ida(codigo)

        # --- REFLECTOR ---
        codigo = self.reflector.pasar(codigo)

        # --- CAMINO DE VUELTA: r3 -> r2 -> r1 -> clavijero ---
        codigo = self.r3.pasar_vuelta(codigo)
        codigo = self.r2.pasar_vuelta(codigo)
        codigo = self.r1.pasar_vuelta(codigo)
        codigo = self.clavijero.pasar(codigo)

        resultado = volverLetra(codigo)

        if self.charPorChar:
            print(f"Paso:{self.r1.pasos} | R1:{self.r1.posicion} "
                  f"R2:{self.r2.posicion} R3:{self.r3.posicion} | "
                  f"{char.upper()} -> {resultado}")

        return resultado

    def cifrar_char(self, char):
        return self._procesar_char(char)

    def descifrar_char(self, char):
        return self._procesar_char(char)

    def cifrar(self, texto):
        return ''.join(self.cifrar_char(c) for c in texto)

    def descifrar(self, texto):
        return ''.join(self.descifrar_char(c) for c in texto)
print("\n=== CIFRADO POR CARACTERES ===")
#Se cifra y decifra en mayusculas
maquina = EnigmaMachine(1, 2, 3, 5, 10, 3)

print(maquina.cifrar_char('H'))
print(maquina.cifrar_char('O'))
print(maquina.cifrar_char('L'))
print(maquina.cifrar_char('A'))
print(maquina.cifrar_char('A'))

print("\n=== CIFRADO Y DESCIFRADO DE UN TEXTO COMPLETO ===")
pares_clavijero = [('H', 'Z'), ('O', 'X')]
reflector = 'B'#PUEDE SER B O C

maquina_cifrado = EnigmaMachine(1, 2, 3, 5, 10, 3, pares_clavijero, reflector)
mensaje_original = "Buenos dias, y hasta luego."
mensaje_original = mensaje_original.upper()
mensaje_cifrado = maquina_cifrado.cifrar(mensaje_original)

print(f"\nTexto original: {mensaje_original}")
print(f"Texto cifrado:  {mensaje_cifrado}")

maquina_descifrado = EnigmaMachine(1, 2, 3, 5, 10, 3, pares_clavijero,reflector)
mensaje_descifrado = maquina_descifrado.descifrar(mensaje_cifrado)

print(f"\nTexto cifrado:    {mensaje_cifrado}")
print(f"Texto descifrado: {mensaje_descifrado}")

assert mensaje_descifrado == mensaje_original, "¡El round-trip falló!"
print("\nEl texto descifrado coincide con el original.")


print("\n=== PRUEBA CON REFLECTOR PERSONALIZADO (C) ===")
maquina_c = EnigmaMachine(1, 2, 3, 5, 10, 3,
                          pares_clavijero=pares_clavijero,
                          charPorChar=False, reflector='C')
cifrado_c = maquina_c.cifrar(mensaje_original)

maquina_c_desc = EnigmaMachine(1, 2, 3, 5, 10, 3,
                               pares_clavijero=pares_clavijero,
                               charPorChar=False, reflector='C')
descifrado_c = maquina_c_desc.descifrar(cifrado_c)

print(f"Texto original:   {mensaje_original}")
print(f"Cifrado (refl C): {cifrado_c}")
print(f"Descifrado:       {descifrado_c}")
assert descifrado_c == mensaje_original.upper(), "¡El round-trip con reflector C falló!"
print("El round-trip con el reflector C también funciona.")