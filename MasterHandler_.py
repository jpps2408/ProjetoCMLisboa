from DictionaryInstantiator import *
from ostools import *


class MasterHandler(object):


    def __init__(self,masterdirectory,*args,**kwargs):
        self.masterdirectory = os.path.abspath(masterdirectory)
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



