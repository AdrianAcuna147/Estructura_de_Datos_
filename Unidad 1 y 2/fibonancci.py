import time

def fib_recursivo(n):
    if n <= 1:
        return n
    return fib_recursivo(n-1) + fib_recursivo(n-2)

def fib_iterativo(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a


n = 35


inicio = time.time()
resultado_rec = fib_recursivo(n)
fin = time.time()
tiempo_rec = fin - inicio


inicio = time.time()
resultado_it = fib_iterativo(n)
fin = time.time()
tiempo_it = fin - inicio


print("Fibonacci recursivo:", resultado_rec)
print(f"Tiempo recursivo: {tiempo_rec: .2f} segundos")

print("Fibonacci iterativo:", resultado_it)

#aqui tuve que ponerle que mustre 5 decimales por que es muy rapido y solo mostraria 00
print(f"Tiempo iterativo: {tiempo_it: .5f} segudnos")
      