class OrdenacionExterna:
    @staticmethod
    def intercalacion(lista_a, lista_b):
        resultado = []
        i = j = 0
        while i < len(lista_a) and j < len(lista_b):
            if lista_a[i] < lista_b[j]:
                resultado.append(lista_a[i])
                i += 1
            else:
                resultado.append(lista_b[j])
                j += 1
        resultado.extend(lista_a[i:])
        resultado.extend(lista_b[j:])
        return resultado

    @staticmethod
    def mezcla_directa(arr):
        if len(arr) <= 1:
            return arr
        medio = len(arr) // 2
        izq = OrdenacionExterna.mezcla_directa(arr[:medio])
        der = OrdenacionExterna.mezcla_directa(arr[medio:])
        return OrdenacionExterna.intercalacion(izq, der)

    @staticmethod
    def mezcla_equilibrada(arr):
        # Enfoque de 'Natural Merge': identifica secuencias ya ordenadas (runs)
        if not arr: return []
        runs = []
        new_run = [arr[0]]
        
        for i in range(1, len(arr)):
            if arr[i] >= arr[i-1]:
                new_run.append(arr[i])
            else:
                runs.append(new_run)
                new_run = [arr[i]]
        runs.append(new_run)
        
        while len(runs) > 1:
            merged_runs = []
            for i in range(0, len(runs), 2):
                if i + 1 < len(runs):
                    merged_runs.append(OrdenacionExterna.intercalacion(runs[i], runs[i+1]))
                else:
                    merged_runs.append(runs[i])
            runs = merged_runs
        return runs[0]