from DictionaryInstantiator import *
from ostools import *
from DirectoryExlorer import *
from ShiftDirClass import ShiftDir
from db_creator import db_creator
from ostools import *
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
                {"namestandard": "InfoCircuitos",
                "alias": "InfoCircuitos",
                "filesystem": None,
                "children" : None},

                {"namestandard": "InfoTripsFiles",
                "alias": "InfoTripsFiles",
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
        path = self.HandlerPaths['MainDirectory']['Circuits']['path']
        return [os.path.join(path,round) for round in os.listdir(path)]


    def get_AllKmls(self):
        path = self.HandlerPaths['MainDirectory']['Kmls']['path']
        return [os.path.join(path,round) for round in os.listdir(path)]


    def get_AllDatabaseFiles(self):
        path = self.HandlerPaths['MainDirectory']['InfoCircuitos']['path']
        return [os.path.join(path,round) for round in os.listdir(path)]


    @timer
    def retrieve_AllKmls(self):
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


    @timer 
    def run_dbcamara(self):
        databasefiles = getfilesinpath(self.HandlerPaths['MainDirectory']['InfoCircuitos']['path'],".csv")
        dict_csv_dbobject ={}
        for csvfile in databasefiles:
            dict_csv_dbobject[csvfile] = db_creator(csvfile,1000)
        self.dbobject = dict_csv_dbobject[csvfile]
        self.dict_csv_dbobject = dict_csv_dbobject

    
    @timer
    def place_inFilled(self,shift):
        src = shift.shiftpaths['ShiftName']['path']
        dst = shift.circuitobject.circuitpathdicts['CircuitName']["CircuitVoyages"]['Filled']['path']
        copyandremove_directory(src,dst)  


