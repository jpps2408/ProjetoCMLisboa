import DirectoryExlorer as CD
from ShiftDirClass import *
from toolsgis import *
from ostools import *
from timeparsingtools import *


######################################################
################## ##################
######################################################

circuit_folder = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01\I0104"
circuit_object = CD.CircuitDir(circuit_folder)
circuit_object.make_CircuitPolygon(200)


realizacao = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01\I0104\aliasCircuitVoyages\aliasToDo\I0104_V2520_17_01_2020"
shift = ShiftDir(realizacao,circuit_object)
shift.process_shift(20)

######################################################
################## ##################
######################################################




