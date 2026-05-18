# Importamos tus librerías usando la ruta de la carpeta
import librerias.internas as int_sort
import librerias.externas as ext_sort

# 1. Crear una lista desordenada
mi_lista = [54, 26, 93, 17, 77, 31, 44, 55, 20]
print(f"Lista original: {mi_lista}")

# 2. Usar un método de internas.py (ej. QuickSort)
resultado_quicksort = int_sort.quicksort(mi_lista.copy())
print(f"Ordenado con QuickSort: {resultado_quicksort}")

# 3. Usar un método de externas.py (ej. Mezcla Directa)
resultado_mezcla = ext_sort.mezcla_directa(mi_lista.copy())
print(f"Ordenado con Mezcla Directa: {resultado_mezcla}")