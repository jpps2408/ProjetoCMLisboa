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

#path = input("Introduza o caminho: \n")
path =r"C:\Users\JoaoPedro\Documents\BIGDirectory"
AS = AncientStructural(path)
try:
    AS.retrieve_AllKmls()
except:
    print("empty KML folder")

try:
    dbfile = AS.run_dbcamara()
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
                try:
                    shift.process_shift(AS.dbobject)
                    print("\n\CLEANED...\nCIRCUIT: {} \nSHIFT: {} ".format(circuit_name,shift_name))
                except:
                    print("\n\SKIPPED...\nCIRCUIT: {} \nSHIFT: {} ".format(circuit_name,shift_name))
                    pass
            circuit.write_summaries()
            

                


except:
    print("The geoprocessing could not be complete")

try:
    #dbfile = AS.run_dbcamara()
    circuit_list =  AS.get_AllCircuits()
    if circuit_list:
        for circuit_folder in circuit_list:
            circuit = CD.CircuitDir(circuit_folder)
            #AS.write_to_memory_reports(circuit)
            circuit_name= os.path.basename(circuit_folder)
            shiftstoprocessincircuit_list = circuit.getRealizacoesToDo()
            if circuit.start():
                for shift_folder in shiftstoprocessincircuit_list:
                    shift_name = os.path.basename(shift_folder)
                    print("\n\nSTARTED...\nCIRCUIT: {} \nSHIFT: {} ".format(circuit_name,shift_name))
                    shift = ShiftDir(shift_folder,circuit)
                    try:
                        AS.finalize_shift(shift)
                    except Exception as e:
                        print(e)
                        print("The shift was not finalized")
                    else:
                        AS.place_inFilled(shift)
                    print("\n\CLEANED...\nCIRCUIT: {} \nSHIFT: {} ".format(circuit_name,shift_name))
                
        try:
            AS.aggregate_summaries()
        except Exception as e:
            print(e)
            print("The circuit did not have values")
except Exception as e:
    print(e)
    print("The times could not be reported")




######################################################
################## ##################
######################################################




