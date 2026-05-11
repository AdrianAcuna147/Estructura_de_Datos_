from internas import OrdenacionInterna
from externas import OrdenacionExterna

def main():
    datos = [54, 26, 93, 17, 77, 31, 44, 55, 20]
    
    print("--- MÉTODOS DE ORDENACIÓN INTERNA ---")
    print(f"Original:   {datos}")
    print(f"Burbuja:    {OrdenacionInterna.burbuja(datos[:])}")
    print(f"Inserción:  {OrdenacionInterna.insercion(datos[:])}")
    print(f"Selección:  {OrdenacionInterna.seleccion(datos[:])}")
    print(f"ShellSort:  {OrdenacionInterna.shell_sort(datos[:])}")
    print(f"QuickSort:  {OrdenacionInterna.quicksort(datos[:])}")
    print(f"HeapSort:   {OrdenacionInterna.heapsort(datos[:])}")
    print(f"RadixSort:  {OrdenacionInterna.radix_sort(datos[:])}")

    print("\n--- MÉTODOS DE ORDENACIÓN EXTERNA ---")
    lista_a = [10, 30, 50]
    lista_b = [20, 40, 60]
    print(f"Intercalación (A+B): {OrdenacionExterna.intercalacion(lista_a, lista_b)}")
    print(f"Mezcla Directa:      {OrdenacionExterna.mezcla_directa(datos[:])}")
    print(f"Mezcla Equilibrada:  {OrdenacionExterna.mezcla_equilibrada(datos[:])}")

if __name__ == "__main__":
    main()