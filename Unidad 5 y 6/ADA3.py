import tkinter as tk
from tkinter import ttk, messagebox


# ---------------- MÉTODOS DE ORDENAMIENTO ---------------- #

def intercalacion(lista, pasos):
    mitad = len(lista) // 2
    izquierda = sorted(lista[:mitad])
    derecha = sorted(lista[mitad:])

    pasos.append(f"Sublista izquierda ordenada: {izquierda}")
    pasos.append(f"Sublista derecha ordenada: {derecha}")

    resultado = []
    i = j = 0

    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] < derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

        pasos.append(f"Proceso: {resultado}")

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])

    pasos.append(f"Resultado final: {resultado}")

    return resultado


def mezcla_directa(lista, pasos):
    if len(lista) <= 1:
        return lista

    medio = len(lista) // 2
    izquierda = mezcla_directa(lista[:medio], pasos)
    derecha = mezcla_directa(lista[medio:], pasos)

    return fusionar(izquierda, derecha, pasos)


def fusionar(izquierda, derecha, pasos):
    resultado = []
    i = j = 0

    pasos.append(f"Dividiendo: {izquierda} | {derecha}")

    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] < derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

        pasos.append(f"Mezclando: {resultado}")

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])

    pasos.append(f"Fusionado: {resultado}")

    return resultado


def mezcla_equilibrada(lista, pasos):
    if len(lista) <= 1:
        return lista

    mitad = len(lista) // 2
    izquierda = mezcla_equilibrada(lista[:mitad], pasos)
    derecha = mezcla_equilibrada(lista[mitad:], pasos)

    return combinar(izquierda, derecha, pasos)


def combinar(izquierda, derecha, pasos):
    resultado = []

    pasos.append(f"Bloques: {izquierda} | {derecha}")

    while izquierda and derecha:
        if izquierda[0] < derecha[0]:
            resultado.append(izquierda.pop(0))
        else:
            resultado.append(derecha.pop(0))

        pasos.append(f"Combinando: {resultado}")

    resultado += izquierda
    resultado += derecha

    pasos.append(f"Bloque ordenado: {resultado}")

    return resultado


# ---------------- INTERFAZ GRÁFICA ---------------- #

def ordenar():
    entrada = entry_numeros.get()

    try:
        numeros = [int(x.strip()) for x in entrada.split(",")]
    except:
        messagebox.showerror(
            "Error",
            "Ingresa números válidos separados por comas."
        )
        return

    metodo = combo_metodo.get()

    if not metodo:
        messagebox.showwarning(
            "Advertencia",
            "Selecciona un método."
        )
        return

    pasos = []

    resultado_texto.delete("1.0", tk.END)

    if metodo == "Intercalación":
        resultado = intercalacion(numeros, pasos)

    elif metodo == "Mezcla Directa":
        resultado = mezcla_directa(numeros, pasos)

    elif metodo == "Mezcla Equilibrada":
        resultado = mezcla_equilibrada(numeros, pasos)

    else:
        return

    resultado_texto.insert(
        tk.END,
        f"Lista original: {numeros}\n\n"
    )

    for paso in pasos:
        resultado_texto.insert(tk.END, paso + "\n")

    resultado_texto.insert(
        tk.END,
        f"\nLista ordenada final: {resultado}"
    )


# ---------------- VENTANA ---------------- #

ventana = tk.Tk()
ventana.title("Métodos de Ordenamiento")
ventana.geometry("850x700")
ventana.config(bg="#f0f0f0")


# -------- TÍTULO -------- #
titulo = tk.Label(
    ventana,
    text="Sistema de Métodos de Ordenamiento",
    font=("Arial", 18, "bold"),
    bg="#f0f0f0"
)
titulo.pack(pady=15)


# -------- ENTRADA -------- #
label_numeros = tk.Label(
    ventana,
    text="Ingresa números separados por comas:",
    font=("Arial", 12),
    bg="#f0f0f0"
)
label_numeros.pack()

entry_numeros = tk.Entry(
    ventana,
    width=60,
    font=("Arial", 12)
)
entry_numeros.pack(pady=10)


# -------- MÉTODO -------- #
label_metodo = tk.Label(
    ventana,
    text="Selecciona método:",
    font=("Arial", 12),
    bg="#f0f0f0"
)
label_metodo.pack()

combo_metodo = ttk.Combobox(
    ventana,
    values=[
        "Intercalación",
        "Mezcla Directa",
        "Mezcla Equilibrada"
    ],
    state="readonly",
    width=30,
    font=("Arial", 11)
)
combo_metodo.pack(pady=10)


# -------- BOTÓN -------- #
boton_ordenar = tk.Button(
    ventana,
    text="Ordenar",
    command=ordenar,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 13)
)
boton_ordenar.pack(pady=15)


# -------- RESULTADOS -------- #
label_resultado = tk.Label(
    ventana,
    text="Proceso y Resultado:",
    font=("Arial", 12),
    bg="#f0f0f0"
)
label_resultado.pack()

resultado_texto = tk.Text(
    ventana,
    width=95,
    height=25,
    font=("Consolas", 10)
)
resultado_texto.pack(pady=10)


# -------- EJECUCIÓN -------- #
ventana.mainloop()