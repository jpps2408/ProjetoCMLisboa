import DirectoryExlorer as CD
from ShiftDirClass import *
from toolsgis import *
from ostools import *
from timeparsingtools import *
from cmd import Cmd
from MasterHandler_ import * 
#import inspect
#inspect.getargspec (pd.read_csv)
######################################################
################## ##################
######################################################

#r"C:\Users\JoaoPedro\Documents\BIGDirectory"

path = input("Introduza o caminho: \n")
AS = AncientStructural(path)
AS.retrieve_AllKmls()
circuit_list = AS.get_AllCircuits()
for circuit_folder in circuit_list:
    circuit = CD.CircuitDir(circuit_folder)
    circuit_name= os.path.basename(circuit_folder)
    shiftstoprocessincircuit_list = circuit.getRealizacoesDoNe()
    if circuit.start():
        for shift_folder in shiftstoprocessincircuit_list:
            shift_name = os.path.basename(shift_folder)
            print("\n\nSTARTED...\nCIRCUIT: {} \nSHIFT: {} ".format(circuit_name,shift_name))
            shift = ShiftDir(shift_folder,circuit)
            shift.process_shift()
            print("\n\CLEANED...\nCIRCUIT: {} \nSHIFT: {} ".format(circuit_name,shift_name))

dbfile = AS.run_dbcamara()
circuit_list = "C:\Users\JoaoPedro\Documents\BIGDirectory\CIRCUITS\I0103"
for circuit_folder in circuit_list:
    circuit = CD.CircuitDir(circuit_folder)
    circuit_name= os.path.basename(circuit_folder)
    shiftstoprocessincircuit_list = circuit.getRealizacoesToDo()
    if circuit.start():
        for shift_folder in shiftstoprocessincircuit_list:
            shift_name = os.path.basename(shift_folder)
            print("\n\nSTARTED...\nCIRCUIT: {} \nSHIFT: {} ".format(circuit_name,shift_name))
            shift = ShiftDir(shift_folder,circuit)
            try:
                shift.finalize_shift(AS.dbobject)
            except Exception as e:
                print(e)
                print("The shift was not finalized")
            else:
                AS.place_inFilled(shift)
            print("\n\CLEANED...\nCIRCUIT: {} \nSHIFT: {} ".format(circuit_name,shift_name))


######################################################
################## ##################
######################################################




