#algoritmo de gijkstra#

import heapq

def dijkstra(grafo, inicio):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    prioridad = [(0, inicio)]
    
    while prioridad:
        distancia_actual, nodo_actual = heapq.heappop(prioridad)
        
        if distancia_actual > distancias[nodo_actual]:
            continue
            
        for vecino, peso in grafo[nodo_actual].items():
            distancia = distancia_actual + peso
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                heapq.heappush(prioridad, (distancia, vecino))
    return distancias

# Ejemplo de uso
grafo = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}
print("Dijkstra desde A:", dijkstra(grafo, 'A'))

#Floyd-Warshall#

def floyd_warshall(matriz):
    n = len(matriz)
    dist = list(map(lambda i: list(map(lambda j: j, i)), matriz))
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist

# INF representa que no hay conexión directa
INF = float('inf')
matriz_adyacencia = [
    [0, 3, INF, 7],
    [8, 0, 2, INF],
    [5, INF, 0, 1],
    [2, INF, INF, 0]
]
print("Matriz de distancias mínimas (Floyd):", floyd_warshall(matriz_adyacencia))

#Warshall#

def warshall(matriz):
    n = len(matriz)
    clausura = [fila[:] for fila in matriz]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                clausura[i][j] = clausura[i][j] or (clausura[i][k] and clausura[k][j])
    return clausura

# 1 si hay camino, 0 si no
matriz_binaria = [
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0],
    [1, 0, 1, 0]
]
print("Clausura transitiva (Warshall):", warshall(matriz_binaria))

#Kruskal#

def kruskal(nodos, aristas):
    aristas.sort(key=lambda x: x[2]) # Ordenar por peso
    padre = {n: n for n in nodos}
    
    def buscar(i):
        if padre[i] == i: return i
        return buscar(padre[i])

    mst = []
    for u, v, peso in aristas:
        raiz_u = buscar(u)
        raiz_v = buscar(v)
        if raiz_u != raiz_v:
            mst.append((u, v, peso))
            padre[raiz_u] = raiz_v
    return mst

# (Nodo1, Nodo2, Peso)
lista_aristas = [
    ('A', 'B', 10), ('A', 'C', 6), ('A', 'D', 5),
    ('B', 'D', 15), ('C', 'D', 4)
]
nodos = ['A', 'B', 'C', 'D']
print("Aristas del Árbol de Expansión Mínima (Kruskal):", kruskal(nodos, lista_aristas))