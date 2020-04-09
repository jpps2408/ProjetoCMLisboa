from DictionaryInstantiator import *
from ostools import *
from DirectoryExlorer import *
from ShiftDirClass import ShiftDir

class AncientStructural(object):


    def __init__(self,masterdirectory,*args,**kwargs):
        self.masterdirectory = os.path.abspath(masterdirectory)
        self.pardir = os.path.join(masterdirectory,os.pardir)
        self.setHandlerPaths()


    def setHandlerPaths(self):
        MASTERJSONDIR = {
        ########Layer 0 #########
        "namestandard": "MainDirectory",
        "alias": os.path.basename(self.masterdirectory),
        "filesystem": {"Reports.csv":"RELATORIO.csv","ancilliarydata.json":"infotrips.json"},
        "children" :
         ########BEGIN Layer 1 #########
        [
                {"namestandard": "InfoTripsFiles",
                "alias": "InfoCircuitos",
                "filesystem": None,
                "children" : None},

                {"namestandard": "Kmls",
                "alias": "PERCURSOS",
                "filesystem": None,
                "children" : None},

               {"namestandard": "Circuits",
                "alias": "CIRCUITS",
                "filesystem": None,
                "children" : None}]
        }
        
        HandlerPathsobject = DictionaryExplorer(self.pardir)
        self.HandlerPaths = HandlerPathsobject.recursive_dictglobalexplorer(MASTERJSONDIR)


    def get_AllCircuits(self):
        path = self.HandlerPaths['MainDirectory']['CIRCUITS']['path']
        return [os.path.join(path,round) for round in os.listdir(path)]


    def get_AllKmls(self):
        path = self.HandlerPaths['MainDirectory']['Kmls']['path']
        return [os.path.join(path,round) for round in os.listdir(path)]


    def get_AllDatabaseFiles(self):
        path = self.HandlerPaths['MainDirectory']['BaseFiles']['path']
        return [os.path.join(path,round) for round in os.listdir(path)]


    @timer
    def replace_AllKmls(self):
        #create a dictionary to hold ShiftDir Objects
        shiftdir_dict ={}
        paths = self.get_AllKmls()
        for origfile in paths:
            shiftpart,_ = os.path.splitext(os.path.basename(origfile))
            splitstringlist = shiftpart.split("_")
            circuitpath= os.path.join(self.HandlerPaths['MainDirectory']['Circuits']['path'],splitstringlist[0])
            if not circuitpath in shiftdir_dict.keys():
                circuithandler = CircuitDir(circuitpath)
                shiftdir_dict[circuitpath] = circuithandler
            circuitdir_inst = shiftdir_dict[circuitpath]
            shiftpardir = circuitdir_inst.circuitpathdicts["CircuitName"]["CircuitVoyages"]["DoNe"]["path"]
            if len(splitstringlist)>5:
                shiftfull = "_".join(splitstringlist[0:5])
            else:
                shiftfull = shiftpart
            shiftpath = os.path.join(shiftpardir,shiftfull)
            if not shiftpath in shiftdir_dict.keys():
                shifthandler = ShiftDir(shiftpath,circuithandler)
                shiftdir_dict[shiftpath] = shifthandler
            shiftdir_inst = shiftdir_dict[shiftpath] 
            movedfile = os.path.join(shiftdir_inst.shiftpaths["ShiftName"]["KML"]["path"],shiftpart + _)
            os.rename(origfile,movedfile)


    
    

