from lib_bus.busqueda import Busqueda, TablaHash
from librerias import internas, externas

def mostrar_menu():
    print("\n==================================================")
    print("      MENÚ INTERACTIVO DE MÉTODOS DE BÚSQUEDA")
    print("==================================================")
    print("1. Búsqueda Secuencial (Buscar una ciudad)")
    print("2. Búsqueda Binaria (Buscar un ID de estantería)")
    print("3. Búsqueda por Hash (Registrar y buscar un paquete)")
    print("4. Salir del programa")
    print("==================================================")

# --- Preparación de datos de respaldo si tus archivos están vacíos ---
try:
    lista_ciudades = externas.obtener_ciudades_ruta()
except AttributeError:
    lista_ciudades = ["Monterrey", "Guadalajara", "Mérida", "Cancún", "Puebla"]

try:
    lista_estanterias = internas.obtener_estanterias()
except AttributeError:
    lista_estanterias = [10, 25, 45, 55, 70, 85, 90] # Ya ordenada para Binaria

# Inicializamos la tabla hash fuera del bucle para que conserve los datos guardados
control_inventario = TablaHash(tamaño_tabla=5)


while True:
    mostrar_menu()
    opcion = input("Elige una opción (1-4): ").strip()

    if opcion == "1":
        print("\n--- [ EJECUTANDO BÚSQUEDA SECUENCIAL ] ---")
        print(f"Datos disponibles (Ciudades): {lista_ciudades}")
        ciudad = input("Ingresa el nombre de la ciudad que deseas buscar: ").strip()
        
        resultado = Busqueda.secuencial(lista_ciudades, ciudad)
        if resultado != -1:
            print(f"¡Encontrada! '{ciudad}' está en la posición {resultado} de la lista.")
        else:
            print(f"La ciudad '{ciudad}' no se encuentra en la lista de rutas.")

    elif opcion == "2":
        print("\n--- [ EJECUTANDO BÚSQUEDA BINARIA ] ---")
        print(f"Datos disponibles ordenados (Estanterías): {lista_estanterias}")
        
        try:
            id_estante = int(input("Ingresa el número de estantería a buscar: "))
            resultado = Busqueda.binaria(lista_estanterias, id_estante)
            
            if resultado != -1:
                print(f"¡Encontrado! El estante {id_estante} está en el índice {resultado}.")
            else:
                print(f"El estante {id_estante} no está registrado en el inventario local.")
        except ValueError:
            print("Error: Por favor, ingresa un número entero válido.")

    elif opcion == "3":
        print("\n--- [ EJECUTANDO BÚSQUEDA POR HASH ] ---")
        print("1. Registrar nuevo paquete")
        print("2. Buscar paquete existente")
        sub_opcion = input("Elige una acción (1 o 2): ").strip()

        if sub_opcion == "1":
            codigo = input("Ingresa el código del paquete (ej. P-10): ").strip()
            contenido = input("Ingresa la descripción del contenido: ").strip()
            control_inventario.insertar(codigo, contenido)
            print(f"¡Paquete [{codigo}] registrado con éxito en la Tabla Hash!")
            
        elif sub_opcion == "2":
            codigo = input("Ingresa el código del paquete a buscar: ").strip()
            resultado = control_inventario.buscar(codigo)
            if resultado:
                print(f"¡Paquete Encontrado! Contenido: {resultado}")
            else:
                print(f"El paquete con código [{codigo}] no existe en la Tabla Hash.")
        else:
            print("Opción no válida en el submenú.")

    elif opcion == "4":
        print("\n¡Gracias por usar el simulador de búsquedas! Saliendo...")
        break
    else:
        print("\nOpción inválida. Por favor, selecciona un número del 1 al 4.")