import tkinter as tk
from tkinter import messagebox, simpledialog
import math
import random

class NodoGrafo:
    def __init__(self, nombre, x, y):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.adyacentes = []  # Lista de (nodo, objeto, es_dirigida)

class AristaInfo:
    def __init__(self, origen, destino, objeto, dirigida):
        self.origen = origen
        self.destino = destino
        self.objeto = objeto
        self.dirigida = dirigida

class GrafoVisual:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Grafos - TDA Grafo")
        self.root.geometry("1000x700")
        
        self.nodos = {}  # nombre -> NodoGrafo
        self.dirigido = False
        
        self.setup_ui()
        self.dibujar_grafo()
    
    def setup_ui(self):
        # Frame superior
        frame_superior = tk.Frame(self.root)
        frame_superior.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Controles de tipo de grafo
        frame_tipo = tk.LabelFrame(frame_superior, text="Tipo de Grafo")
        frame_tipo.pack(side=tk.LEFT, padx=5)
        
        self.tipo_var = tk.StringVar(value="no_dirigido")
        rb_no_dir = tk.Radiobutton(frame_tipo, text="No Dirigido", variable=self.tipo_var, 
                                   value="no_dirigido", command=self.cambiar_tipo)
        rb_dir = tk.Radiobutton(frame_tipo, text="Dirigido", variable=self.tipo_var,
                               value="dirigido", command=self.cambiar_tipo)
        rb_no_dir.pack(side=tk.LEFT, padx=5)
        rb_dir.pack(side=tk.LEFT, padx=5)
        
        # Botones de operaciones
        frame_botones = tk.LabelFrame(frame_superior, text="Operaciones")
        frame_botones.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        btn_vertice = tk.Button(frame_botones, text="Insertar Vértice", command=self.insertar_vertice, width=15)
        btn_vertice.pack(side=tk.LEFT, padx=2)
        
        btn_arista = tk.Button(frame_botones, text="Insertar Arista", command=self.insertar_arista, width=15)
        btn_arista.pack(side=tk.LEFT, padx=2)
        
        btn_eliminar_v = tk.Button(frame_botones, text="Eliminar Vértice", command=self.eliminar_vertice, width=15)
        btn_eliminar_v.pack(side=tk.LEFT, padx=2)
        
        btn_eliminar_a = tk.Button(frame_botones, text="Eliminar Arista", command=self.eliminar_arista, width=15)
        btn_eliminar_a.pack(side=tk.LEFT, padx=2)
        
        # Botones de información
        frame_info = tk.LabelFrame(frame_superior, text="Información")
        frame_info.pack(side=tk.LEFT, padx=5)
        
        btn_info = tk.Button(frame_info, text="Info Grafo", command=self.mostrar_info, width=12)
        btn_info.pack(side=tk.LEFT, padx=2)
        
        btn_grado = tk.Button(frame_info, text="Grado Vértice", command=self.mostrar_grado, width=12)
        btn_grado.pack(side=tk.LEFT, padx=2)
        
        btn_ady = tk.Button(frame_info, text="Adyacentes", command=self.mostrar_adyacentes, width=12)
        btn_ady.pack(side=tk.LEFT, padx=2)
        
        # Canvas para dibujar
        frame_canvas = tk.Frame(self.root)
        frame_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(frame_canvas, bg='white', cursor='cross')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Barra de estado
        self.status_bar = tk.Label(self.root, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def cambiar_tipo(self):
        nuevo_tipo = self.tipo_var.get()
        if nuevo_tipo == "dirigido" and not self.dirigido:
            self.dirigido = True
            self.status_bar.config(text="Modo: Grafo Dirigido")
            self.dibujar_grafo()
        elif nuevo_tipo == "no_dirigido" and self.dirigido:
            self.dirigido = False
            self.status_bar.config(text="Modo: Grafo No Dirigido")
            self.dibujar_grafo()
    
    def insertar_vertice(self):
        nombre = simpledialog.askstring("Insertar Vértice", "Nombre del vértice:")
        if not nombre:
            return
        
        if nombre in self.nodos:
            messagebox.showwarning("Advertencia", f"El vértice '{nombre}' ya existe")
            return
        
        # Posición aleatoria dentro del canvas
        x = random.randint(50, self.canvas.winfo_width() - 50) if self.canvas.winfo_width() > 100 else 200
        y = random.randint(50, self.canvas.winfo_height() - 50) if self.canvas.winfo_height() > 100 else 200
        
        nuevo_nodo = NodoGrafo(nombre, x, y)
        self.nodos[nombre] = nuevo_nodo
        
        self.dibujar_grafo()
        messagebox.showinfo("Éxito", f"Vértice '{nombre}' insertado")
    
    def insertar_arista(self):
        if len(self.nodos) < 2:
            messagebox.showwarning("Advertencia", "Se necesitan al menos 2 vértices")
            return
        
        vertices = list(self.nodos.keys())
        
        origen = simpledialog.askstring("Insertar Arista", f"Vértice origen\nVértices disponibles: {vertices}")
        if not origen or origen not in self.nodos:
            messagebox.showerror("Error", "Vértice origen no válido")
            return
        
        destino = simpledialog.askstring("Insertar Arista", f"Vértice destino\nVértices disponibles: {vertices}")
        if not destino or destino not in self.nodos:
            messagebox.showerror("Error", "Vértice destino no válido")
            return
        
        objeto = simpledialog.askstring("Insertar Arista", "Etiqueta/valor de la arista (opcional):")
        if not objeto:
            objeto = ""
        
        # Verificar si ya existe la arista
        nodo_origen = self.nodos[origen]
        for (dest, obj, dir) in nodo_origen.adyacentes:
            if dest == destino:
                messagebox.showwarning("Advertencia", "La arista ya existe")
                return
        
        # Insertar arista
        nodo_origen.adyacentes.append((destino, objeto, self.dirigido))
        
        if not self.dirigido:
            # En grafo no dirigido, agregar en ambos sentidos
            nodo_destino = self.nodos[destino]
            nodo_destino.adyacentes.append((origen, objeto, False))
        
        self.dibujar_grafo()
        tipo = "dirigida" if self.dirigido else "no dirigida"
        messagebox.showinfo("Éxito", f"Arista {tipo} insertada: {origen} → {destino}")
    
    def eliminar_vertice(self):
        if not self.nodos:
            messagebox.showinfo("Info", "No hay vértices para eliminar")
            return
        
        vertices = list(self.nodos.keys())
        nombre = simpledialog.askstring("Eliminar Vértice", f"Vértice a eliminar:\n{vertices}")
        
        if not nombre or nombre not in self.nodos:
            messagebox.showerror("Error", "Vértice no encontrado")
            return
        
        # Eliminar todas las aristas que involucran este vértice
        for nodo in self.nodos.values():
            nodo.adyacentes = [(d, o, dir) for (d, o, dir) in nodo.adyacentes if d != nombre]
        
        # Eliminar el vértice
        del self.nodos[nombre]
        
        self.dibujar_grafo()
        messagebox.showinfo("Éxito", f"Vértice '{nombre}' eliminado")
    
    def eliminar_arista(self):
        if len(self.nodos) < 2:
            messagebox.showinfo("Info", "No hay suficientes vértices")
            return
        
        # Listar todas las aristas
        aristas = []
        for origen, nodo in self.nodos.items():
            for (destino, objeto, dirigida) in nodo.adyacentes:
                if self.dirigido or origen < destino:  # Evitar duplicados en no dirigido
                    aristas.append((origen, destino))
        
        if not aristas:
            messagebox.showinfo("Info", "No hay aristas para eliminar")
            return
        
        aristas_str = [f"{o} → {d}" for o, d in aristas]
        
        arista_str = simpledialog.askstring("Eliminar Arista", 
                                            f"Aristas existentes:\n{', '.join(aristas_str)}\n\nIngrese: origen destino")
        
        if arista_str:
            partes = arista_str.split()
            if len(partes) == 2:
                origen, destino = partes[0], partes[1]
                
                if origen in self.nodos and destino in self.nodos:
                    # Eliminar arista
                    nodo_origen = self.nodos[origen]
                    nodo_origen.adyacentes = [(d, o, dir) for (d, o, dir) in nodo_origen.adyacentes if d != destino]
                    
                    if not self.dirigido:
                        nodo_destino = self.nodos[destino]
                        nodo_destino.adyacentes = [(d, o, dir) for (d, o, dir) in nodo_destino.adyacentes if d != origen]
                    
                    self.dibujar_grafo()
                    messagebox.showinfo("Éxito", "Arista eliminada")
                else:
                    messagebox.showerror("Error", "Vértice no encontrado")
            else:
                messagebox.showerror("Error", "Formato inválido. Use: origen destino")
    
    def mostrar_info(self):
        info = "=== INFORMACIÓN DEL GRAFO ===\n\n"
        info += f"Tipo: {'Dirigido' if self.dirigido else 'No Dirigido'}\n"
        info += f"Número de vértices: {len(self.nodos)}\n"
        
        # Contar aristas
        aristas_count = 0
        for nodo in self.nodos.values():
            aristas_count += len(nodo.adyacentes)
        
        if not self.dirigido:
            aristas_count //= 2
        
        info += f"Número de aristas: {aristas_count}\n\n"
        info += "Vértices:\n"
        for nombre in self.nodos.keys():
            info += f"  • {nombre}\n"
        
        info += "\nAristas:\n"
        aristas_mostradas = set()
        for origen, nodo in self.nodos.items():
            for (destino, objeto, dirigida) in nodo.adyacentes:
                key = (origen, destino) if self.dirigido else tuple(sorted([origen, destino]))
                if key not in aristas_mostradas:
                    aristas_mostradas.add(key)
                    flecha = " → " if dirigida else " — "
                    etiqueta = f" [{objeto}]" if objeto else ""
                    info += f"  • {origen}{flecha}{destino}{etiqueta}\n"
        
        messagebox.showinfo("Información del Grafo", info)
    
    def mostrar_grado(self):
        if not self.nodos:
            messagebox.showinfo("Info", "No hay vértices")
            return
        
        vertices = list(self.nodos.keys())
        nombre = simpledialog.askstring("Grado del Vértice", f"Vértice:\n{vertices}")
        
        if not nombre or nombre not in self.nodos:
            messagebox.showerror("Error", "Vértice no encontrado")
            return
        
        if self.dirigido:
            # Grado de entrada y salida
            grado_salida = len(self.nodos[nombre].adyacentes)
            grado_entrada = 0
            
            for nodo in self.nodos.values():
                for (destino, _, _) in nodo.adyacentes:
                    if destino == nombre:
                        grado_entrada += 1
            
            info = f"Vértice: {nombre}\n\n"
            info += f"Grado de entrada: {grado_entrada}\n"
            info += f"Grado de salida: {grado_salida}\n"
            info += f"Grado total: {grado_entrada + grado_salida}"
        else:
            grado = len(self.nodos[nombre].adyacentes)
            info = f"Vértice: {nombre}\n\nGrado: {grado}"
        
        messagebox.showinfo("Grado del Vértice", info)
    
    def mostrar_adyacentes(self):
        if not self.nodos:
            messagebox.showinfo("Info", "No hay vértices")
            return
        
        vertices = list(self.nodos.keys())
        nombre = simpledialog.askstring("Vértices Adyacentes", f"Vértice:\n{vertices}")
        
        if not nombre or nombre not in self.nodos:
            messagebox.showerror("Error", "Vértice no encontrado")
            return
        
        if self.dirigido:
            salida = [d for (d, _, _) in self.nodos[nombre].adyacentes]
            entrada = []
            for nodo in self.nodos.values():
                for (destino, _, _) in nodo.adyacentes:
                    if destino == nombre:
                        entrada.append(nodo.nombre)
            
            info = f"Vértice: {nombre}\n\n"
            info += f"Adyacentes de salida: {salida if salida else 'Ninguno'}\n"
            info += f"Adyacentes de entrada: {entrada if entrada else 'Ninguno'}"
        else:
            adyacentes = [d for (d, _, _) in self.nodos[nombre].adyacentes]
            info = f"Vértice: {nombre}\n\nAdyacentes: {adyacentes if adyacentes else 'Ninguno'}"
        
        messagebox.showinfo("Vértices Adyacentes", info)
    
    def dibujar_grafo(self):
        """Dibuja el grafo en el canvas"""
        self.canvas.delete("all")
        
        if not self.nodos:
            self.canvas.create_text(400, 300, text="Grafo vacío\nAgregue vértices usando el botón 'Insertar Vértice'",
                                   font=("Arial", 14), fill="gray")
            return
        
        # Obtener dimensiones del canvas
        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()
        
        if ancho <= 1:
            ancho = 800
            alto = 500
        
        # Reorganizar nodos si es necesario
        self.reorganizar_nodos(ancho, alto)
        
        # Dibujar aristas primero
        aristas_dibujadas = set()
        for origen, nodo in self.nodos.items():
            x1, y1 = nodo.x, nodo.y
            for (destino, objeto, dirigida) in nodo.adyacentes:
                # Evitar dibujar dos veces la misma arista en no dirigido
                key = tuple(sorted([origen, destino])) if not dirigida else (origen, destino)
                if key in aristas_dibujadas:
                    continue
                aristas_dibujadas.add(key)
                
                if destino in self.nodos:
                    nodo_dest = self.nodos[destino]
                    x2, y2 = nodo_dest.x, nodo_dest.y
                    
                    # Dibujar arista
                    if dirigida:
                        # Dibujar flecha
                        self.dibujar_flecha(x1, y1, x2, y2, objeto)
                    else:
                        self.canvas.create_line(x1, y1, x2, y2, width=2, fill="black")
                        
                        # Dibujar etiqueta de la arista
                        if objeto:
                            mx = (x1 + x2) / 2
                            my = (y1 + y2) / 2
                            self.canvas.create_text(mx, my - 10, text=objeto, font=("Arial", 9), fill="blue")
        
        # Dibujar vértices
        for nombre, nodo in self.nodos.items():
            # Círculo del vértice
            self.canvas.create_oval(nodo.x - 25, nodo.y - 25, nodo.x + 25, nodo.y + 25,
                                    fill="lightblue", outline="darkblue", width=2)
            # Nombre del vértice
            self.canvas.create_text(nodo.x, nodo.y, text=nombre, font=("Arial", 12, "bold"))
    
    def dibujar_flecha(self, x1, y1, x2, y2, etiqueta):
        """Dibuja una línea con flecha dirigida"""
        # Calcular ángulo
        angulo = math.atan2(y2 - y1, x2 - x1)
        
        # Punto de inicio y fin (acortar para no chocar con el círculo)
        radio_nodo = 25
        x1_ajust = x1 + radio_nodo * math.cos(angulo)
        y1_ajust = y1 + radio_nodo * math.sin(angulo)
        x2_ajust = x2 - radio_nodo * math.cos(angulo)
        y2_ajust = y2 - radio_nodo * math.sin(angulo)
        
        # Dibujar línea
        self.canvas.create_line(x1_ajust, y1_ajust, x2_ajust, y2_ajust, width=2, fill="black", arrow=tk.LAST)
        
        # Dibujar etiqueta
        if etiqueta:
            mx = (x1_ajust + x2_ajust) / 2
            my = (y1_ajust + y2_ajust) / 2
            self.canvas.create_text(mx, my - 10, text=etiqueta, font=("Arial", 9), fill="blue")
    
    def reorganizar_nodos(self, ancho, alto):
        """Reorganiza los nodos en el canvas"""
        if not self.nodos:
            return
        
        # Si hay pocos nodos, distribuirlos en círculo
        n = len(self.nodos)
        radio = min(ancho, alto) * 0.35
        
        centro_x = ancho / 2
        centro_y = alto / 2
        
        for i, (nombre, nodo) in enumerate(self.nodos.items()):
            # Si el nodo está fuera del canvas o en la esquina, reubicarlo
            if (nodo.x < 50 or nodo.x > ancho - 50 or 
                nodo.y < 50 or nodo.y > alto - 50):
                angulo = 2 * math.pi * i / n
                nodo.x = centro_x + radio * math.cos(angulo)
                nodo.y = centro_y + radio * math.sin(angulo)

def main():
    root = tk.Tk()
    app = GrafoVisual(root)
    
    # Actualizar el canvas después de que se muestre
    def on_resize(event):
        app.dibujar_grafo()
    
    root.bind("<Configure>", on_resize)
    root.mainloop()

if __name__ == "__main__":
    main()