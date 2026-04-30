def shell_sort(arr):
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
        print(f"  gap={gap}: {arr}")
        gap //= 2

    return arr
def quick_sort(arr, low=0, high=None, _top_level=True):
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_index = _partition(arr, low, high)
        print(f"  pivote={arr[pivot_index]}: {arr[low:high+1]}")
        quick_sort(arr, low, pivot_index - 1, _top_level=False)
        quick_sort(arr, pivot_index + 1, high, _top_level=False)

    return arr


def _partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
def heap_sort(arr):
    n = len(arr)

    # Construir el max-heap
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)

    print(f"  heap construido: {arr}")

    # Extraer elementos del heap uno por uno
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0)
        print(f"  extraer {arr[i]}: {arr[:i]}")

    return arr


def _heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest)
def radix_sort(arr):
    if not arr:
        return arr

    max_val = max(arr)
    exp = 1

    while max_val // exp > 0:
        _counting_sort_by_digit(arr, exp)
        print(f"  exp={exp} (dígito {len(str(exp))}): {arr}")
        exp *= 10

    return arr


def _counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for num in arr:
        index = (num // exp) % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    for i in range(n):
        arr[i] = output[i]



def mostrar_menu():
    print("\n" + "=" * 50)
    print("   MÉTODOS DE ORDENAMIENTO")
    print("=" * 50)
    print("  1. ShellSort")
    print("  2. QuickSort")
    print("  3. HeapSort")
    print("  4. Radix Sort")
    print("  5. Salir")
    print("=" * 50)


def pedir_numeros():
    while True:
        try:
            cantidad = int(input("\n¿Cuántos números deseas ordenar? "))
            if cantidad <= 0:
                print("  Ingresa un número mayor a 0.")
                continue
            break
        except ValueError:
            print("  Valor inválido. Ingresa un número entero.")

    numeros = []
    print(f"Ingresa {cantidad} número(s):")
    for i in range(cantidad):
        while True:
            try:
                n = int(input(f"  Número {i + 1}: "))
                if n < 0:
                    print("  Solo números positivos (Radix Sort no soporta negativos).")
                    continue
                numeros.append(n)
                break
            except ValueError:
                print("  Valor inválido. Ingresa un entero.")
    return numeros


def ejecutar_algoritmo(opcion, numeros):
    algoritmos = {
        1: ("ShellSort",  shell_sort),
        2: ("QuickSort",  quick_sort),
        3: ("HeapSort",   heap_sort),
        4: ("Radix Sort", radix_sort),
    }

    nombre, funcion = algoritmos[opcion]
    arr_copia = numeros[:]  # trabajar sobre copia para no modificar original

    print(f"\n--- {nombre} ---")
    print(f"Original: {numeros}")
    print("Pasos:")

    resultado = funcion(arr_copia)

    print(f"\nOrdenado: {resultado}")


def main():
    print("\nBienvenido al programa de Métodos de Ordenamiento")

    while True:
        mostrar_menu()

        try:
            opcion = int(input("\nElige una opción (1-5): "))
        except ValueError:
            print("  Opción inválida.")
            continue

        if opcion == 5:
            print("\n¡Hasta luego!\n")
            break
        elif opcion in (1, 2, 3, 4):
            numeros = pedir_numeros()
            ejecutar_algoritmo(opcion, numeros)
        else:
            print("  Opción fuera de rango. Elige entre 1 y 5.")
if __name__ == "__main__":
    main()