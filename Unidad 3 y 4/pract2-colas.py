from abc import ABC, abstractmethod


# ── Interfaz Cola ──────────────────────────────────────────
class InterfazCola(ABC):

    @abstractmethod
    def tamanio(self) -> int:
        """Retorna el número de elementos en la Cola"""
        pass

    @abstractmethod
    def esta_vacia(self) -> bool:
        """Verifica si la Cola está vacía. True si vacía | False si no vacía."""
        pass

    @abstractmethod
    def frente(self):
        """Retorna el primer elemento. NO ES ELIMINADO. Retorna None si está vacía."""
        pass

    @abstractmethod
    def encolar(self, info):
        """Agrega un nuevo elemento a la Cola."""
        pass

    @abstractmethod
    def desencolar(self):
        """Retorna el primer elemento. ES ELIMINADO. Retorna None si está vacía."""
        pass


# ── Nodo ───────────────────────────────────────────────────
class Nodo:
    def __init__(self, info):
        self.info = info
        self.siguiente = None

    def get_siguiente(self):
        return self.siguiente

    def set_siguiente(self, siguiente):
        self.siguiente = siguiente


# ── Cola ───────────────────────────────────────────────────
class Cola(InterfazCola):
    def __init__(self):
        self.tope = None
        self._tamanio = 0

    def tamanio(self) -> int:
        return self._tamanio

    def esta_vacia(self) -> bool:
        return self._tamanio == 0

    def frente(self):
        if self.esta_vacia():
            return None
        return self.tope.info

    def encolar(self, info):
        nuevo_nodo = Nodo(info)
        if self.esta_vacia():
            self.tope = nuevo_nodo
        else:
            nodo = self.tope
            while nodo.get_siguiente() is not None:
                nodo = nodo.get_siguiente()
            nodo.set_siguiente(nuevo_nodo)
        self._tamanio += 1

    def desencolar(self):
        if self.esta_vacia():
            return None
        info = self.tope.info
        self.tope = self.tope.get_siguiente()
        self._tamanio -= 1
        return info

    def insertar_en_posicion(self, info, posicion):
        """Inserta un elemento en una posición específica (1 = primero)"""
        if posicion < 1 or posicion > self._tamanio + 1:
            print(f"   ✗ Posición inválida. Debe estar entre 1 y {self._tamanio + 1}")
            return
        nuevo_nodo = Nodo(info)
        if posicion == 1:
            nuevo_nodo.set_siguiente(self.tope)
            self.tope = nuevo_nodo
        else:
            nodo = self.tope
            for _ in range(posicion - 2):
                nodo = nodo.get_siguiente()
            nuevo_nodo.set_siguiente(nodo.get_siguiente())
            nodo.set_siguiente(nuevo_nodo)
        self._tamanio += 1
        print(f"   ✓ Pedido insertado en posición {posicion}")

    def eliminar_en_posicion(self, posicion):
        """Elimina un elemento en una posición específica (1 = primero)"""
        if self.esta_vacia():
            print("   ✗ La cola está vacía.")
            return None
        if posicion < 1 or posicion > self._tamanio:
            print(f"   ✗ Posición inválida. Debe estar entre 1 y {self._tamanio}")
            return None
        if posicion == 1:
            info = self.tope.info
            self.tope = self.tope.get_siguiente()
        else:
            nodo = self.tope
            for _ in range(posicion - 2):
                nodo = nodo.get_siguiente()
            info = nodo.get_siguiente().info
            nodo.set_siguiente(nodo.get_siguiente().get_siguiente())
        self._tamanio -= 1
        print(f"   ✓ Pedido eliminado de posición {posicion}")
        return info

    def eliminar_por_cliente(self, cliente):
        """Elimina el primer pedido que coincida con el nombre del cliente"""
        if self.esta_vacia():
            print("   ✗ La cola está vacía.")
            return None
        if self.tope.info.get_cliente() == cliente:
            info = self.tope.info
            self.tope = self.tope.get_siguiente()
            self._tamanio -= 1
            print(f"   ✓ Pedido de '{cliente}' eliminado.")
            return info
        nodo = self.tope
        while nodo.get_siguiente() is not None:
            if nodo.get_siguiente().info.get_cliente() == cliente:
                info = nodo.get_siguiente().info
                nodo.set_siguiente(nodo.get_siguiente().get_siguiente())
                self._tamanio -= 1
                print(f"   ✓ Pedido de '{cliente}' eliminado.")
                return info
            nodo = nodo.get_siguiente()
        print(f"   ✗ No se encontró ningún pedido de '{cliente}'.")
        return None

    def volcar(self):
        print("********* VOLCADO DE COLA *********")
        print(f"   Tamaño: {self.tamanio()}")
        nodo = self.tope
        contador = 1
        while nodo is not None:
            print(f"   ** Elemento {contador}")
            nodo.info.imprimir()
            nodo = nodo.get_siguiente()
            contador += 1
        print("***********************************")


# ── Pedido ─────────────────────────────────────────────────
class Pedido:
    def __init__(self, cantidad, cliente):
        self.cliente = cliente
        self.cantidad = cantidad

    def imprimir(self):
        print(f"     Cliente: {self.cliente}")
        print(f"     Cantidad: {self.cantidad}")
        print("     ------------")

    def get_cantidad(self):
        return self.cantidad

    def get_cliente(self):
        return self.cliente


# ── Menú interactivo ───────────────────────────────────────
def menu():
    cola = Cola()

    # Datos iniciales
    cola.encolar(Pedido(20, "cliente1"))
    cola.encolar(Pedido(30, "cliente2"))
    cola.encolar(Pedido(40, "cliente3"))
    cola.encolar(Pedido(50, "cliente4"))

    while True:
        print("\n========== MENÚ ==========")
        print("1. Ver cola")
        print("2. Insertar pedido al final")
        print("3. Insertar pedido en posición")
        print("4. Eliminar primer pedido")
        print("5. Eliminar pedido en posición")
        print("6. Eliminar pedido por cliente")
        print("7. Salir")
        print("==========================")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            cola.volcar()

        elif opcion == "2":
            cliente = input("   Nombre del cliente: ")
            cantidad = int(input("   Cantidad: "))
            cola.encolar(Pedido(cantidad, cliente))
            print("   ✓ Pedido agregado al final.")

        elif opcion == "3":
            cliente = input("   Nombre del cliente: ")
            cantidad = int(input("   Cantidad: "))
            posicion = int(input(f"   Posición (1 a {cola.tamanio() + 1}): "))
            cola.insertar_en_posicion(Pedido(cantidad, cliente), posicion)

        elif opcion == "4":
            pedido = cola.desencolar()
            if pedido:
                print("   ✓ Pedido eliminado:")
                pedido.imprimir()

        elif opcion == "5":
            posicion = int(input(f"   Posición a eliminar (1 a {cola.tamanio()}): "))
            pedido = cola.eliminar_en_posicion(posicion)
            if pedido:
                pedido.imprimir()

        elif opcion == "6":
            cliente = input("   Nombre del cliente a eliminar: ")
            cola.eliminar_por_cliente(cliente)

        elif opcion == "7":
            print("   Saliendo...")
            break

        else:
            print("   ✗ Opción inválida.")


if __name__ == "__main__":
    menu()