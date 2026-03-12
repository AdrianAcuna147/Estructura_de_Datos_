import time

movimientos = 0
inicio = time.time()
limite = 120  

def hanoi(n, origen, auxiliar, destino):
    global movimientos, inicio

    
    if time.time() - inicio > limite:
        raise TimeoutError

    if n == 1:
        movimientos += 1
        return

    hanoi(n-1, origen, destino, auxiliar)

    movimientos += 1

    hanoi(n-1, auxiliar, origen, destino)


n = int(input("Número de discos: "))

movimientos_totales = (2**n) - 1

try:
    hanoi(n, "A", "B", "C")

    fin = time.time()
    print("Se completó el algoritmo")
    print("Movimientos:", movimientos)
    print("Tiempo:", fin - inicio, "segundos")

except TimeoutError:
    tiempo_actual = time.time() - inicio

    velocidad = movimientos / tiempo_actual
    tiempo_estimado = movimientos_totales / velocidad

    print("\nTiempo límite alcanzado (2 minutos)")
    print("Movimientos realizados:", movimientos)
    print("Movimientos totales:", movimientos_totales)

    print("Velocidad aproximada:", round(velocidad,2), "movimientos/segundo")

    print("Tiempo estimado total:", round(tiempo_estimado,2), "segundos")

    dias = tiempo_estimado / 86400
    años = dias / 365

    print("≈", round(dias,2), "días")
    print("≈", round(años,2), "años")