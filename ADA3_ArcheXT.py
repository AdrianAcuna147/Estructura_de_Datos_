# ==============================
# MÉTODOS DE ORDENAMIENTO CON ARCHIVOS EXTERNOS
# Lee números desde un archivo .txt
# Guarda el resultado en otro archivo .txt
# ==============================


# -------- INTERCALACIÓN -------- #
def intercalacion(lista):
    mitad = len(lista) // 2
    izquierda = sorted(lista[:mitad])
    derecha = sorted(lista[mitad:])

    resultado = []
    i = j = 0

    print("\nSublista izquierda:", izquierda)
    print("Sublista derecha:", derecha)

    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] < derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

        print("Proceso:", resultado)

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])

    return resultado


# -------- MEZCLA DIRECTA -------- #
def mezcla_directa(lista):
    if len(lista) <= 1:
        return lista

    medio = len(lista) // 2
    izquierda = mezcla_directa(lista[:medio])
    derecha = mezcla_directa(lista[medio:])

    return fusionar(izquierda, derecha)


def fusionar(izquierda, derecha):
    resultado = []
    i = j = 0

    print("\nDividiendo:", izquierda, "|", derecha)

    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] < derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

        print("Mezclando:", resultado)

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])

    return resultado


# -------- MEZCLA EQUILIBRADA -------- #
def mezcla_equilibrada(lista):
    if len(lista) <= 1:
        return lista

    mitad = len(lista) // 2
    izquierda = mezcla_equilibrada(lista[:mitad])
    derecha = mezcla_equilibrada(lista[mitad:])

    return combinar(izquierda, derecha)


def combinar(izquierda, derecha):
    resultado = []

    print("\nBloques:", izquierda, "|", derecha)

    while izquierda and derecha:
        if izquierda[0] < derecha[0]:
            resultado.append(izquierda.pop(0))
        else:
            resultado.append(derecha.pop(0))

        print("Combinando:", resultado)

    resultado += izquierda
    resultado += derecha

    return resultado


# -------- MANEJO DE ARCHIVOS -------- #
def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, "r") as archivo:
            contenido = archivo.read()
            numeros = [int(x.strip()) for x in contenido.split(",")]
            return numeros
    except:
        print("Error al leer el archivo.")
        return None


def guardar_archivo(nombre_archivo, lista):
    with open(nombre_archivo, "w") as archivo:
        archivo.write(",".join(map(str, lista)))

    print(f"\nResultado guardado en {nombre_archivo}")


# -------- MENÚ PRINCIPAL -------- #
def menu():
    while True:
        print("\n====== ORDENAMIENTO CON ARCHIVOS ======")
        print("1. Intercalación")
        print("2. Mezcla Directa")
        print("3. Mezcla Equilibrada")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "4":
            print("Programa finalizado.")
            break

        archivo_entrada = input("Ingresa el nombre del archivo de entrada (ej: numeros.txt): ")

        numeros = leer_archivo(archivo_entrada)

        if numeros is None:
            continue

        print("\nLista original:", numeros)

        if opcion == "1":
            resultado = intercalacion(numeros)
            metodo = "Intercalación"

        elif opcion == "2":
            resultado = mezcla_directa(numeros)
            metodo = "Mezcla Directa"

        elif opcion == "3":
            resultado = mezcla_equilibrada(numeros)
            metodo = "Mezcla Equilibrada"

        else:
            print("Opción no válida.")
            continue

        print(f"\nMétodo utilizado: {metodo}")
        print("Lista ordenada:", resultado)

        archivo_salida = input("Ingresa el nombre del archivo de salida (ej: resultado.txt): ")
        guardar_archivo(archivo_salida, resultado)


# -------- EJECUCIÓN -------- #
menu()