# ==========================================
# INTERFAZ GRÁFICA PARA ORDENAMIENTO TXT
# - Carga archivos TXT
# - Selecciona método
# - Ordena números
# - Guarda resultado en nuevo TXT
# ==========================================

import tkinter as tk
from tkinter import filedialog, messagebox, ttk


# -------- MÉTODOS DE ORDENAMIENTO -------- #
def intercalacion(lista):
    mitad = len(lista) // 2
    izquierda = sorted(lista[:mitad])
    derecha = sorted(lista[mitad:])

    resultado = []
    i = j = 0

    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] < derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])

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

    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] < derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])

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

    while izquierda and derecha:
        if izquierda[0] < derecha[0]:
            resultado.append(izquierda.pop(0))
        else:
            resultado.append(derecha.pop(0))

    resultado += izquierda
    resultado += derecha

    return resultado


# -------- ARCHIVOS TXT -------- #
def leer_txt(nombre_archivo):
    numeros = []

    try:
        with open(nombre_archivo, "r") as archivo:
            contenido = archivo.read()

            for dato in contenido.replace("\n", ",").split(","):
                dato = dato.strip()

                if dato:
                    try:
                        numeros.append(int(dato))
                    except:
                        pass

    except:
        messagebox.showerror("Error", "No se pudo leer el archivo.")

    return numeros


def guardar_txt(nombre_archivo, lista):
    try:
        with open(nombre_archivo, "w") as archivo:
            archivo.write(",".join(map(str, lista)))

    except:
        messagebox.showerror("Error", "No se pudo guardar el archivo.")


# -------- VARIABLES -------- #
archivo_seleccionado = ""
datos = []


# -------- FUNCIONES INTERFAZ -------- #
def seleccionar_archivo():
    global archivo_seleccionado

    archivo = filedialog.askopenfilename(
        title="Selecciona archivo TXT",
        filetypes=[("Archivos TXT", "*.txt")]
    )

    if archivo:
        archivo_seleccionado = archivo
        entry_archivo.config(state="normal")
        entry_archivo.delete(0, tk.END)
        entry_archivo.insert(0, archivo)
        entry_archivo.config(state="readonly")


def ordenar_archivo():
    global datos

    if not archivo_seleccionado:
        messagebox.showwarning("Advertencia", "Selecciona un archivo TXT.")
        return

    datos = leer_txt(archivo_seleccionado)

    if not datos:
        messagebox.showerror("Error", "No se encontraron números válidos.")
        return

    metodo = combo_metodo.get()

    if metodo == "Intercalación":
        resultado = intercalacion(datos)

    elif metodo == "Mezcla Directa":
        resultado = mezcla_directa(datos)

    elif metodo == "Mezcla Equilibrada":
        resultado = mezcla_equilibrada(datos)

    else:
        messagebox.showwarning("Advertencia", "Selecciona un método.")
        return

    resultado_texto.delete("1.0", tk.END)
    resultado_texto.insert(tk.END, str(resultado))

    guardar = messagebox.askyesno("Guardar", "¿Deseas guardar el resultado?")

    if guardar:
        archivo_salida = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo TXT", "*.txt")]
        )

        if archivo_salida:
            guardar_txt(archivo_salida, resultado)
            messagebox.showinfo(
                "Éxito",
                f"Archivo guardado en:\n{archivo_salida}"
            )


# -------- VENTANA -------- #
ventana = tk.Tk()
ventana.title("Ordenamiento de Archivos TXT")
ventana.geometry("750x550")
ventana.config(bg="#f0f0f0")


# -------- TÍTULO -------- #
titulo = tk.Label(
    ventana,
    text="Sistema de Ordenamiento TXT",
    font=("Arial", 18, "bold"),
    bg="#f0f0f0"
)
titulo.pack(pady=15)


# -------- SELECCIÓN DE ARCHIVO -------- #
btn_archivo = tk.Button(
    ventana,
    text="Seleccionar Archivo TXT",
    command=seleccionar_archivo,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12)
)
btn_archivo.pack(pady=10)

entry_archivo = tk.Entry(
    ventana,
    width=90,
    state="readonly"
)
entry_archivo.pack(pady=5)


# -------- MÉTODO -------- #
label_metodo = tk.Label(
    ventana,
    text="Selecciona método de ordenamiento:",
    font=("Arial", 12),
    bg="#f0f0f0"
)
label_metodo.pack(pady=10)

combo_metodo = ttk.Combobox(
    ventana,
    values=[
        "Intercalación",
        "Mezcla Directa",
        "Mezcla Equilibrada"
    ],
    state="readonly",
    width=30
)
combo_metodo.pack(pady=5)


# -------- BOTÓN ORDENAR -------- #
btn_ordenar = tk.Button(
    ventana,
    text="Ordenar Archivo",
    command=ordenar_archivo,
    bg="#2196F3",
    fg="white",
    font=("Arial", 12)
)
btn_ordenar.pack(pady=15)


# -------- RESULTADO -------- #
label_resultado = tk.Label(
    ventana,
    text="Resultado:",
    font=("Arial", 12),
    bg="#f0f0f0"
)
label_resultado.pack()

resultado_texto = tk.Text(
    ventana,
    width=85,
    height=12
)
resultado_texto.pack(pady=10)


# -------- EJECUCIÓN -------- #
ventana.mainloop()