"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import list as lt
from DISClib.ADT import queue as que



"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________
servicefile="201801-2-citibike-tripdata.csv"
# servicefile="201801-1-citibike-tripdata.csv"
# servicefile='201801-3-citibike-tripdata.csv'
# ___________________________________________________
#  Menu principal
# ___________________________________________________
def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de Citibike")
    print("3- Calcular componentes conectados")
    print("4- Calcular rutas circulares")

def optionTwo():
    print("\nCargando información de Citibike ....")
    controller.loadFile(cont,servicefile)
    # numedges = controller.totalConnections(cont)
    # numvertex = controller.totalStops(cont)
    # print('Numero de vertices: ' + str(numvertex))
    # print('Numero de arcos: ' + str(numedges))
    # print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    # sys.setrecursionlimit(recursionLimit)
    # print('El limite de recursion se ajusta a: ' + str(recursionLimit))
    #D:\SEGUNDO SEMESTRE\ESTRUCTURA DE DATOS Y ALGORITMOS\LAB 12\EDA-2020-20-Lab-12-SEC-05-GRUPO-06\Data

def optionThree():
    conectados = controller.estacionesConectadas(cont, estacion1, estacion2)
    if conectados == True:
        print(str(estacion1) + " y " + str(estacion2) + " estan fuertemente conectados")
    else:
        print(str(estacion1) + " y " + str(estacion2) + " no estan fuertemente conectados")
    return None

def optionFour():
    lista=controller.encontrar_ciclos(cont,origen,tiempo1,tiempo2)
    iterador=it.newIterator(lista)
    contador=0
    print("se encontraron: "+str(lt.size(lista))+" rutas circulares.")
    while it.hasNext(iterador):
        contador+=1
        tupla=it.next(iterador)
        ciclos=tupla[0]
        costo=tupla[1]
        print(str(contador)+".\n")
        while not que.isEmpty(ciclos):
            print(que.dequeue(ciclos))
        print("el tiempo estimado es: "+ str(round(costo))+" minutos\n")



# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        estacion1 = input("Ingrese la primera estación:\n ")
        estacion2 = input("Ingrese la segunda estación:\n ")
        executiontime = timeit.timeit(optionThree, number=1)
        a=cont["components"]
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        origen = input("Estación Base: ")
        tiempo1=int(input("Igrese el minimo de tiempo: "))
        tiempo2=int(input("Ingrese el maximo de tiempo: "))
        executiontime = timeit.timeit(optionFour, number=1)
        # print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        destStation = input("Estación destino (Ej: 15151-10): ")
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 6:
        destStation = input("Estación destino (Ej: 15151-10): ")
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 7:
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    else:
        sys.exit(0)
sys.exit(0)