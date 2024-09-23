import heapq

def solve():
    try:
        # n: cantidad de llegadas.
        # m: tiempo final.
        # c: capacidad total.
        # c0: capacidad utilizada hasta el momento.
        n, m, c, c0 = map(int, input().split()[:4])

        # Arreglo de datos <tiempo de llegada, cantidad de unidades, costo por unidad>.
        data = [[0, 0, 0] for _ in range(n + 2)]

        # Leer los datos de entrada.
        for i in range(1, n + 1):
            data[i] = list(map(int, input().split()[:3]))

        # Agregar datos ficticios al inicio y al final para simplificar el código.
        data[0][1] = c0
        data[n + 1][0] = m
        n += 2  # Aumentar el número de entradas por dos.

        data.sort(lambda trio: trio[0])  # Ordenar por tiempo de llegada.

        # Distribución de unidades disponibles para compra <costo por unidad, unidades disponibles>.
        dist = {0: c0}
        max_heap = [0]  # Heap para precios máximos.
        min_heap = [0]  # Heap para precios mínimos.

        ans = 0  # Costo total.

        # Procesar cada llegada.
        for i in range(1, n):
            tiempo = data[i][0]
            cantidad = data[i][1]
            costo = data[i][2]

            # Diferencia de tiempo hasta la próxima llegada.
            dif = tiempo - data[i - 1][0]

            # Mientras haya unidades disponibles y no hayamos llegado al tiempo actual.
            while dist and dif > 0:
                # Eliminar precios obsoletos del heap mínimo.
                while min_heap and dist.get(min_heap[0], 0) == 0:
                    heapq.heappop(min_heap)

                # Costo de la unidad más barata.
                min_costo = min_heap[0]

                # Cantidad a comprar de la unidad más barata.
                comprar = min(dist[min_costo], dif)

                ans += min_costo * comprar  # Sumar el costo al total.
                c0 -= comprar  # Actualizar capacidad utilizada.
                dif -= comprar  # Reducir la diferencia de tiempo.
                dist[min_costo] -= comprar  # Actualizar unidades disponibles.

                # Si se agota la unidad, eliminarla de la distribución.
                if dist[min_costo] == 0:
                    heapq.heappop(min_heap)
                    del dist[min_costo]
            
            # Si no hay suficientes unidades para alcanzar el tiempo actual, el problema no tiene solución.
            if dif > 0:
                return -1

            # Agregar la cantidad máxima de la unidad recién llegada, hasta llenar la capacidad.
            agregar = min(c - c0, cantidad)
            c0 += agregar

            # Mientras queden unidades de este tipo.
            while agregar < cantidad and len(dist) > 0:
                # Eliminar precios obsoletos del heap máximo.
                while len(max_heap) > 0 and dist.get(-max_heap[0], 0) == 0:
                    heapq.heappop(max_heap)

                # Si hay unidades más caras, reemplazarlas por la nueva unidad.
                if -max_heap[0] > costo:
                    max_costo = -max_heap[0]
                    sustitucion = min(dist[max_costo], cantidad - agregar)

                    agregar += sustitucion  # Actualizar unidades totales.
                    dist[max_costo] -= sustitucion  # Actualizar unidades disponibles.

                    # Eliminar si se agota la unidad más cara.
                    if dist[max_costo] == 0:
                        heapq.heappop(max_heap)
                        del dist[max_costo]
                else:
                    break
            
            # Actualizar la distribución de unidades disponibles con las unidades tomadas.
            if agregar > 0:
                # Actualizar la distribución de unidades disponibles.
                if costo in dist:
                    dist[costo] += agregar
                else:
                    dist[costo] = agregar
                    # Add the new price to the heaps.
                    heapq.heappush(min_heap, costo)
                    heapq.heappush(max_heap, -costo)
                

        # Retornar el costo total.
        return ans

    except Exception as e:
        print(f"Error al actualizar la distribución: {e}")
        return -1  # O manejar el error de otra manera según tu lógica.

# Leer la cantidad de consultas.
q = int(input())

# Para cada consulta, imprimir la solución del problema.
for _ in range(q):
    print(solve())