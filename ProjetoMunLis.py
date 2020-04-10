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


#class MyPrompt(Cmd):
#    prompt = 'pb> '
#    intro = "Welcome! Type ? to list commands"
 
#    def do_exit(self, inp):
#        print("Bye")
#        return True
    
#    def help_exit(self):
#        print('exit the application. Shorthand: x q Ctrl-D.')
 
#    def do_add(self, inp):
#        print("adding '{}'".format(inp))
 
#    def help_add(self):
#        print("Add a new entry to the system.")
 
#    def default(self, inp):
#        if inp == 'x' or inp == 'q':
#            return self.do_exit(inp)
 
#        print("Default: {}".format(inp))
 
#    do_EOF = do_exit
#    help_EOF = help_exit
 

#if __name__ == '__main__':
#    MyPrompt().cmdloop()
#circuit_folder = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01\I0104"
#circuit_object = CD.CircuitDir(circuit_folder)
#circuit_object(False)




#path = input("Path:")
AS = AncientStructural(r"C:\Users\JoaoPedro\Documents\BIGDirectory")
AS.replace_AllKmls()

circuit_folder = r"C:\Users\JoaoPedro\Documents\BIGDirectory\CIRCUITS\I0103"
circuit = CD.CircuitDir(circuit_folder)

cir
realizacao = r"C:\Users\JoaoPedro\Documents\BIGDirectory\CIRCUITS\I0103\aliasCircuitVoyages\aliasDoNe\I0103_V2538_15_01_2020"
shift = ShiftDir(realizacao,circuit)
shift.process_shift()
######################################################
################## ##################
######################################################




