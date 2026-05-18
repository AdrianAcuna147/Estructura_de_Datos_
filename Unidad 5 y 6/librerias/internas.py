"""
Librería de Algoritmos de Ordenamiento Interno
Archivo: internas.py
"""

def bubble_sort(arr):
    """Ordena una lista utilizando el método de Burbuja optimizado."""
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def insertion_sort(arr):
    """Ordena una lista utilizando el método de Inserción."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def selection_sort(arr):
    """Ordena una lista utilizando el método de Selección."""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def shell_sort(arr):
    """Ordena una lista utilizando el método ShellSort."""
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


def quicksort(arr):
    """Ordena una lista utilizando el método QuickSort (In-place)."""
    def _quicksort(lista, low, high):
        if low < high:
            p_idx = _partition(lista, low, high)
            _quicksort(lista, low, p_idx - 1)
            _quicksort(lista, p_idx + 1, high)

    def _partition(lista, low, high):
        pivot = lista[high]
        i = low - 1
        for j in range(low, high):
            if lista[j] <= pivot:
                i += 1
                lista[i], lista[j] = lista[j], lista[i]
        lista[i + 1], lista[high] = lista[high], lista[i + 1]
        return i + 1

    _quicksort(arr, 0, len(arr) - 1)
    return arr


def heapsort(arr):
    """Ordena una lista utilizando el método HeapSort."""
    def heapify(lista, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and lista[left] > lista[largest]:
            largest = left
        if right < n and lista[right] > lista[largest]:
            largest = right

        if largest != i:
            lista[i], lista[largest] = lista[largest], lista[i]
            heapify(lista, n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr


def radix_sort(arr):
    """Ordena una lista de enteros no negativos usando Radix Sort."""
    if not arr:
        return arr

    def counting_sort_for_radix(lista, exp):
        n = len(lista)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = lista[i] // exp
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = lista[i] // exp
            output[count[index % 10] - 1] = lista[i]
            count[index % 10] -= 1
            i -= 1

        for i in range(n):
            lista[i] = output[i]

    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort_for_radix(arr, exp)
        exp *= 10
    return arr