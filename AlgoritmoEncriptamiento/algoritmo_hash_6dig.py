# =============================================================================
#  TABLA DE CARACTERES (100 símbolos)
# =============================================================================
ID_A_CHAR = {
     0: '0',  1: '1',  2: '2',  3: '3',  4: '4',
     5: '5',  6: '6',  7: '7',  8: '8',  9: '9',
    10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E',
    15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J',
    20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'Ñ',
    25: 'O', 26: 'P', 27: 'Q', 28: 'R', 29: 'S',
    30: 'T', 31: 'U', 32: 'V', 33: 'W', 34: 'X',
    35: 'Y', 36: 'Z', 37: 'Á', 38: 'É', 39: 'Í',
    40: 'Ó', 41: 'Ú', 42: 'a', 43: 'b', 44: 'c',
    45: 'd', 46: 'e', 47: 'f', 48: 'g', 49: 'h',
    50: 'i', 51: 'j', 52: 'k', 53: 'l', 54: 'm',
    55: 'n', 56: 'ñ', 57: 'o', 58: 'p', 59: 'q',
    60: 'r', 61: 's', 62: 't', 63: 'u', 64: 'v',
    65: 'w', 66: 'x', 67: 'y', 68: 'z', 69: 'á',
    70: 'é', 71: 'í', 72: 'ó', 73: 'ú', 74: ',',
    75: '.', 76: ';', 77: ':', 78: '*', 79: '/',
    80: '+', 81: '-', 82: '_', 83: '=', 84: '¿',
    85: '?', 86: '¡', 87: '!', 88: '"', 89: "'",
    90: '(', 91: ')', 92: '{', 93: '}', 94: '[',
    95: ']', 96: '#', 97: '$', 98: '%', 99: ' ',
}

CHAR_A_ID = {v: k for k, v in ID_A_CHAR.items()}


def id_a_bits(id_num: int) -> str:
    """Convierte un identificador (0-99) a cadena de 8 bits."""
    return format(id_num, '08b')


# =============================================================================
#  CIFRADO IRREVERSIBLE (pasos 0‑6 + reducción módulo 10⁶ en base 36)
# =============================================================================
def cifrar(entrada: str, verbose: bool = False) -> str:
    """
    Transforma un texto en un número de 0 a 999999 de forma determinista
    e irreversible (no se puede recuperar el original).

    El alfabeto aceptado cubre números, letras mayúsculas/minúsculas (incluyendo
    Ñ, ñ y vocales acentuadas), espacio y ciertos signos de puntuación.
    Cualquier carácter fuera de la tabla lanza ValueError.

    Si verbose=True imprime el resultado después de cada paso.
    """
    # ── 0. Texto → decimal con dígito de control hexadecimal ─────────────────
    binario = ''
    for ch in entrada:
        if ch not in CHAR_A_ID:
            raise ValueError(f"Carácter '{ch}' no está en la tabla de cifrado.")
        binario += id_a_bits(CHAR_A_ID[ch])

    # Se reduce el número binario módulo 1 000 000 para forzar colisiones
    decimal     = int(binario, 2) % 1000000
    hexa        = format(decimal % 16, 'X')          # dígito de control
    posicion    = len(entrada)
    decimal_str = str(decimal)
    # Insertar el dígito hexa en la posición dada por la longitud original
    resultado   = decimal_str[:posicion] + hexa + decimal_str[posicion:]

    if verbose:
        print(f"[Paso 0] Texto → decimal + hexa insertado: {resultado}")

    # ── 1. Sustituir todos los '0' por 'A' ───────────────────────────────────
    count_0_real     = resultado.count('0')
    count_0_insertar = count_0_real + 1
    resultado        = resultado.replace('0', 'A')

    if verbose:
        print(f"[Paso 1] '0' → 'A' (count_0_real={count_0_real}): {resultado}")

    # ── 2. Agregar 'C' a la derecha de cada '1' ─────────────────────────────
    resultado_list = list(resultado)
    count_c = 0
    i = 0
    while i < len(resultado_list):
        if resultado_list[i] == '1':
            resultado_list.insert(i + 1, 'C')
            count_c += 1
            i += 2
        else:
            i += 1

    if verbose:
        print(f"[Paso 2] 'C' tras cada '1' (count_c={count_c}): {''.join(resultado_list)}")

    # ── 3. Bucle de ofuscación C1 ───────────────────────────────────────────
    # Se eliminan todas las apariciones de "C1", se rota la cadena
    # y se inserta un '1' cerca del final. Se repite (núm. de "C1" + 1) veces.
    cadena_temp     = ''.join(resultado_list)
    count_c1_previo = cadena_temp.count('C1')
    repeticiones    = count_c1_previo + 1
    info_vueltas_c1 = []   # (innecesario ahora, pero mantenemos compatibilidad)
    for vuelta in range(repeticiones):
        cadena_temp   = ''.join(resultado_list)
        posiciones_c1 = []
        idx = 0
        while True:
            pos = cadena_temp.find('C1', idx)
            if pos == -1:
                break
            posiciones_c1.append(pos)
            idx = pos + 2
        # Posiciones ajustadas (sin usar, solo por claridad del algoritmo original)
        pos_ajustadas = [pos - i * 2 for i, pos in enumerate(posiciones_c1)]
        cadena_temp   = cadena_temp.replace('C1', '')
        n     = len(cadena_temp)
        shift = count_c % n if (n and count_c % n != 0) else 0
        cadena_temp    = (cadena_temp[-shift:] + cadena_temp[:-shift]
                          if shift else cadena_temp)
        resultado_list = list(cadena_temp)
        insert_pos     = max(0, len(resultado_list) - 1 - vuelta)
        resultado_list.insert(insert_pos, '1')
        info_vueltas_c1.append({
            'pos_ajustadas': pos_ajustadas,
            'shift': shift,
            'insert_pos': insert_pos,
        })

    if verbose:
        print(f"[Paso 3] Bucle C1 (repeticiones={repeticiones}): {''.join(resultado_list)}")

    # ── 4. Insertar 'A' cada 2 posiciones (exactamente count_0_insertar veces)
    i = 2
    insertadas = 0
    while insertadas < count_0_insertar:
        # Si i sobrepasa la longitud, insertamos al final
        pos = min(i, len(resultado_list))
        resultado_list.insert(pos, 'A')
        insertadas += 1
        i += 3   # avanzamos 3 porque insertamos un carácter

    if verbose:
        print(f"[Paso 4] Insertar 'A' cada 2 posiciones: {''.join(resultado_list)}")

    # ── 5. Insertar count_0_insertar después de cada 'A' ────────────────────
    i = 3
    inserciones = 0
    while inserciones < count_0_insertar:
        pos = min(i, len(resultado_list))
        resultado_list.insert(pos, str(count_0_insertar))
        inserciones += 1
        i += 4   # avanzamos 4 por la 'A', el número insertado y el carácter siguiente

    if verbose:
        print(f"[Paso 5] Insertar {count_0_insertar} tras cada 'A': {''.join(resultado_list)}")

    resultado_final = ''.join(resultado_list)

    # ── 6. Corrimiento a la derecha por count_c ──────────────────────────────
    n     = len(resultado_final)
    shift = count_c % n if n else 0
    resultado_final = (resultado_final[-shift:] + resultado_final[:-shift]
                       if shift else resultado_final)

    if verbose:
        print(f"[Paso 6] Corrimiento derecha {shift} posiciones: {resultado_final}")

    # ── 7. Convertir a decimal (base 36) y aplicar módulo 1 000 000 ─────────
    decimal_base36 = int(resultado_final, 36)
    modulo7 = decimal_base36 % 1000000
    cifrado_mod = str(modulo7)

    if verbose:
        print(f"[Paso 7] Base36 = {decimal_base36}, módulo 10⁶ = {modulo7}")
        print(f"         Cifrado final (dígito): {cifrado_mod}")

    return cifrado_mod


# =============================================================================
#  DEMOSTRACIÓN (sólo muestra el proceso de cifrado, no intenta descifrar)
# =============================================================================
if __name__ == '__main__':

    pruebas = [
        "a",
        "Juan",
        "Erick",
        "Carina",
        "Ana",
        "Simar",
        "Inter Ciencias2",
        "UDistri"
    ]

    for texto in pruebas:
        try:
            print("\n" + "=" * 70)
            print(f"Texto original: {texto!r}")
            cifrado = cifrar(texto, verbose=True)
            print("=" * 70)
            print(f"→ Cifrado irreversible: {cifrado}")
            print("(Este número identifica el texto, pero no permite recuperarlo)\n")
        except ValueError as e:
            print(f"Error con {texto!r}: {e}")
