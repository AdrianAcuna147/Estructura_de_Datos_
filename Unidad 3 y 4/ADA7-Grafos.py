"""
=============================================================
  GRAFO DE ESTADOS DE MÉXICO - RECORRIDO Y KILÓMETROS
  7 estados: CDMX, Puebla, Veracruz, Oaxaca,
             Guerrero, Morelos, Tlaxcala
=============================================================
"""

import heapq
from collections import defaultdict

# ---------------------------------------------
#  1. DEFINICIÓN DEL GRAFO (Costos y KM)
# ---------------------------------------------

ESTADOS = ["CDMX", "Puebla", "Veracruz", "Oaxaca", "Guerrero", "Morelos", "Tlaxcala"]

# (estado_a, estado_b, costo_mxn, kilometros)
DATOS_ARISTAS = [
    ("CDMX",     "Puebla",    420, 130),
    ("CDMX",     "Morelos",   280, 85),
    ("CDMX",     "Guerrero",  900, 275),
    ("CDMX",     "Tlaxcala",  380, 115),
    ("Puebla",   "Tlaxcala",  120, 30),
    ("Puebla",   "Veracruz",  650, 280),
    ("Puebla",   "Oaxaca",    780, 340),
    ("Puebla",   "Morelos",   350, 110),
    ("Veracruz", "Oaxaca",    600, 365),
    ("Oaxaca",   "Guerrero",  520, 450),
    ("Morelos",  "Guerrero",  400, 190),
    ("Tlaxcala", "Veracruz",  500, 240),
]

def construir_grafo(datos):
    grafo = defaultdict(dict)
    for a, b, costo, km in datos:
        grafo[a][b] = {'costo': costo, 'km': km}
        grafo[b][a] = {'costo': costo, 'km': km}
    return grafo

# ---------------------------------------------
#  2. ALGORITMOS DE BÚSQUEDA
# ---------------------------------------------

def hamiltonian_path(grafo, estados, inicio):
    n = len(estados)
    mejor = {"camino": None, "costo": float("inf"), "km": 0}

    def backtrack(actual, visitados, camino, costo_acc, km_acc):
        if len(visitados) == n:
            if costo_acc < mejor["costo"]:
                mejor["camino"] = camino[:]
                mejor["costo"] = costo_acc
                mejor["km"] = km_acc
            return
        
        for vecino, datos in grafo[actual].items():
            if vecino not in visitados:
                visitados.add(vecino)
                camino.append(vecino)
                backtrack(vecino, visitados, camino, costo_acc + datos['costo'], km_acc + datos['km'])
                camino.pop()
                visitados.remove(vecino)

    backtrack(inicio, {inicio}, [inicio], 0, 0)
    return mejor["camino"], mejor["costo"], mejor["km"]

def distancia_minima(grafo, origen, destino):
    dist = {n: float("inf") for n in grafo}
    dist_km = {n: 0 for n in grafo}
    dist[origen] = 0
    prev = {n: None for n in grafo}
    heap = [(0, origen)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]: continue
        for v, datos in grafo[u].items():
            nd = d + datos['costo']
            if nd < dist[v]:
                dist[v] = nd
                dist_km[v] = dist_km[u] + datos['km']
                prev[v] = u
                heapq.heappush(heap, (nd, v))

    camino = []
    cur = destino
    while cur is not None:
        camino.append(cur)
        cur = prev[cur]
    camino.reverse()
    return dist[destino], dist_km[destino], camino

def recorrido_con_repeticion(grafo, estados, inicio):
    orden = [e for e in estados if e != inicio]
    camino_total = [inicio]
    costo_total = 0
    km_total = 0
    actual = inicio
    for destino in orden:
        costo, km, sub_camino = distancia_minima(grafo, actual, destino)
        camino_total.extend(sub_camino[1:])
        costo_total += costo
        km_total += km
        actual = destino
    return camino_total, costo_total, km_total

# ---------------------------------------------
#  3. DIBUJO Y VISUALIZACIÓN EN TERMINAL
# ---------------------------------------------

def dibujar_grafo_terminal():
    print("\n" + "═" * 70)
    print("      REPRESENTACIÓN VISUAL DEL GRAFO (ESTADOS Y CONEXIONES)")
    print("═" * 70)
    # Dibujo ASCII representando las conexiones principales
    print("""
    [TLAXCALA] --------(240km)------- [VERACRUZ]
        | \\                             /
       (30km) \\ (500km)                / (365km)
        |       \\                    /
    [PUEBLA] --(130km)-- [CDMX] ---/---- [OAXACA]
        |      /          /        /       /
      (110km)(420km)   (85km)   (780km) (520km)
        |    /          /        /       /
    [MORELOS] --------(190km)------- [GUERRERO]
    """)
    print("Nota: Los valores en ( ) representan la distancia en kilómetros.")

def mostrar_relaciones(grafo, estados):
    print("\n" + "═" * 70)
    print("  RELACIONES DETALLADAS: ESTADOS Y KILÓMETROS")
    print("═" * 70)
    for estado in estados:
        vecinos = grafo[estado]
        linea = f"📍 {estado:<10} -> "
        conexiones = [f"{v} ({d['km']}km)" for v, d in vecinos.items()]
        print(linea + ", ".join(conexiones))

def main():
    grafo = construir_grafo(DATOS_ARISTAS)
    inicio = "CDMX"

    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + "SISTEMA DE RUTAS: MÉXICO (7 ESTADOS)".center(68) + "║")
    print("╚" + "═" * 68 + "╝")

    # Mostrar estados y relaciones
    mostrar_relaciones(grafo, ESTADOS)

    # Dibujo en terminal
    dibujar_grafo_terminal()

    # --- INCISO A ---
    print("\n" + "═" * 70)
    print("  A) RECORRIDO SIN REPETIR (Hamiltoniano)")
    print("═" * 70)
    cam_a, cos_a, km_a = hamiltonian_path(grafo, ESTADOS, inicio)
    print(f"Ruta: {' -> '.join(cam_a)}")
    print(f"Costo Total: ${cos_a:,} MXN | Distancia Total: {km_a} km")

    # --- INCISO B ---
    print("\n" + "═" * 70)
    print("  B) RECORRIDO CON REPETICIÓN (Mínimo esfuerzo)")
    print("═" * 70)
    cam_b, cos_b, km_b = recorrido_con_repeticion(grafo, ESTADOS, inicio)
    print(f"Ruta: {' -> '.join(cam_b)}")
    print(f"Costo Total: ${cos_b:,} MXN | Distancia Total: {km_b} km")
    print("\n" + "═" * 70)

if __name__ == "__main__":
    main()