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

import config as cf
from App import model
import csv
import os
from DISClib.ADT import map as m
"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newCitibike()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def loadTrips(citibike):

    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(analyzer, filename)
    return analyzer

def loadFile(citibike, tripfile):
    """
    """
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTrip(citibike, trip)
        model.addTripMap(citibike,trip)
    return citibike

def ordenar_estaciones(citibike):
    return model.ordenar_estaciones(citibike)

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def componentesConectados(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.componentesConectados(analyzer)

def estacionesConectadas(analyzer, estacion1, estacion2):
    """
    Numero de componentes fuertemente conectados
    """

    return model.estacionesConectadas(analyzer, estacion1, estacion2)

def totalestaciones(analyzer):
    """
    Total de estaciones
    """
    return model.totalestaciones(analyzer)

def totalConnections(analyzer):
    """
    Total de enlaces 
    """
    return model.totalConnections(analyzer)

def encontrar_ciclos(analyzer,origen,tiempo1,tiempo2):

    return model.encontrar_ciclos(analyzer,origen,tiempo1,tiempo2)


    
def estacionS_criticas (analyzer):
    return model.estacionS_criticas(analyzer)

def estacionL_criticas (analyzer):
    return model.estacionL_criticas(analyzer)

def estacionG_criticas(analyzer):
    return model.estacionG_criticas(analyzer)