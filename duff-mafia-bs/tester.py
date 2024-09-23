"""
Tester para D. Duff in Mafia

El algoritmo generado el n, m, y las aristas en caso de no tener ningunas por defecto

N se genera en el rango 3-7, mientras que m en 3-15, para las aristas se genera primero 
un vertice y despues el segundo de tal forma que sea menor que el primero, para evitar repiticiones.
Las aristas reciben un color y un tiempo de eliminacion al azar

Para revisar la salida del algoritmo primero se prueban todas las posibles soluciones al problema, y se guarda el tiempo de la mejor,
en caso de existir. En ambos casos se revisas si el algoritmo responde que hay o no respuesta y si esto es correcto.
El tiempo se compara con el tiempo del algoritmo, en caso de ser iguales, se comprueba que la solucion del algoritmo es correcta.

La entrada generada se guarda en el archivo caso.txt y la salida en salida.txt
"""

import os
import random
import sys

from subprocess import Popen, PIPE, TimeoutExpired


style = True

num_tests = 10000

#entrada del problema
n = 0
m = 0


edges = []

# tiempo limite
time_limit = 3

os.system("")

RED = '\033[31m'
GREEN = '\033[32m'
WHITE = '\033[37m'

def write(color, text):
    """
    Funcion para escribir en consola usando colores
    """
    if style:
        print(color + text)
        sys.stdout.write(WHITE)
    else:
        print(text)

def write_to_file(name, text):
    """
    Funcion para escribir en un archivo
    """
    file = open(name, "w")
    file.write(text)
    file.close()


def check(n, edges, value):
    """
    Dada la cantidad de nodos, las aristas y una mascara de bits
    Se revisa si eliminando los elementos marcados con 1 en la mascara
    se obtiene una respuesa correcta
    """
    current = []
    removed = []
    # procesamos la mascara de bits
    for i in range(len(edges)):
        if value % 2 == 0:
            current.append(edges[i])
        else:
            removed.append(edges[i])
        value = value >> 1
    
    # guardamos los colores y nos aseguramos de que el grafo esta bien coloreado
    colors = {i : set() for i in range(1, n+1)}
    for edge in current:
        if edge[2] in colors[edge[0]]:
            return False, 0
        if edge[2] in colors[edge[1]]:
            return False, 0
        colors[edge[0]].add(edge[2])
        colors[edge[1]].add(edge[2])
    
    # revisamos que las aristas eliminadas no tengan nodos en comun
    for i in range(len(removed)):
        for j in range(i+1, len(removed)):
            if removed[i][0] == removed[j][0] or removed[i][0] == removed[j][1]:
                return False, 0
            if removed[i][1] == removed[j][0] or removed[i][1] == removed[j][1]:
                return False, 0
    # devolvemos que existe solucion y el tiempo necesario para la misma
    return True, removed[-1][3] if removed else 0 
    

def solve(n, edges):
    """
    Dada la cantidad de nodos y las aristas encuentra un optimo al problema
    """
    edges = sorted(edges, key=lambda x: x[3]) # primero se ordenan por tiempo de eliminacion
    # luego se recorren las posibles mascaras de bits, de forma tal que siempre intenta eliminar
    # los elementos con menor tiempo de eliminacion
    for value in range(2 << (n+1)):
        sol, t = check(n, edges, value)
        if sol:
            return "Yes", t
    return "No", 0

for test in range(num_tests):
    # Generamos los valores aleatorios para n, m y edges en cada iteración
    n = random.randint(3, 7)
    m = random.randint(3, 15)
    edges = []
    for _ in range(m):
        first = random.randint(2, n)
        edges.append((first, random.randint(1, first - 1), random.randint(1, n), random.randint(1, 20)))

    # Generar la entrada del problema y guardar en un archivo
    args = "{} {}\n{}".format(n, m, "\n".join([" ".join(map(str, edge)) for edge in edges]))
    write_to_file("caso.txt", args)

    # Ejecutar el código
    process = Popen([sys.executable, "-Xfrozen_modules=off", "code.py"], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    try:
        # Pasar la entrada al código y procesar la respuesta
        output, error = process.communicate(input=args.encode(), timeout=time_limit)
        if error:
            write(RED, error.decode())
            continue  # Saltar a la siguiente iteración en caso de error

        write_to_file("salida.txt", output.decode())
        output = output.decode().splitlines()
        solution, time = solve(n, edges)

        # Verificar la respuesta del algoritmo
        if output[0] != solution:
            write(RED, "Wrong answer")
            continue
        if solution == "Yes":
            t, k = map(int, output[1].split())
            if t != time:
                write(RED, "Wrong answer")
                continue
            if t != 0:
                result = list(map(int, output[2].split()))
                value = 0
                for i in result:
                    value |= (1 << (i - 1))
                if not check(n, edges, value):
                    write(RED, "Wrong answer")
                    continue
        write(GREEN, "Correct answer")

    except TimeoutExpired:
        write(RED, "Time limit exceeded")