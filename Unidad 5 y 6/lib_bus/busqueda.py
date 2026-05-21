class Busqueda:
    @staticmethod
    def secuencial(lista, elemento_buscado):
        for indice in range(len(lista)):
            if lista[indice] == elemento_buscado:
                return indice
        return -1

    @staticmethod
    def binaria(lista_ordenada, elemento_buscado):
        izquierda = 0
        derecha = len(lista_ordenada) - 1

        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            if lista_ordenada[medio] == elemento_buscado:
                return medio
            elif lista_ordenada[medio] > elemento_buscado:
                derecha = medio - 1
            else:
                izquierda = medio + 1
        return -1


class TablaHash:
    def __init__(self, tamaño_tabla=10):
        self.tamaño = tamaño_tabla
        self.tabla = [[] for _ in range(self.tamaño)]

    def _funcion_hash(self, clave):
        return abs(hash(clave)) % self.tamaño

    def insertar(self, clave, valor):
        indice = self._funcion_hash(clave)
        for par in self.tabla[indice]:
            if par[0] == clave:
                par[1] = valor
                return
        self.tabla[indice].append([clave, valor])

    def buscar(self, clave):
        indice = self._funcion_hash(clave)
        for par in self.tabla[indice]:
            if par[0] == clave:
                return par[1]
        return None