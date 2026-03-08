import time 
def factorial(n):
    resultado = 1

    for i in range(1, n + 1):
        resultado *= i

    return resultado


numero = 5

inicio = time.perf_counter()
resultado = factorial(numero)
fin = time.perf_counter()

duracion = fin - inicio 

print("Factorial de", numero, "es:", factorial(numero))
print(f"tiempo de ejecucion: {duracion: .10f} segundos")