class OrdenacionInterna:
    @staticmethod
    def burbuja(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    @staticmethod
    def insercion(arr):
        for i in range(1, len(arr)):
            llave = arr[i]
            j = i - 1
            while j >= 0 and llave < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = llave
        return arr

    @staticmethod
    def seleccion(arr):
        for i in range(len(arr)):
            idx_min = i
            for j in range(i + 1, len(arr)):
                if arr[j] < arr[idx_min]:
                    idx_min = j
            arr[i], arr[idx_min] = arr[idx_min], arr[i]
        return arr

    @staticmethod
    def shell_sort(arr):
        n = len(arr)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and arr[j - gap] > temp:
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 2
        return arr

    @staticmethod
    def quicksort(arr):
        if len(arr) <= 1:
            return arr
        pivote = arr[len(arr) // 2]
        izq = [x for x in arr if x < pivote]
        centro = [x for x in arr if x == pivote]
        der = [x for x in arr if x > pivote]
        return OrdenacionInterna.quicksort(izq) + centro + OrdenacionInterna.quicksort(der)

    @staticmethod
    def heapsort(arr):
        import heapq
        heapq.heapify(arr)
        return [heapq.heappop(arr) for _ in range(len(arr))]

    @staticmethod
    def radix_sort(arr):
        max_val = max(arr)
        exp = 1
        while max_val // exp > 0:
            buckets = [[] for _ in range(10)]
            for val in arr:
                buckets[(val // exp) % 10].append(val)
            arr = [val for b in buckets for val in b]
            exp *= 10
        return arr