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


# ── Programa principal ─────────────────────────────────────
if __name__ == "__main__":
    cola = Cola()

    cola.encolar(Pedido(20, "cliente1"))
    cola.encolar(Pedido(30, "cliente2"))
    cola.encolar(Pedido(40, "cliente3"))
    cola.encolar(Pedido(50, "cliente3"))

    cola.volcar()