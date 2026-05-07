# ---------------- MÉTODOS DE ORDENAMIENTO ---------------- #

def intercalacion(lista):
    mitad = len(lista) // 2
    izquierda = sorted(lista[:mitad])
    derecha = sorted(lista[mitad:])

    print("\nSublista izquierda ordenada:", izquierda)
    print("Sublista derecha ordenada:", derecha)

    resultado = []
    i = j = 0

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

    print("Resultado final:", resultado)
    return resultado


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

    print("Fusionado:", resultado)
    return resultado


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

    print("Bloque ordenado:", resultado)
    return resultado


# ---------------- INTERFAZ EN TERMINAL ---------------- #

def menu():
    while True:
        print("\n====== MÉTODOS DE ORDENAMIENTO ======")
        print("1. Intercalación")
        print("2. Mezcla Directa")
        print("3. Mezcla Equilibrada")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "4":
            print("Programa finalizado.")
            break

        entrada = input("Ingresa números separados por comas: ")

        try:
            numeros = [int(x.strip()) for x in entrada.split(",")]
        except:
            print("Error: Ingresa solo números válidos.")
            continue

        print("\nLista original:", numeros)

        if opcion == "1":
            metodo = "Intercalación"
            resultado = intercalacion(numeros)

        elif opcion == "2":
            metodo = "Mezcla Directa"
            resultado = mezcla_directa(numeros)

        elif opcion == "3":
            metodo = "Mezcla Equilibrada"
            resultado = mezcla_equilibrada(numeros)

        else:
            print("Opción no válida.")
            continue

        print(f"\nMétodo seleccionado: {metodo}")
        print("Lista ordenada final:", resultado)


# Ejecutar programa
menu()