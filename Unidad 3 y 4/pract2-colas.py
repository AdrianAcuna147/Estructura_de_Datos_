from abc import ABC, abstractmethod


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
        """Retorna el primer elemento de la Cola. El elemento NO ES ELIMINADO. Retorna None si está vacía."""
        pass

    @abstractmethod
    def encolar(self, info):
        """Agrega un nuevo elemento a la Cola."""
        pass

    @abstractmethod
    def desencolar(self):
        """Retorna el primer elemento de la Cola. El elemento ES ELIMINADO. Retorna None si está vacía."""
        pass