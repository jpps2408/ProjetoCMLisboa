import DirectoryExlorer as CD
from ShiftDirClass import *
from toolsgis import *
from ostools import *
from timeparsingtools import *
from cmd import Cmd
from MasterHandler_ import * 

######################################################
################## ##################
######################################################

#r"C:\Users\JoaoPedro\Documents\BIGDirectory"

path = input("Introduza o caminho: \n")
AS = AncientStructural(path)
circuit_list = AS.get_AllCircuits()
for circuit_folder in circuit_list:
    circuit = CD.CircuitDir(circuit_folder)
    shiftstoprocessincircuit_list = circuit.getRealizacoesDoNe()
    if circuit.start():
        for shift_folder in shiftstoprocessincircuit_list:



realizacao = r"C:\Users\JoaoPedro\Documents\BIGDirectory\CIRCUITS\I0103\aliasCircuitVoyages\Preparados\I0103_V2538_12_01_2020"
shift = ShiftDir(realizacao,circuit)
shift.process_shift()
######################################################
################## ##################
######################################################




