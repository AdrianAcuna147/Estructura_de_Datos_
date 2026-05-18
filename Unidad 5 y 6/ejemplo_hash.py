import tkinter as tk
from tkinter import messagebox, ttk
import random

# IMPORTACIÓN DIRECTA DE TU LIBRERÍA
# Esto buscará el archivo 'tablahash.py' en la misma carpeta e importará tu clase TablaHash
from libreria_bus.tablahash import TablaHash

class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario Avanzado - Usando tu Librería")
        self.root.geometry("800x650")
        self.root.configure(bg="#f5f5f5")

        # Inicializamos tu estructura con capacidad 11 para provocar y ver colisiones de forma didáctica
        self.inventario = TablaHash(capacidad=11)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Arial", 9, "bold"), padding=5)
        self.style.configure("TLabel", font=("Arial", 10), background="#f5f5f5")

        self.crear_componentes()
        self.actualizar_vista_hash()

    def crear_componentes(self):
        # --- TÍTULO ---
        titulo = tk.Label(self.root, text="📦 Gestión de Inventario (Importando tu Librería)", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#333")
        titulo.pack(pady=10)

        # --- CONTENEDOR PRINCIPAL IZQUIERDA/DERECHA ---
        frame_superior = tk.Frame(self.root, bg="#f5f5f5")
        frame_superior.pack(fill="x", padx=20, pady=5)

        # --- FORMULARIO (Izquierda) ---
        frame_form = tk.LabelFrame(frame_superior, text=" Control de Productos ", font=("Arial", 10, "bold"), bg="#f5f5f5", padx=10, pady=10)
        frame_form.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ttk.Label(frame_form, text="Código (Clave):").grid(row=0, column=0, sticky="w", pady=5)
        self.txt_codigo = ttk.Entry(frame_form, width=15)
        self.txt_codigo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_form, text="Producto (Valor):").grid(row=1, column=0, sticky="w", pady=5)
        self.txt_nombre = ttk.Entry(frame_form, width=20)
        self.txt_nombre.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Botones de Acción
        frame_botones = tk.Frame(frame_form, bg="#f5f5f5")
        frame_botones.grid(row=2, column=0, columnspan=2, pady=10, sticky="w")

        ttk.Button(frame_botones, text="Guardar", width=10, command=self.guardar_producto).pack(side="left", padx=2)
        ttk.Button(frame_botones, text="Buscar", width=10, command=self.buscar_producto).pack(side="left", padx=2)
        ttk.Button(frame_botones, text="Eliminar", width=10, command=self.eliminar_producto).pack(side="left", padx=2)
        
        # Botón Aleatorio
        ttk.Button(frame_form, text="🎲 Llenar Aleatorio", command=self.generar_aleatorios).grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

        # --- PANEL DE RASTREO / TRACE DE BÚSQUEDA (Derecha) ---
        frame_rastreo = tk.LabelFrame(frame_superior, text=" 🔍 Pasos de la Última Búsqueda ", font=("Arial", 10, "bold"), bg="#f5f5f5", padx=10, pady=10)
        frame_rastreo.pack(side="right", fill="both", expand=True)

        self.txt_rastreo = tk.Text(frame_rastreo, font=("Courier New", 10), bg="#eef2f3", fg="#2c3e50", height=7, width=40)
        self.txt_rastreo.pack(fill="both", expand=True)
        self.txt_rastreo.insert(tk.END, "Esperando búsqueda...")
        self.txt_rastreo.configure(state="disabled")

        # --- MONITOR GENERAL DE LA ESTRUCTURA (Abajo) ---
        frame_hash = tk.LabelFrame(self.root, text=" Estructura Interna de la Tabla Hash (Memoria Real) ", font=("Arial", 10, "bold"), bg="#f5f5f5", padx=10, pady=10)
        frame_hash.pack(fill="both", expand=True, padx=20, pady=10)

        self.txt_monitor = tk.Text(frame_hash, font=("Courier New", 11), bg="#2c3e50", fg="#ecf0f1", wrap="none")
        scrollbar = ttk.Scrollbar(frame_hash, orient="vertical", command=self.txt_monitor.yview)
        self.txt_monitor.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.txt_monitor.pack(side="left", fill="both", expand=True)

    # --- LÓGICA CONECTADA A TU LIBRERÍA ---

    def guardar_producto(self):
        codigo = self.txt_codigo.get().strip()
        nombre = self.txt_nombre.get().strip()

        if not codigo or not nombre:
            messagebox.showwarning("Campos vacíos", "Por favor, llena ambos campos.")
            return

        # LLAMADA A TU MÉTODO INSERTAR
        self.inventario.insertar(codigo, nombre)
        self.limpiar_entradas()
        self.actualizar_vista_hash()

    def buscar_producto(self):
        codigo = self.txt_codigo.get().strip()

        if not codigo:
            messagebox.showwarning("Código requerido", "Ingresa un código para buscar.")
            return

        # RASTREO EXPLICATIVO EN BASE A TU LÓGICA INTERNA
        # Usamos tu función hash por módulo para el log visual
        indice = self.inventario._funcion_hash_modulo(codigo)
        
        log_pasos = f"1. Clave buscada: '{codigo}'\n"
        log_pasos += f"2. Índice por módulo calculado: {indice}\n"
        log_pasos += f"3. Buscando en la lista enlazada:\n"

        # Accedemos a tu arreglo para mostrar cómo itera el bucle while
        actual = self.inventario.tabla[indice]
        paso = 1
        encontrado = False

        # LLAMADA A TU MÉTODO BUSCAR para obtener el valor real
        resultado_valor = self.inventario.buscar(codigo)

        # Lógica de impresión para el monitor de pasos
        while actual:
            log_pasos += f"   └─ [Nodo {paso}]: ¿'{actual.clave}' == '{codigo}'? "
            if actual.clave == codigo:
                log_pasos += "¡SÍ!\n"
                encontrado = True
                break
            else:
                log_pasos += "No. Siguiente...\n"
            
            paso += 1
            actual = actual.siguiente

        if not encontrado:
            log_pasos += "   └─ Llegó al final (None). Clave no existe."

        self.txt_rastreo.configure(state="normal")
        self.txt_rastreo.delete("1.0", tk.END)
        self.txt_rastreo.insert(tk.END, log_pasos)
        self.txt_rastreo.configure(state="disabled")

        if resultado_valor is not None:
            self.txt_nombre.delete(0, tk.END)
            self.txt_nombre.insert(0, resultado_valor)
        else:
            messagebox.showerror("No encontrado", "El código no existe en el inventario.")

    def eliminar_producto(self):
        codigo = self.txt_codigo.get().strip()

        if not codigo:
            messagebox.showwarning("Código requerido", "Ingresa un código para eliminar.")
            return

        # LLAMADA A TU MÉTODO ELIMINAR
        exito = self.inventario.eliminar(codigo)

        if exito:
            self.limpiar_entradas()
            self.actualizar_vista_hash()
        else:
            messagebox.showerror("Error", "No se pudo eliminar. El código no existe.")

    def generar_aleatorios(self):
        """ Inserta datos usando tu método 'insertar' """
        productos_ficticios = [
            ("A10", "Refresco 2L"), ("B25", "Papas Fritas"), ("C04", "Leche Entera"),
            ("A11", "Jabón Líquido"), ("X99", "Cereal Caja"), ("H45", "Chocolate"),
            ("K02", "Pan Molido"), ("M12", "Atún en Lata"), ("Z03", "Café Soluble")
        ]
        
        seleccionados = random.sample(productos_ficticios, 5)
        
        for codigo, nombre in seleccionados:
            codigo_final = f"{codigo}{random.randint(1,9)}"
            # Usando tu método de inserción
            self.inventario.insertar(codigo_final, nombre)
            
        self.actualizar_vista_hash()

    def actualizar_vista_hash(self):
        """ Dibuja la tabla recorriendo tu arreglo self.tabla y tus Nodos """
        self.txt_monitor.configure(state="normal")
        self.txt_monitor.delete("1.0", tk.END)

        # Acceso directo a los atributos de tu objeto TablaHash
        for i in range(self.inventario.capacidad):
            elementos = []
            actual = self.inventario.tabla[i]
            while actual:
                elementos.append(f"[{actual.clave}: {actual.valor}]")
                actual = actual.siguiente
            
            if elementos:
                linea = f"Índice {i:02d} ➔ " + " ➔ ".join(elementos) + " ➔ None\n"
            else:
                linea = f"Índice {i:02d} ➔ Empty\n"
                
            self.txt_monitor.insert(tk.END, linea)
        
        self.txt_monitor.configure(state="disabled")

    def limpiar_entradas(self):
        self.txt_codigo.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()