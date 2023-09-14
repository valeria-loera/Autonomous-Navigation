# Autonomous Navigation Challenge
Reto de Navegación Autónoma basado en el algoritmo BFS, creado con Python para el University Rover Challenge de Quantum Robotics.

## Sobre el reto
En University Rover Challenge, existe una misión de Navegación Autónoma, en la cual es necesario buscar un código AR dada una coordenada aproximada donde podría estar. Por lo cual, se ha propuesto hacer un algoritmo de búsqueda de códigos ArUco, en el cual recibe unas coordenadas que sería la posición alrededor de la cual puede estar el código ArUco y unas coordenadas `ar_x` y `ar_y`, que tendrían la posición y orientación inicial del Rover. Únicamente se tiene `xr`, `yr`, `Θr` para trabajar en la trayectoria que seguiría el robot, no en la detección de los códigos. Se considera que la posición de inicio del robot será: `xr = 0` , `yr = 0` , `θr = 0`, y que las coordenadas del código ArUco serán generadas de manera aleatoria.


## Algoritmo de búsqueda BFS
### ¿Qué es el algoritmo BFS?
Búsqueda en Anchura (BFS) es un algoritmo simple que explora todos los nodos en el mismo nivel antes de pasar al siguiente nivel; puede ser útil para exploración y mapeo del entorno.

### ¿Por qué BFS?
Dado a que el objetivo del reto fue llevar al rover desde su posición inicial a unas coordenadas determinadas sin considerar la complejidad del terreno ni los obstáculos, bastó con un algoritmo de búsqueda simple y efectivo como el algoritmo de búsqueda en anchura (BFS). Resulta una opción adecuada ya que, para este reto, explora todas las posibles rutas desde la posición inicial hasta las coordenadas objetivo y encuentra la más corta en términos del número de movimientos.

### ¿En qué consiste?
Utiliza una estrategia de búsqueda por niveles y se expande a todos los nodos vecinos antes de avanzar a los siguientes niveles. Aunque su complejidad en tiempo puede ser alta en grafos muy grandes, si el espacio de búsqueda no es extremadamente grande, el BFS es una opción eficiente. En este sentido, el algoritmo funciona de la siguiente manera:

>  Inicializar una cola con la posición inicial del rover.
>  Mientras la cola no esté vacía:
> * Sacar el nodo (posición actual del rover) de la cola.
> * Si el nodo coincide con las coordenadas objetivo, se ha encontrado la solución.
> * De lo contrario, agregar todos los nodos vecinos (posibles movimientos) a la cola.
> 
>  Repetir el ciclo hasta encontrar las coordenadas objetivo o hasta que la cola esté vacía.

La cola se usa para mantener un conjunto de nodos que se deben visitar durante el proceso de búsqueda y determinar qué nodo se debe explorar a continuación. En este algoritmo, un nodo representa un punto en el grafo que puede estar conectado a otros nodos a través de aristas; en este caso, refiere a una posición o estado específico en el espacio de búsqueda del código ArUco. 

<img width="450" alt="bfs_ejemplo" src="https://github.com/valeria-loera/Autonomous-Navigation/assets/140004567/163d4190-2975-4a86-9ac3-4ddd95f4253c">

En el diagrama anterior se muestra como:
> * En el nivel 0, se marca el nodo como inicial.
> 
> * Después, se explora y atraviesan los nodos no visitados adyacentes al nodo inicial.
> 
> * Finalmente, se marca el nodo como completado o visitado y se mueve al siguiente nodo adyacente y que no ha sido visitado.


## Implementación del algoritmo
Cada nodo en el grafo representa una posición en el plano bidimensional con coordenadas (*x*, *y*). Las aristas del grafo representan los movimientos del rover desde una posición a otra. Así, estando en el nodo `node` `(x, y)`, el rover puede moverse a los nodos vecinos `node_neighbor` `(x+1, y)`, `(x-1, y)`, `(x, y+1)`, y `(x, y-1)`.
El algoritmo comienza con el nodo de inicio `p_inicial`, que es la posición inicial del rover `(xr, yr)`. Se agrega el `p_inicial` al `queue`, una cola con una estructura de datos `deque` de la biblioteca `collections` que se utiliza para mantener un registro de los nodos que se deben explorar. Se inicializa el ciclo mientras `queue` no esté vacía, y se saca el nodo actual `current_node`. Si `current_node` coincide con las coordenadas del código ArUco `(ar_x, ar_y)`, se ha encontrado la solución y se detiene el algoritmo; en caso contrario, se agregan al `queue` todos los `node_neighbor` que no han sido visitados, los cuales se han agregado al conjunto `visited` para evitar repeticiones. 

## Trayectoria del rover
### Recuperación de la ruta
La recuperación de la ruta implica rastrear desde el nodo de destino `p_aruco` hasta el nodo de inicio `p_inicial` siguiendo los padres de cada nodo visitado durante la búsqueda. Se creó un diccionario llamado `parents` donde se registra el nodo padre `current_node` de cada nodo de `visited`. Tras finalizar el algoritmo de búsqueda, se llama a la función `construir_ruta`, que recibe el diccionario `parents` y las coordenadas finales `p_aruco`, e inicializa la lista `ruta` para  almacenar los nodos de la ruta en orden. Para ello, se crea la variable `step_node` con el valor de `p_aruco`, de modo que se comienza desde el punto final y retrocede a lo largo de la ruta hacia el punto inicial. A continuación, se va agregando el valor `step_node` a ruta, y se actualiza valor de `step_node` a partir del diccionario `parents`, por lo que el ciclo se ejecuta mientras aún existan nodos en `ruta` y se haya llegado al nodo inicial (`step_node is None`). Una vez que se ha recorrido toda la ruta, se invierte la lista `ruta` utilizando el método `reverse()` para que esté en orden desde el punto inicial hasta el punto final.

<img width="450" alt="impresion2" src="https://github.com/valeria-loera/Autonomous-Navigation/assets/140004567/39c0b729-8369-4721-9fe7-da136cb6bd8d">


### Orientación del rover
Para obtener la orientación `ar_𝜽` que el rover tendrá al momento de buscar la coordenada del código ArUco, se consideró la trayectoria del rover como la hipotenusa de un triángulo rectángulo, cuyo cateto opuesto es la diferencia entre las coordenadas en *y* de la posición inicial y la posición del código (`ar_y - yr`), y el cateto adyacente la diferencia entre las coordenadas en *x* de la posición inicial y la posición del código (`ar_x - xr`). Así, si el valor del cateto adyacente daba `0`, `ar_𝜽 = 90°`, en caso contrario, `ar_𝜽` será la tangente inversa del cateto opuesto entre el cateto adyacente. 

<img width="450" alt="orientacion" src="https://github.com/valeria-loera/Autonomous-Navigation/assets/140004567/cec8a1d7-9f2e-4297-9c9c-34a832858722">

### Ejes del gráfico
Antes de graficar la trayectoria, se dibujaron las líneas del sistema de coordenadas donde se encuentran el rover y el código ArUco, con sus respectivas etiquetas indicando el eje *x* y el eje *y*. Para ello, se implementó `Turtle`, librería de Python que proporciona una forma simple y gráfica de crear dibujos y gráficos en dos dimensiones. 

<img width="450" alt="ejes_coordenadas" src="https://github.com/valeria-loera/Autonomous-Navigation/assets/140004567/a04f29f6-017d-47a2-acd1-29b363f2b3c5">

### Gráfico de la trayectoria
Se configuró el diseño gráfico de la ventana de Turtle y crearon dos tortugas: `coordenada` que muestra los valores de las coordenadas, y `rover` que se desplaza en la pantalla. Las coordenadas iniciales y finales `p_initial` y `p_aruco` se escriben en la pantalla, junto con el ángulo `ar_𝜽`. El rover se mueve desde su posición inicial a la final y se marca con un cuadrado. Finalmente, la ventana de Turtle se cierra al hacer clic en ella, y el código devuelve el valor del ángulo `ar_𝜽`.

![trayectoria](https://github.com/valeria-loera/Autonomous-Navigation/assets/140004567/fa306633-5497-4efc-8652-9077515aec29)
