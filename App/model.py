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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newCitibike():
    """ Inicializa el analizador
   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'stationsS': None,
                    'graph': None,
                    'components': None,
                    'stationsL': None,
                    'ordenadosS': None,
                    'ordenadosL': None
                    }

        analyzer['stationsS'] = m.newMap(numelements=14000,
                                      maptype='PROBING',
                                      comparefunction=compareStopIds)
        analyzer['stationsL'] = m.newMap(numelements=14000,
                                      maptype='PROBING',
                                      comparefunction=compareStopIds)
        analyzer['stationsG'] = m.newMap(numelements=14000,
                                      maptype='PROBING',
                                      comparefunction=compareStopIds)                              
        analyzer['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)   
        analyzer['ordenadosS'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareIds)
        analyzer['ordenadosL'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareIds)
        analyzer['ordenadosG'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar informacion al grafo
def addTrip(citibike, trip):
    """
    """
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration)

def addTripMap(citibike, trip):
    mapS = citibike['stationsS']
    mapL = citibike['stationsL']
    mapG = citibike['stationsG']
    name_salida = trip['start station name']
    name_llegada = trip['end station name']
    vi = 1
    
    #Salida
    if m.contains(mapS, name_salida):
        valors = (m.get(mapS, name_salida)) 
        valorsr = int(valors["value"]) + 1
        m.put(mapS, name_salida, valorsr)
    else:
        m.put(mapS, name_salida, vi)
    #Llegada
    if m.contains(mapL, name_llegada):
        valorl = (m.get(mapL, name_llegada))
        valorlr = int(valorl["value"]) + 1
        m.put(mapL, name_llegada, valorlr)
    else:
        m.put(mapL, name_llegada, vi)
    #General
    if m.contains(mapG, name_salida):
        valorgs = (m.get(mapG, name_salida))
        valorgsr = int(valorgs["value"]) + 1
        m.put(mapG, name_salida, valorgsr)
    else:
        m.put(mapG, name_salida, vi)

    if m.contains(mapG, name_llegada):
        valorgl = (m.get(mapG, name_llegada))
        valorglr = int(valorgl["value"]) + 1
        m.put(mapG, name_llegada, valorglr)
    else:
        m.put(mapG, name_llegada, vi)

def addStation(citibike, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(citibike ["graph"], stationid):
            gr.insertVertex(citibike ["graph"], stationid)
    return citibike

def addConnection(citibike, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(citibike ["graph"], origin, destination)
    if edge is None:
        gr.addEdge(citibike["graph"], origin, destination, duration)
    return citibike

def ordenar_estaciones(citibike):
    mapS = citibike["stationsS"]
    OmapS = citibike["ordenadosS"]
    listaS = m.keySet(mapS)
    IterS = it.newIterator(listaS)
    while it.hasNext(IterS):
        i = it.next(IterS)
        valorS = m.get(mapS, i)
        om.put(OmapS, valorS["value"],valorS["key"])
    #___________________________________
    mapL = citibike["stationsL"]
    OmapL = citibike["ordenadosL"]
    listaL = m.keySet(mapL)
    IterL = it.newIterator(listaL)
    while it.hasNext(IterL):
        i = it.next(IterL)
        valorL = m.get(mapL, i)
        om.put(OmapL, valorL["value"],valorL["key"])
    #___________________________________
    mapG = citibike["stationsG"]
    OmapG = citibike["ordenadosG"]
    listaG = m.keySet(mapG)
    IterG = it.newIterator(listaG)
    while it.hasNext(IterG):
        i = it.next(IterG)
        valorG = m.get(mapG, i)
        om.put(OmapG, valorG["value"],valorG["key"])

# ==============================
# Funciones de consulta
# ==============================
def componentesConectados(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['graph'])
    return scc.connectedComponents(analyzer['components'])

def estacionesConectadas(analyzer, estacion1, estacion2):
    """
    Calcula si 2 estaciones estan fuertemente conectadas
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['graph'])
    return scc.stronglyConnected(analyzer['components'], estacion1, estacion2)

def totalestaciones(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['graph'])

def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['graph'])

def estacionS_criticas (analyzer):
    Omap = analyzer["ordenadosS"]
    Cont = 0
    lista = lt.newList(datastructure="ARRAY_LIST")
    while Cont != 3:
        maximae = om.maxKey(Omap)
        maximaE = om.get(Omap, maximae)
        lt.addLast(lista,maximaE["value"])
        om.deleteMax(Omap)
        Cont += 1
    f = str(lt.getElement(lista, 1))
    s = str(lt.getElement(lista, 2))
    t = str(lt.getElement(lista, 3))
    R = f + ", " + s + ", " + t
    return R

def estacionL_criticas(analyzer):
    Omap = analyzer["ordenadosL"]
    Cont = 0
    lista = lt.newList(datastructure="ARRAY_LIST")
    while Cont != 3:
        maximae = om.maxKey(Omap)
        maximaE = om.get(Omap, maximae)
        lt.addLast(lista,maximaE["value"])
        om.deleteMax(Omap)
        Cont += 1
    f = str(lt.getElement(lista, 1))
    s = str(lt.getElement(lista, 2))
    t = str(lt.getElement(lista, 3))
    R = f + ", " + s + ", " + t
    return R

def estacionG_criticas(analyzer):
    Omap = analyzer["ordenadosG"]
    Cont = 0
    lista = lt.newList(datastructure="ARRAY_LIST")
    while Cont != 3:
        minimae = om.minKey(Omap)
        minimaE = om.get(Omap, minimae)
        lt.addLast(lista,minimaE["value"])
        om.deleteMin(Omap)
        Cont += 1
    f = str(lt.getElement(lista, 1))
    s = str(lt.getElement(lista, 2))
    t = str(lt.getElement(lista, 3))
    R = f + ", " + s + ", " + t
    return R

# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1