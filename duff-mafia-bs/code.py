import sys
import traceback


def orden_topologico_util(grafo, v, visitado, pila):
    """
    Función utilizada para colocar en una pila el orden topológico invertido de una componente conexa
    """
    visitado[v] = True
    for i in grafo[v]:
        if not visitado[i]:
            orden_topologico_util(grafo, i, visitado, pila)
    pila.append(v)
 

def orden_topologico_inverso(grafo):
    """
    Dado un DAG devuelve el orden topológico invertido
    """
    visitado = [False] * len(grafo)
    pila = []
    
    for i in range(1, len(grafo)):
        if not visitado[i]:
            orden_topologico_util(grafo, i, visitado, pila)

    return pila[::]


class SAT:
    """
    Clase para encapsular las funciones necesarias para resolver un problema de 2-SAT 
    """

    def __init__(self, n):
        self.n = n  # cantidad de literales
        self.grafo = [[] for _ in range(2 * n + 1)]  # grafo asociado al SAT
        self.grafo_transpuesto = [[] for _ in range(2 * n + 1)]  # grafo transpuesto para componentes fuertemente conexas
        self.visitado = [False] * (2 * n + 1)  # nodos visitados en DFS
        self.pila = []  # pila para componentes fuertemente conexas
        self.cfc = [-1] * (2 * n + 1)  # componentes fuertemente conexas de cada nodo

    def agregar_clausula(self, a, no_a, b, no_b):
        """
        Función para agregar cláusulas al problema. `no_a` y `no_b` indican si a y b deben tomarse como sus negaciones.
        """
        if no_a:
            na = a
            a += self.n
        else:
            na = a + self.n
        if no_b:
            nb = b
            b += self.n
        else:
            nb = b + self.n

        # Agregamos las aristas al grafo y grafo transpuesto
        self.grafo[na].append(b)
        self.grafo[nb].append(a)
        self.grafo_transpuesto[b].append(na)
        self.grafo_transpuesto[a].append(nb)

    def dfs1(self, v):
        """
        DFS sobre el grafo como parte del proceso de búsqueda de componentes fuertemente conexas
        """
        self.visitado[v] = True
        for u in self.grafo[v]:
            if not self.visitado[u]:
                self.dfs1(u)
        self.pila.append(v)

    def dfs2(self, v, cfc):
        """
        DFS sobre el grafo transpuesto para asignar componentes fuertemente conexas a cada nodo
        """
        self.cfc[v] = cfc
        for u in self.grafo_transpuesto[v]:
            if self.cfc[u] == -1:
                self.dfs2(u, cfc)
        
    def resolver(self):
        """
        Resuelve el problema 2-SAT encontrando las componentes fuertemente conexas de cada nodo.
        """
        # Inicializar las estructuras
        self.visitado = [False] * (2 * self.n + 1)
        self.pila = []
        self.cfc = [-1] * (2 * self.n + 1)

        # Primer recorrido DFS en el grafo
        for i in range(1, len(self.grafo)):
            if not self.visitado[i]:
                self.dfs1(i)

        # Segundo recorrido DFS en el grafo transpuesto
        componente = 1
        while self.pila:
            v = self.pila.pop()
            if self.cfc[v] == -1:
                self.dfs2(v, componente)
                componente += 1
                

        # Creamos un diccionario donde para cada nodo tenemos su componente
        mapeo_nodo_componente = dict(enumerate(self.cfc))

        # Eliminamos la entrada 0 si está presente, ya que esta sobra
        mapeo_nodo_componente.pop(0, None)
        
        #creamos un mapeo inverso, donde para cada componente guardamos los nodos que estan contenidos en ella
        inverso = {i: [] for i in range(1, componente)}

        for key in mapeo_nodo_componente:
            inverso[mapeo_nodo_componente[key]].append(key)


        # Creamos el grafo de las componentes fuertemente conexas
        grafo_componentes = [set() for _ in range(componente)]
        
        for v in range(1, len(self.grafo)):
            for u in self.grafo[v]:
                if mapeo_nodo_componente[v] != mapeo_nodo_componente[u]:
                    grafo_componentes[mapeo_nodo_componente[v]].add(mapeo_nodo_componente[u])


        # Verificación de solución: ningún literal y su negación deben estar en la misma componente
        for i in range(1, self.n + 1):
            if self.cfc[i] == self.cfc[i + self.n]:
                return None

        # Aplicar orden topológico sobre el grafo condensado
        top_sort = orden_topologico_inverso(grafo_componentes)
        resultado = {}

        # Asignar valores a cada componente en el orden topológico
        for comp in top_sort:
            if comp not in resultado:
                for adj in grafo_componentes[comp]:
                    if adj in resultado and not resultado[adj]:
                        resultado[comp] = False
                        break
                else:
                    resultado[comp] = True

            for arista in inverso[comp]:
                neg = arista + self.n if self.n >= arista else arista - self.n
                if mapeo_nodo_componente[neg] in resultado:
                    if resultado[mapeo_nodo_componente[neg]] == resultado[comp]:
                        return None
                else:
                    resultado[mapeo_nodo_componente[neg]] = not resultado[comp]

        # por ultimo filtramos para quedarnos solo con los literales sin negar
        rem = []

        for llave in resultado:
            if resultado[llave]:
                for arista in inverso[llave]:
                    if arista <= self.n:
                        rem.append(arista)
        return rem


def predicado(grafo, pos, conflictos):
    """
    Predicado a evaluar en la búsqueda binaria, genera un 2-SAT y lo resuelve para obtener la solución del problema.
    """
    extra = pos + 1
    n = 3 * pos
    sat = SAT(n)

    for i in range(1, len(grafo)):
        adj = [indice for _, indice in grafo[i] if indice <= pos]
        for j, v in enumerate(adj):
            sat.agregar_clausula(v, 1, extra, 0)
            if j != 0:
                sat.agregar_clausula(extra - 1, 1, extra, 0)
            if j != len(adj) - 1:
                sat.agregar_clausula(extra, 1, adj[j + 1], 1)
            extra += 1

    for v, u in conflictos:
        if v > pos and u > pos:
            return None
        if v <= pos and u <= pos:
            sat.agregar_clausula(v, 0, u, 0)
        elif v <= pos:
            sat.agregar_clausula(v, 0, v, 0)
        else:
            sat.agregar_clausula(u, 0, u, 0)

    res = sat.resolver()
    
    if res is None:
        return None

    # Por ultimo filtramos para quedarnos solo con los nodos correspondientes a las aristas del problema
    rem = []

    for arista in res:
        if arista <= pos:
            rem.append(arista)
    return rem

def busqueda_binaria(grafo, aristas, pred, conflictos):
    """
    Realiza una búsqueda binaria sobre las aristas usando un predicado dado
    """
    l, r = 0, len(aristas)
    while l < r:
        mid = (l + r) // 2
        if pred(grafo, mid, conflictos) is not None:
            r = mid
        else:
            l = mid + 1
    return pred(grafo, l, conflictos)

def obtener_conflictos(grafo, aristas):
    """
    Calcula pares de aristas de un mismo color incidentes en un vértice.
    """
    conflictos = set()
    for nodo in range(1, len(grafo)):
        colores = {}
        for _, indice in grafo[nodo]:
            color = aristas[indice - 1][2]
            if color not in colores:
                colores[color] = [indice]
            else:
                colores[color].append(indice)

        if any(len(val) > 2 for val in colores.values()) or sum(len(val) == 2 for val in colores.values()) > 1:
            return None

        for color in colores:
            if len(colores[color]) == 2:
                conflictos.add(tuple(colores[color]))

    return conflictos

try:
    # Procesar entrada
    n, m = map(int, sys.stdin.readline().split())
    aristas = []
    for i in range(m):
        v, u, c, t = map(int, sys.stdin.readline().split())
        aristas.append((v, u, c, t, i+1))
    grafo = [[] for _ in range(n + 1)]

    # Ordenar aristas por tiempo y construir el grafo
    aristas.sort(key=lambda x: x[3])
    for i in range(m):
        grafo[aristas[i][0]].append((aristas[i][1], i+1))
        grafo[aristas[i][1]].append((aristas[i][0], i+1))

    # Obtener conflictos
    conflictos = obtener_conflictos(grafo, aristas)
    if conflictos is None:
        print("No")
    else:
        resultado = busqueda_binaria(grafo, aristas, predicado, conflictos)
        if resultado is None:
            print("No")
        else:
            print("Yes")
            print(aristas[max(resultado) - 1][3] if resultado else 0, len(resultado))
            print(" ".join(map(lambda x: str(aristas[x-1][4]), resultado)))
            
except Exception as e:
    print(e)
    exc_type, exc_value, exc_traceback = sys.exc_info()
    for tb in traceback.extract_tb(exc_traceback):
        print(f"Archivo: {tb.filename}, Línea: {tb.lineno}, Función: {tb.name}")
                