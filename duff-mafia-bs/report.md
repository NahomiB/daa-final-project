# Problema "Binary Search"

## [Duff in Mafia](https://codeforces.com/problemset/problem/587/D)

Duff es una de las jefas de la Mafia en su país, Andarz Gu. Andarz Gu tiene $n$ ciudades (numeradas del 1 al $n$) conectadas por $m$ carreteras bidireccionales (numeradas del 1 al $m$).

Cada carretera tiene un tiempo de destrucción y un color. La $i$-ésima carretera conecta las ciudades $v_i$ y $u_i$, su color es $c_i$ y su tiempo de destrucción es $t_i$.

La Mafia quiere destruir un emparejamiento en Andarz Gu. Un emparejamiento es un subconjunto de carreteras tal que ninguna de las dos carreteras en este subconjunto tiene un extremo en común. Pueden destruir estas carreteras en paralelo, es decir, el tiempo total de destrucción es el máximo de los tiempos de destrucción de todas las carreteras seleccionadas.

Quieren que se cumplan dos condiciones:

1. Las carreteras restantes forman una coloración propia.
2. El tiempo de destrucción de este emparejamiento se minimiza.

Las carreteras restantes después de destruir este emparejamiento forman una coloración propia si y solo si no hay dos carreteras del mismo color que tengan el mismo extremo; en otras palabras, los bordes de cada color deben formar un emparejamiento.

No hay programador en la Mafia. Por eso, Duff te pidió ayuda. Por favor, ayúdala a determinar qué emparejamiento destruir para satisfacer esas condiciones (o indicar que esto no es posible).

### Entrada

La primera línea de entrada contiene dos enteros $n$ y $m$ ($2 \leq n \leq 5 \times 10^4$ y $1 \leq m \leq 5 \times 10^4$), el número de ciudades y el número de carreteras en el país.

Las siguientes $m$ líneas contienen las carreteras. La $i$-ésima de ellas contiene cuatro enteros $v_i, u_i, c_i$ y $t_i$ ($1 \leq v_i, u_i \leq n$, $v_i \neq u_i$ y $1 \leq c_i, t_i \leq 10^9$ para cada $1 \leq i \leq m$).

### Salida

En la primera línea de salida, imprime "Sí" (sin comillas) si es posible satisfacer la primera condición y "No" (sin comillas) en caso contrario.

Si es posible, entonces debes imprimir dos enteros $t$ y $k$ en la segunda línea, el tiempo mínimo de destrucción y el número de carreteras en el emparejamiento.

En la tercera línea, imprime $k$ enteros distintos separados por espacios, los índices de las carreteras en el emparejamiento en cualquier orden. Las carreteras están numeradas desde uno en orden de su aparición en la entrada.

Si hay más de una solución, imprime cualquiera de ellas.

## Reinterpretación del problema

Consideremos un grafo no dirigido $G$ que consta de $n$ nodos y $m$ aristas. Cada arista $e_i$ posee 2 valores $c_i$ y $t_i$ tal que $c_i$ es el color correspondiente a la arista y $t_i$ el tiempo que toma eliminarla.  El objetivo es eliminar aristas de $G$ en el menor tiempo posible en el menor tiempo posible, cumpliendo las siguientes restricciones:

- No se pueden eliminar dos aristas que compartan un nodo.

- No pueden quedar dos aristas del mismo color que compartan un nodo.

- El tiempo total para eliminar un conjunto $E$ de aristas se define como $\max_{e_i \in E}{t_i}$

Si no es posible eliminar un conjunto de aristas que cumpla con estas condiciones, se debe imprimir "No". Si existe una solución, se debe imprimir "Sí", seguido del tiempo requerido y la cantidad de aristas a eliminar. Finalmente, se debe mostrar el conjunto de aristas a eliminar.

## Propuesta de solución

Dado un conjunto de aristas $E$ en el grafo, se pueden ordenar estas aristas según el tiempo $t_i$ que toma eliminarlas, en orden no decreciente. Este orden nos permitirá analizar el tiempo de eliminación de manera eficiente.

Una vez que hemos ordenado las aristas, podemos aplicar un algoritmo de búsqueda binaria sobre este conjunto ordenado para determinar el tiempo mínimo necesario para eliminar un conjunto válido de aristas, teniendo en cuenta que **es posible eliminar aristas del prefijo de longitud $i$ de forma correcta para obtener un grafo válido.**

## Demostración

Si encontramos una solución $s_i$ que permite eliminar aristas del prefijo $p_i$ de longitud $i$ podemos afirmar que esta solución también será válida para cualquier $j > i$. Esto se debe a que todas las aristas eliminadas pertenecen al conjunto $p_i$ y y por lo tanto, también están incluidas en el conjunto $p_j$.

Luego al aplicar que es posible eliminar aristas del prefijo de longitud $i$ de forma correcta para obtener un grafo válido, sobre la secuencia $1, 2, 3, \ldots, n$ se obtiene la secuencia $0, 0, \ldots, 0, 1, 1, \ldots, 1, 1$ sobre la que se puede aplicar búsqueda binaria para encontrar el primer elemento donde el predicado se cumple.

si en algún momento se detecta que existen más de una pareja de aristas del mismo color conectadas a un mismo nodo, se puede concluir que no existe solución válida. Esto es porque, según las restricciones, solo se puede eliminar una arista que incida en ese nodo. Por lo tanto, no se podrá cumplir la condición de no dejar dos aristas del mismo color en ese nodo, haciendo imposible encontrar una solución viable.

Dado un prefijo $p$ del conjunto de aristas $E$ definimos una variable booleana para cada arista $e_i \in E$, donde será True si la arista $e_i$ será eliminado del grafo $G$, False si no es eliminada. El objetivo es determinar si existe una asignación de True o False para cada arista, de modo que se cumplan las restricciones del problema y se obtenga una solución válida. Este problema se puede modelar utilizando la técnica de 2-SAT de la siguiente manera:

- si dos aristas $e_i$ y $e_j$ comparten un nodo y tienen el mismo color, necesitamos eliminar al menos una de ellas para evitar que dos aristas del mismo color incidan en un mismo nodo. Esto lleva a la clausula lógica $e_i \lor e_j$ ya que necesitamos eliminar uno de ellos.

- si existe un subconjunto de aristas $e_1, e_2, \ldots, ... e_k$ con un nodo en común entonces $\forall i < j \quad \neg{e_i} \lor \neg{e_j}$ ya que si decidimos eliminar una arista $e_i$ entonces necesitamos que el resto no sean eliminadas.

Con estas dos reglas, hemos convertido el problema de eliminar aristas en una instancia de 2-SAT, donde las cláusulas lógicas describen las restricciones sobre qué aristas pueden ser eliminadas.

### Resolución mediante 2-SAT

El problema de 2-SAT consiste en encontrar una asignación de valores True o False para un conjunto de literales $a_1, a_2, \ldots, a_n$, de manera que se satisfagan $m$ clausulas de la forma $a_i \lor a_j$, entonces el 2-SAT retorna True si existe una asignación de True para cada literal $a_i$ de forma tal que todas las clausulas sean verdaderas, False en caso contrario.

Este problema se puede modelar como un grafo dirigido con las siguientes características:

Por cada literal $a_i$, se crean dos nodos en el grafo: uno para el literal $a_i$ y otro para su complemento $\neg{a_i}$

Por cada claúsula de la forma $a_i \lor a_j$, sse puede reescribir como dos implicaciones: $\neg a_i \implies a_j$ y $\neg a_j \implies a_i$. Esto se modela en el grafo añadiendo dos aristas: la primera que va del nodo $a_i$ al nodo $\neg{a_j}$ y otra de $a_j$ a $\neg{a_i}$.

Notese que en caso de existir un camino en el grafo de $a_i$ a $a_j$ dada la transitividad de la implicación lógica podemos decir que $a_i \implies a_j$

Una vez que se ha construido este grafo, el siguiente paso es identificar las componentes fuertemente conexas. Si un literal $a_i$ y su complemento $\neg{a_i}$ se encuentran en la misma componente fuertemente conexa, significa que hay una contradicción. Esto se debe a que existe un camino desde $a_i$ hasta $\neg{a_i}$ y de $\neg{a_i}$ a $a_i$. por lo tanto $a_i \implies \neg{a_i}$ y $\neg{a_i} \implies a_i$ lo cual es una contradicción. En este caso, no existe una asignación válida para los literales, y el 2-SAT devolverá False.

Una vez identificadas las componentes fuertemente conexas, se construye un grafo dirigido acíclico (DAG), donde cada nodo representa una componente fuertemente conexa. Entre dos nodos $a$ y $b$ del DAG, existirá una arista $(a,b)$ si hay una arista entre algún nodo de la componente correspondiente a $a$ y algún nodo de la componente correspondiente a $b$ en el grafo original.

El nuevo grafo obtenido es un grafo dirigido acíclico (demostrado en EDA). Luego posee un orden topológico (demostrado en EDA). Una vez obtenido un orden topológico podemos invertirlo y realizar las siguientes operaciones en orden:

Si una componente no tiene un valor asignado, se le asigna True a todos los nodos dentro de esa componente.

Una vez que a un nodo se le asigna un valor, se asigna el valor contrario a su complemento. Este valor se extiende a todos los nodos de la misma componente.

Si una componente se le asigna False, todas las componentes que tengan un camino hacia esa componente en el DAG también recibirán el valor False.

Este procedimiento garantiza que todas las asignaciones sean consistentes y que no haya contradicciones entre los nodos y sus complementos, ya que los literales $a_i$ y $\neg{a_i}$ pertenecen a componentes diferentes.

Como este algoritmo siempre es posible podemos decir que el 2-SAT tiene solución si y solo si para todo nodo $x$ se cumple que $x$ y $\neq{x}$ pertenecen a distintas componentes fuertemente conexas.

### Problema con la solución actual

Cuando se resuelve el problema para un prefijo $p_i$ e las aristas, no se toma en cuenta el caso en el que existan dos aristas $e_j, e_k$ tal que $e_j \in p_i$ y $e_k \notin p_i$ pero que $e_j$ y $e_k$ que compartan un nodo y tengan el mismo color. En este caso, para que exista una solución el prefijo $p_i$, $e_j$ debe ser eliminado del grafo.

Para corregir esto, se puede agregar la cláusula  $e_j \lor e_j$ en el 2-SAT, lo que fuerza la eliminación de $e_j del grafo y asegura que el prefijo $p_i$ cumpla con las restricciones.

### Salida del programa

Al resolver el problema usando búsqueda binaria sobre los prefijos de las aristas y aplicando 2-SAT para verificar la validez de cada prefijo, se obtiene lo siguiente: si no se encuentra un prefijo que contenga una solución válida, el programa imprimirá "No". En caso de que exista una solución, el programa imprimirá "Yes", seguido del tiempo mínimo obtenido por la búsqueda binaria, junto con la cantidad de aristas a eliminar y las aristas correspondientes, de acuerdo con la asignación de True realizada por el 2-SAT en el prefijo válido.

## Complejidad temporal

Para un conjunto de $n$ literales y $m$ cláusulas, el 2-SAT genera un grafo con $2n$ nodos y $2m$ aristas, y calcular las componentes fuertemente conexas toma $O(n+m)$. Revisar que un nodo y su complemento no pertenezcan a la misma componente se puede realizar en $O(n)$ operaciones.

La construcción del grafo de componentes también toma $O(n+m)$, y obtener su orden topológico tiene la misma complejidad.

Evaluar los literales y propagar la información requiere $O(n+m)$, ya que debemos asignarle valor a cada nodo y a lo sumo revisamos cada arista una única vez. Luego podemos resolver el predicado para un 2-SAT de $n$ literales y $m$ clausulas en tiempo $O(n+m)$.

Para el problema completo, se revisa que no haya más de dos pares de aristas del mismo color en cada nodo en $O(n+m)$. Antes de la búsqueda binaria, las aristas se ordenan por tiempo de eliminación en $O(m\log{m})$. La búsqueda binaria hace $O(\log(m))$ evaluaciones, y cada evaluación del predicado genera $O(m^2)$ cláusulas, con una complejidad total de $O(n+m^2)\cdot\log{m}$.

Una forma de optimizar el número de cláusulas generadas en el predicado para el 2-SAT es evitar la creación de todas las posibles parejas de aristas que inciden en un mismo nodo. En su lugar, se pueden introducir $k$ nuevos literales $p_1, p_2, \ldots, p_k$ para un conjunto de aristas $e_1, e_2, \ldots, e_k$ que comparten un nodo en común. Luego, se añaden las siguientes cláusulas:

$\neg{e_i} \lor p_i$ para cada $i$
$\neg{p_{i-1}} \lor p_i$ para todo $i \geq 1$
$\neg{e_{i+1}} \lor \neg{p_i}$ para cada $i$
Con este enfoque, se mantienen $O(m)$ literales, pero las cláusulas se reducen a $O(m)$ en lugar de $O(m^2)$. Esto reduce la complejidad del problema a $O((n + m) \log{m})$.

Demostremos ahora que esta mejora es válida.

Sea un conjunto de aristas $e_1, e_2, e_3, \ldots e_k$ que inciden sobre un mismo nodo. Si no se elimina ninguna arista, las cláusulas $(1)$ y $(3)$ se cumplen, y la cláusula $(2)$ se satisface si se asigna el valor True a todos los $p_i$. Si se elimina una sola arista $e_i$, se le asigna el valor True, y al resto de las aristas el valor False. Por la cláusula $(1)$, $p_i$ debe ser True, y asignando False a $p_j$ para todo $j \neq i$, se cumplen las tres cláusulas para todos los $i$.

Si se intentan eliminar dos aristas $e_i$ y $e_j$ con $i < j$, sin pérdida de generalidad, la cláusula $(1)$ implica que $p_i$ es True. La cláusula $(2)$ establece una relación de implicación entre los $p_i$, lo que significa que si $p_i$ es True, entonces $p_{i+1}, p_{i+2}, \ldots, p_k$ también lo serán. Como $j > i$, $p_{j-1}$ también será True. Sin embargo, por la cláusula $(3)$, esto implica que $e_j$ debe ser False, lo que genera una contradicción, demostrando que no se pueden eliminar dos aristas.

En conclusión, las nuevas cláusulas garantizan que a lo sumo se elimine una arista, lo que asegura el comportamiento deseado y valida la corrección del algoritmo.

## Pruebas

Dada la complejidad del código, las pruebas realizadas en Codeforces presentaron dificultades significativas, particularmente debido a errores de tiempo de ejecución difíciles de diagnosticar. Para abordar estos problemas, se desarrolló un tester que se ejecutó 10,000 veces, produciendo respuestas correctas en todas sus ejecuciones.

### Funcionamiento del Tester

A continuación, se describen sus componentes principales:

Generación de Entrada:

Se generan los valores de n y m, donde n varía entre 3 y 7 y m entre 3 y 15.
Las aristas se generan aleatoriamente. Para cada arista, se selecciona un primer vértice y un segundo vértice de manera que el segundo sea menor que el primero, evitando repeticiones. Además, cada arista recibe un color y un tiempo de eliminación aleatorios.

Pruebas de Salida:

Para verificar la salida del algoritmo, se calculan todas las posibles soluciones al problema, guardando el tiempo de la mejor solución si existe.

Se compara la respuesta del algoritmo con la respuesta correcta: si el algoritmo afirma que hay una solución, se valida que esto sea cierto. Si la solución existe, se comprueba que el tiempo de ejecución del algoritmo sea correcto y que la solución proporcionada sea válida.
