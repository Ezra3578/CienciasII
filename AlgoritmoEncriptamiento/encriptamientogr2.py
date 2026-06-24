# =============================================================================
#  Algoritmo de cifrado (paso 7 DESTRUCTIVO cada 2) + intento de descifrado
#  con reconstruccion guiada por restricciones (muestra hasta 20 intentos).
# =============================================================================
import itertools
import random #este es para hacer los intentos de descifrado, no se usa en el cifrado

def eliminar_seguidos(cadena):
    """
    Elimina todo caracter que forme parte de una racha de 2+ iguales consecutivos.
    Devuelve (cadena_filtrada, info_eliminados) donde info_eliminados guarda
    (caracter, posicion_original) para poder revertir.
    """
    n      = len(cadena)
    quitar = [False] * n
    for i in range(n):
        if (i > 0 and cadena[i] == cadena[i - 1]) or \
           (i < n - 1 and cadena[i] == cadena[i + 1]):
            quitar[i] = True
    eliminados = [(cadena[i], i) for i in range(n) if quitar[i]]
    filtrada   = ''.join(cadena[i] for i in range(n) if not quitar[i])
    return filtrada, eliminados
 
 
def reinsertar_seguidos(cadena, info_eliminados):
    """Revierte eliminar_seguidos: reinserta cada caracter en su posicion original."""
    resultado = list(cadena)
    for ch, pos in sorted(info_eliminados, key=lambda x: x[1]):
        resultado.insert(pos, ch)
    return ''.join(resultado)
 
 
# -----------------------------------------------------------------------------
#  Cifrado
# -----------------------------------------------------------------------------
def cifrar(entrada):
    """
    Pasos:
      0. Texto -> decimal via binario UTF-8, insertar hexa en posicion len
      1. Eliminar 'A1'
      2. Agregar 'C' a la derecha de cada '1'
      3. Bucle C1
      4. Insertar 'A' cada 2 posiciones (count_a1_insertar veces)
      5. Insertar count_a1_insertar despues de cada 'A'
      6. Corrimiento derecha count_c posiciones
      7. [DESTRUCTIVO] Eliminar el caracter en indices impares (1,3,5,...)
      8. Eliminar terminos seguidos
    Devuelve la tupla de cifrado + metadatos (sin lo destruido en el paso 7).
    """
    # ── 0. Texto → decimal ───────────────────────────────────────────────────
    binario = ''
    for ch in entrada:
        binario += bin(ord(ch))[2:].zfill(8)
    decimal = int(binario, 2)
    hexa    = format(decimal % len(entrada), 'X')
    posicion    = len(entrada)
    decimal_str = str(decimal)
    resultado   = decimal_str[:posicion] + hexa + decimal_str[posicion:]
 
    # ── 1. Contar y eliminar 'A1' ────────────────────────────────────────────
    count_a1_real     = resultado.count('A1')
    count_a1_insertar = count_a1_real + 1
    resultado         = resultado.replace('A1', '')
 
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
 
    # ── 3. Bucle C1 ──────────────────────────────────────────────────────────
    cadena_temp     = ''.join(resultado_list)
    count_c1_previo = cadena_temp.count('C1')
    repeticiones    = count_c1_previo + 1
    info_vueltas_c1 = []
    for vuelta in range(repeticiones):
        cadena_temp = ''.join(resultado_list)
        posiciones_c1 = []
        idx = 0
        while True:
            pos = cadena_temp.find('C1', idx)
            if pos == -1:
                break
            posiciones_c1.append(pos)
            idx = pos + 2
        pos_ajustadas = [pos - i * 2 for i, pos in enumerate(posiciones_c1)]
        cadena_temp = cadena_temp.replace('C1', '')
        n     = len(cadena_temp)
        shift = count_c % n if (n and count_c % n != 0) else 0
        cadena_temp = cadena_temp[-shift:] + cadena_temp[:-shift] if shift else cadena_temp
        resultado_list = list(cadena_temp)
        insert_pos     = max(0, len(resultado_list) - 1 - vuelta)
        resultado_list.insert(insert_pos, '1')
        info_vueltas_c1.append({'pos_ajustadas': pos_ajustadas,
                                'shift': shift, 'insert_pos': insert_pos})
 
    # ── 4. Insertar 'A' cada 2 posiciones ────────────────────────────────────
    i = 2
    insertadas = 0
    while insertadas < count_a1_insertar and i <= len(resultado_list):
        resultado_list.insert(i, 'A')
        insertadas += 1
        i += 3
 
    # ── 5. Insertar count_a1_insertar despues de cada 'A' ───────────────────
    i = 3
    inserciones = 0
    while inserciones < count_a1_insertar and i <= len(resultado_list):
        resultado_list.insert(i, str(count_a1_insertar))
        inserciones += 1
        i += 4
    resultado_final = ''.join(resultado_list)
 
    # ── 6. Corrimiento a la derecha por count_c ──────────────────────────────
    n     = len(resultado_final)
    shift = count_c % n if n else 0
    resultado_final = resultado_final[-shift:] + resultado_final[:-shift] if shift else resultado_final
 
    # Longitud de la cadena justo ANTES del paso destructivo (necesaria para
    # ubicar los huecos durante el intento de descifrado).
    longitud_post6 = len(resultado_final)
 
    # ── 7. [DESTRUCTIVO] Eliminar caracter en indices impares (1,3,5,...) ────
    #     NO se guarda nada: ni el caracter ni la posicion.
    lista_r7  = list(resultado_final)
    conservar = [c for idx, c in enumerate(lista_r7) if idx % 2 == 0]
    resultado_final = ''.join(conservar)
 
    # ── 8. Eliminar terminos seguidos ────────────────────────────────────────
    resultado_final, info_eliminados = eliminar_seguidos(resultado_final)
 
    return (resultado_final,
            len(entrada),
            count_a1_real,
            count_a1_insertar,
            count_c,
            info_vueltas_c1,
            count_c1_previo,
            info_eliminados,
            longitud_post6)
 
 
# -----------------------------------------------------------------------------
#  Descifrado parcial: revierte pasos 6..0 desde la cadena tal como quedo
#  tras el paso 6 (es decir, ya reconstruidos los huecos del paso 7).
#  Devuelve el texto si pasa la verificacion hexa, o None si es inconsistente.
# -----------------------------------------------------------------------------
def descifrar_resto(cadena_post6, longitud, count_a1_real, count_a1_insertar,
                    count_c, info_vueltas_c1, count_c1_previo):
    # ── Revertir 6: corrimiento izquierda ────────────────────────────────────
    n     = len(cadena_post6)
    shift = count_c % n if n else 0
    resultado = cadena_post6[shift:] + cadena_post6[:shift] if shift else cadena_post6
    resultado = list(resultado)
 
    # ── Revertir 5: borrar count_a1_insertar numerico ───────────────────────
    i = 3; eliminados = 0
    while eliminados < count_a1_insertar and i < len(resultado):
        if resultado[i] == str(count_a1_insertar):
            resultado.pop(i); eliminados += 1; i += 3
        else:
            i += 1
 
    # ── Revertir 4: borrar las 'A' insertadas ───────────────────────────────
    i = 2; eliminadas = 0
    while eliminadas < count_a1_insertar and i < len(resultado):
        if resultado[i] == 'A':
            resultado.pop(i); eliminadas += 1; i += 2
        else:
            i += 1
 
    # ── Revertir 3: bucle C1 en orden inverso ───────────────────────────────
    cadena = ''.join(resultado)
    repeticiones = count_c1_previo + 1
    for vuelta in range(repeticiones - 1, -1, -1):
        info = info_vueltas_c1[vuelta]
        shift = info['shift']; ins = info['insert_pos']; pos_adj = info['pos_ajustadas']
        lista = list(cadena)
        if ins < len(lista) and lista[ins] == '1':
            lista.pop(ins)
        cadena = ''.join(lista)
        n = len(cadena)
        cadena = cadena[shift:] + cadena[:shift] if shift else cadena
        offset = 0
        for pa in sorted(pos_adj):
            real_pos = pa + offset
            cadena = cadena[:real_pos] + 'C1' + cadena[real_pos:]
            offset += 2
 
    # ── Revertir 2: borrar las 'C' que siguen a un '1' ──────────────────────
    resultado = list(cadena)
    i = 0
    while i < len(resultado):
        if resultado[i] == '1' and i + 1 < len(resultado) and resultado[i + 1] == 'C':
            resultado.pop(i + 1); i += 1
        else:
            i += 1
    resultado = ''.join(resultado)
 
    # ── Revertir 1: reinsertar las 'A1' originales ───────────────────────────
    resultado = resultado[:longitud] + ('A1' * count_a1_real) + resultado[longitud:]
 
    # ── Revertir 0: extraer hexa y reconstruir decimal ───────────────────────
    if longitud >= len(resultado):
        return None
    hexa_insertado = resultado[longitud]
    decimal_str    = resultado[:longitud] + resultado[longitud + 1:]
    try:
        decimal = int(decimal_str)
    except ValueError:
        return None
    # Verificacion interna (suma de control del paso 0)
    if format(decimal % longitud, 'X') != hexa_insertado:
        return None
    binario = bin(decimal)[2:]
    while len(binario) % 8 != 0:
        binario = '0' + binario
    texto = ''
    for k in range(0, len(binario), 8):
        b = binario[k:k + 8]
        texto += chr(int(b, 2))
    return texto
 
 
# -----------------------------------------------------------------------------
#  Intento de descifrado: reconstruccion guiada por restricciones.
#  Muestra hasta 'max_intentos' candidatos concretos (relleno de huecos,
#  resultado de la verificacion y texto al que descifro). Para temprano si
#  encuentra el original.
# -----------------------------------------------------------------------------
def intentar_descifrar(cifrado, longitud, count_a1_real, count_a1_insertar,
                       count_c, info_vueltas_c1, count_c1_previo, info_eliminados,
                       longitud_post6, original=None, max_intentos=20, semilla=7):
    """
    El paso 7 borro los caracteres en indices impares de una cadena de longitud
    'longitud_post6'. Sabemos DONDE estan los huecos, no su valor. Probamos
    rellenos plausibles (sesgados a digitos, que dominan en esa etapa) y usamos
    la verificacion hexa del paso 0 (dentro de descifrar_resto) como filtro.
 
    Devuelve (encontrado | None, intentos_log) donde cada entrada del log es
    (numero, cifrado_reconstruido, estado, texto). Los intentos que fallan la
    verificacion hexa NO se incluyen en el log (pero si cuentan para el tope).
    """
    random.seed(semilla)
    cadena_post7 = reinsertar_seguidos(cifrado, info_eliminados)
    huecos = sorted(idx for idx in range(longitud_post6) if idx % 2 == 1)
    n = len(huecos)
    alfabeto = '0123456789ABCDEF'
    pesos = [10] * 10 + [2, 1, 1, 1, 1, 1]   # digitos frecuentes, A-F raros
 
    intentos_log = []
    encontrado = None
 
    for intento in range(1, max_intentos + 1):
        if intento == 1:
            combo = ['0'] * n                # intento base: todo ceros
        else:
            combo = [random.choices(alfabeto, weights=pesos, k=1)[0] for _ in range(n)]
 
        recon = list(cadena_post7)
        for h, val in zip(huecos, combo):
            recon.insert(h, val)
        recon = ''.join(recon)   # cifrado con los huecos rellenados
 
        if len(recon) != longitud_post6:
            continue
 
        texto = descifrar_resto(recon, longitud, count_a1_real, count_a1_insertar,
                                count_c, info_vueltas_c1, count_c1_previo)
        if texto is None:
            # Fallo la verificacion hexa: no se muestra este intento.
            continue
 
        imprimible = all(32 <= ord(ch) < 127 for ch in texto)
        estado = "texto imprimible" if imprimible else "texto no imprimible"
        intentos_log.append((intento, recon, estado, texto))
        if original is not None and texto == original:
            encontrado = texto
            break
 
    return encontrado, intentos_log
 
 
# -----------------------------------------------------------------------------
#  Demostracion
# -----------------------------------------------------------------------------
if __name__ == '__main__':
  
    arreglo_valores=["Daniel", "Juan", "Erick", "Carina", "Ana", "Simar", "Inter Ciencias2", "UDistri"]
    
    for prueba in arreglo_valores:
        salida = cifrar(prueba)
        (cif, longitud, ca1r, ca1i, cc, ivc, cc1p, ie, lp6) = salida
 
        print("=" * 70)
        print(f"Texto real: {prueba!r}")
        print(f"Cifrado:             {cif}")
        huecos = sum(1 for idx in range(lp6) if idx % 2 == 1)
        print(f"Huecos a reconstruir: {huecos}")
        print("-" * 70)
 
        enc, log = intentar_descifrar(
            cif, longitud, ca1r, ca1i, cc, ivc, cc1p, ie, lp6,                      #HOLA ESTIMADOS PARA CAMBIAR EL NÚMERO DE INTENTOS ES ACÁ, PARA PONER O QUITAR PALABRAS DE PRUEBA ES PURO ARRIBA
            original=prueba, max_intentos=980)
 
        print(f"{'#':>3}  {'cifrado con huecos rellenados':<34}  {'resultado':<22}  texto")
        print("-" * 70)
        for intento, recon, estado, texto in log:
            recon_show = (recon[:32] + '..') if len(recon) > 34 else recon
            txt_show   = str(texto) if texto is not None else '-'
            print(f"{intento:>3}  {recon_show:<34}  {estado:<22}  {txt_show}")
        print("-" * 70)
        if enc is not None:
            print(f"RESULTADO: se encontro el original {enc!r} (parada temprana).")
        else:
            print(f"RESULTADO: ninguno de los intentos mostrados acerto "
                  f"(esperado: el paso 7 destructivo hace inviable la reconstruccion).")
            print(f"           (los intentos que fallaron la verificacion hexa se omiten)")
        print()
