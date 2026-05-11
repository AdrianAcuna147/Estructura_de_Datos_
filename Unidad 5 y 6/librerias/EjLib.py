import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import threading
import os

try:
    import pandas as pd
except ImportError:
    pd = None

from internas import OrdenacionInterna
from externas import OrdenacionExterna

class AplicacionOrdenacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusión y Ordenamiento Multifuente")
        self.root.geometry("850x900")
        self.root.configure(bg="#2c3e50")
        
        self.historial_tiempos = {}
        self.datos_preparados = []

        # --- Interfaz Gráfica ---
        tk.Label(root, text="SISTEMA DE FUSIÓN Y ORDENAMIENTO", font=("Arial", 16, "bold"), bg="#2c3e50", fg="white").pack(pady=15)

        # 1. Carga de Datos Múltiples
        frame_carga = tk.LabelFrame(root, text=" 1. Carga de Archivos (Múltiples permitidos) ", bg="#2c3e50", fg="white", padx=10, pady=10)
        frame_carga.pack(pady=10, padx=20, fill="x")

        self.btn_archivo = tk.Button(frame_carga, text="SELECCIONAR ARCHIVOS", command=self.cargar_archivos_multiples, bg="#3498db", fg="white", font=("bold"))
        self.btn_archivo.pack(side="left", padx=5)

        tk.Label(frame_carga, text="O manual:", bg="#2c3e50", fg="white").pack(side="left", padx=5)
        self.entrada_manual = tk.Entry(frame_carga, width=35)
        self.entrada_manual.pack(side="left", padx=5)

        # 2. Selección de Algoritmo y Control
        frame_alg = tk.Frame(root, bg="#2c3e50")
        frame_alg.pack(pady=10)

        self.metodo_var = tk.StringVar()
        self.combo_metodos = ttk.Combobox(frame_alg, textvariable=self.metodo_var, state="readonly", width=25)
        self.combo_metodos['values'] = ("Burbuja", "Inserción", "Selección", "ShellSort", "QuickSort", "HeapSort", "Radix", "Intercalación", "Mezcla Directa", "Mezcla Equilibrada")
        self.combo_metodos.pack(side="left", padx=10)
        self.combo_metodos.current(0)

        self.btn_ejecutar = tk.Button(frame_alg, text="ORDENAR TODO", command=self.iniciar_hilo, bg="#27ae60", fg="white", font=("Arial", 10, "bold"))
        self.btn_ejecutar.pack(side="left", padx=5)

        self.btn_limpiar = tk.Button(frame_alg, text="LIMPIAR CONSOLA", command=self.limpiar_consola_visual, bg="#c0392b", fg="white")
        self.btn_limpiar.pack(side="left", padx=5)

        # 3. Consola
        self.txt_proceso = tk.Text(root, height=18, width=95, state="disabled", bg="#1e1e1e", fg="#00ff00", font=("Consolas", 9))
        self.txt_proceso.pack(pady=10, padx=20)

        # 4. Tabla
        self.tree = ttk.Treeview(root, columns=("Metodo", "Tiempo"), show="headings", height=5)
        self.tree.heading("Metodo", text="Algoritmo")
        self.tree.heading("Tiempo", text="Tiempo (s)")
        self.tree.pack(pady=10, fill="x", padx=20)

    def log(self, mensaje):
        self.txt_proceso.config(state="normal")
        self.txt_proceso.insert(tk.END, mensaje + "\n")
        self.txt_proceso.see(tk.END)
        self.txt_proceso.config(state="disabled")

    def limpiar_consola_visual(self):
        self.txt_proceso.config(state="normal")
        self.txt_proceso.delete(1.0, tk.END)
        self.txt_proceso.config(state="disabled")
        self.datos_preparados = []

    def limpiar_y_validar(self, lista_cruda):
        numeros, basura = [], []
        for item in lista_cruda:
            try:
                numeros.append(int(item))
            except:
                if str(item).strip(): basura.append(str(item))
        if basura:
            messagebox.showwarning("Filtro de Datos", f"Se descartaron elementos no numéricos:\n{', '.join(basura)}")
        return numeros

    def cargar_archivos_multiples(self):
        # Permite elegir varios archivos a la vez manteniendo presionada la tecla Ctrl
        rutas = filedialog.askopenfilenames(filetypes=[("Archivos de Datos", "*.txt *.xlsx")])
        if not rutas: return
        
        datos_acumulados = []
        try:
            for ruta in rutas:
                if ruta.endswith('.txt'):
                    with open(ruta, 'r') as f:
                        datos_acumulados.extend(f.read().split())
                elif ruta.endswith('.xlsx'):
                    if pd is None: raise ImportError("Se requiere pandas para archivos Excel.")
                    df = pd.read_excel(ruta, header=None)
                    datos_acumulados.extend(df.values.flatten().tolist())
            
            self.datos_preparados = self.limpiar_y_validar(datos_acumulados)
            self.log(f"--- Fusión exitosa: {len(rutas)} archivos cargados ---")
            self.log(f"Total de elementos a ordenar: {len(self.datos_preparados)}")
        except Exception as e:
            messagebox.showerror("Error de Carga", str(e))

    def iniciar_hilo(self):
        if not self.datos_preparados:
            self.datos_preparados = self.limpiar_y_validar(self.entrada_manual.get().replace(',', ' ').split())
        if not self.datos_preparados:
            return messagebox.showerror("Error", "No hay datos para procesar.")
        threading.Thread(target=self.ejecutar_ordenamiento, daemon=True).start()

    def ejecutar_ordenamiento(self):
        metodo = self.metodo_var.get()
        datos = self.datos_preparados[:]
        self.log(f"\n>>> PROCESANDO FUSIÓN CON {metodo.upper()}...")
        
        inicio = time.perf_counter()
        # Lógica de los algoritmos (Burbuja, QuickSort, etc... igual que antes)
        if metodo == "Burbuja":
            for i in range(len(datos)):
                for j in range(0, len(datos)-i-1):
                    if datos[j] > datos[j+1]:
                        datos[j], datos[j+1] = datos[j+1], datos[j]
                        self.log(str(datos))
                        time.sleep(0.01) # Más rápido para fusiones grandes
        elif metodo == "QuickSort":
            datos = OrdenacionInterna.quicksort(datos)
        else:
            # Llamada genérica para el resto de métodos
            func = getattr(OrdenacionInterna, metodo.lower().replace("sort", "_sort"), None)
            if not func: func = getattr(OrdenacionInterna, metodo.lower().replace(" ", "_"), None)
            datos = func(datos) if func else datos

        fin = time.perf_counter()
        self.log(f"¡Ordenamiento completado en {fin-inicio:.4f}s!")
        self.actualizar_tabla(metodo, fin - inicio)
        
        # PREGUNTA SI QUIERE GUARDAR
        self.root.after(0, lambda: self.preguntar_guardado(datos))

    def preguntar_guardado(self, datos_finales):
        if messagebox.askyesno("Guardar Resultado", "¿Desea guardar la lista ordenada en un archivo?"):
            ruta = filedialog.asksaveasfilename(
                title="Guardar como...",
                filetypes=[("Excel", "*.xlsx"), ("Archivo de Texto", "*.txt")],
                defaultextension=".xlsx"
            )
            if not ruta: return
            
            try:
                if ruta.endswith('.xlsx'):
                    df = pd.DataFrame(datos_finales)
                    df.to_excel(ruta, index=False, header=False)
                else:
                    with open(ruta, 'w') as f:
                        f.write("\n".join(map(str, datos_finales)))
                messagebox.showinfo("Éxito", f"Archivo guardado en:\n{ruta}")
            except Exception as e:
                messagebox.showerror("Error al guardar", str(e))
        
        self.datos_preparados = []

    def actualizar_tabla(self, m, t):
        self.historial_tiempos[m] = f"{t:.6f}"
        for i in self.tree.get_children(): self.tree.delete(i)
        for m, t in self.historial_tiempos.items():
            self.tree.insert("", tk.END, values=(m, t))

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionOrdenacion(root)
    root.mainloop()