import time
def factorial(n):
    if n == 0 or n == 1:  
        return 1
    else:
        return n * factorial(n - 1)  


numero = 5

inicio = time.perf_counter()
resultado = factorial(numero)
fin = time.perf_counter()

duracion = fin - inicio

print("Factorial de", numero, "es:", factorial(numero))
print(f"tiempo de ejecucion: {duracion: .10f} segundos")