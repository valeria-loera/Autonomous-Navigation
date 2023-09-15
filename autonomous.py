#AUTONOMOUS NAVIGATION CHALLENGE
#Reto de Navegación Autónoma basado en el algoritmo BFS, creado con Python para el University Rover Challenge de Quantum Robotics.
#Nombre: Valeria Loera Gómez
#Fecha: 14/09/23
#Versión: 1.0

import random
import math
from collections import deque
import turtle

#ALGORITMO DE BÚSQUEDA BFS
def algoritmo_bfs(p_initial, p_aruco, ar_𝜽):
    queue = deque()
    visited = set()
    parents = {}

    queue.append(p_initial)
    parents[p_initial] = None 

    while queue:
        current_node = queue.popleft()
        if current_node == p_aruco:
            ruta = construir_ruta(parents, p_aruco)
            return ruta
        
        visited.add(current_node)

        x, y = current_node
        node_neighbor = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for node in node_neighbor:
            if node not in visited:
                queue.append(node)
                parents[node] = current_node
    
    return None


#RECUPERACIÓN DE LA RUTA
def construir_ruta(parents,p_aruco):
    ruta = []
    step_node = p_aruco

    while step_node is not None:
        ruta.append(step_node)
        step_node = parents [step_node]

    ruta.reverse()
    return ruta
    


#CÁLCULO DEL ÁNGULO DEL ORIGEN AL CÓDIGO ARUCO
def calculo_angulo(xr, yr, ar_x, ar_y):
    co = ar_y - yr
    ca = ar_x - xr

    if ca == 0:
        ar_𝜽 = 90
    else:
        ar_𝜽 = math.degrees(math.atan(co/ca))
    return ar_𝜽


#DISEÑO PLANO GRÁFICO TURTLE
def diseno_grafico():
    screen = turtle.getscreen()
    turtle.title("Trayectoria Rover a Código ArUco") 
    turtle.bgcolor("#acdbfc")
    screen.setworldcoordinates(-1, -1, 17, 17)

    linea = turtle.Turtle()

    linea.shapesize(1,1,1)
    linea.speed(100)
    linea.color("#ffffff")
    
    #EJE Y
    linea.left(90)
    linea.goto(0,15)
    linea.stamp()

    linea.penup()
    linea.goto(0,15.5)
    linea.pencolor("#243d82")
    linea.write("y", font=("Open Sans", 16))
    linea.pencolor("#ffffff")
    
    #EJE X
    linea.penup()
    linea.right(90)
    linea.goto(0,0)
    linea.pendown()

    linea.goto(15,0)
    linea.stamp()

    linea.penup()
    linea.goto(15.5,0)
    linea.pencolor("#243d82")
    linea.write("x", font=("Open Sans", 18))
    linea.pencolor("#ffffff")

    linea.penup()
    linea.goto(0,0)
    



#GRÁFICO DE LA TRAYECTORIA DEL ROVER EN TURTLE
def grafico_turtle(p_initial, p_aruco, ar_x, ar_y, ar_𝜽):
    diseno_grafico()
    coordenada = turtle.Turtle()
    coordenada.shape("circle")
    coordenada.shapesize(0.01, 0.01, 0.01)
    coordenada.pencolor("#243d82")
    
    #crear turtle del rover
    rover = turtle.Turtle()
    rover.shape("square")
    rover.shapesize(0.75,0.75,0.75)

    #escribir coordenada origen
    coordenada.speed(300)
    coordenada.penup()
    coordenada.goto(-0.5,-0.75)
    coordenada.write(p_initial, font=("Verdana", 14))
    
    #movimiento del rover
    rover.speed(1)
    rover.left(ar_𝜽)
    rover.dot(8)
    rover.goto(p_aruco)
    rover.pendown

    #escribir coordenada final
    coordenada.goto(ar_x - 0.25,  ar_y + 0.5)
    coordenada.write(p_aruco, font=("Verdana", 14))

    #escribir ángulo
    coordenada.goto(13,0.5)
    coordenada.write(f"\n𝜽: {ar_𝜽:.2f}°", font=("Verdana", 14))

    turtle.Screen().exitonclick()

    return ar_𝜽




def main():
    #VALORES INCIIALES
    xr = 0
    yr = 0
    𝜽r = 0
    p_initial = (xr, yr)

    ar_x = random.randint(0,15)
    ar_y = random.randint(0,15)
    ar_𝜽 = 0
    p_aruco = (ar_x, ar_y)


    #IMPPRESIÓN RESULTADOS
    print("\n\n\t⋙⋙ TRAYETCORIA ROVER QUANTUM ROBOTICS ⋘⋘")
    print("\nPOSICIÓN INICIAL: ", p_initial)
    print("POSICIÓN CÓDIGO ARUCO: ", p_aruco)


    ruta = algoritmo_bfs(p_initial, p_aruco, ar_𝜽)
    for step_node in ruta:
        print("\nPOSICIÓN ROVER: ", step_node)
        print("POSICIÓN CÓDIGO ARUCO: ", p_aruco)

    ar_𝜽 = calculo_angulo(xr,yr,ar_x,ar_y)
    print(f"\nORIENTACIÓN RESULTANTE: {ar_𝜽:.3f}°")

    grafico_turtle(p_initial, p_aruco, ar_x, ar_y, ar_𝜽)

    print()

main()
