"""
Librería de Algoritmos de Ordenamiento Externo y Mezcla
Archivo: externas.py
"""

def intercalacion(arr1, arr2):
    """Intercala dos listas previamente ordenadas en una sola lista ordenada."""
    result = []
    i = j = 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result


def mezcla_directa(arr):
    """Ordena una lista usando el algoritmo de Mezcla Directa (Merge Sort)."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = mezcla_directa(arr[:mid])
    right = mezcla_directa(arr[mid:])
    return intercalacion(left, right)


def mezcla_equilibrada(arr):
    """Ordena una lista localizando tramos naturalmente ordenados."""
    if len(arr) <= 1:
        return arr

    def buscar_tramos(lista):
        tramos = []
        n = len(lista)
        i = 0
        while i < n:
            inicio = i
            while i < n - 1 and lista[i] <= lista[i + 1]:
                i += 1
            i += 1
            tramos.append(lista[inicio:i])
        return tramos

    tramos = buscar_tramos(arr)
    while len(tramos) > 1:
        nuevos_tramos = []
        for i in range(0, len(tramos), 2):
            if i + 1 < len(tramos):
                fusionado = intercalacion(tramos[i], tramos[i + 1])
                nuevos_tramos.append(fusionado)
            else:
                nuevos_tramos.append(tramos[i])
        tramos = nuevos_tramos

    return tramos[0] if tramos else []