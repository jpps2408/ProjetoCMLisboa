import os
from DictionaryInstantiator import *
from ShiftDirClass import *

class CircuitDir(object):

    
    def __init__(self, circuitdirectory, *args, **kwargs):
        self.circuitdirectory = os.path.abspath(circuitdirectory)
        self.circuito = os.path.basename(self.circuitdirectory)
        self.pardir = os.path.abspath(os.path.join(circuitdirectory,os.path.pardir))
        self.setCircuitPaths()
    
    def setCircuitPaths(self):

        CIRCUITJSONDIR = {
        ########Layer 0 #########
        "namestandard": "CircuitName",
        "alias": self.circuito,
        "filesystem": None,
        "children" :
         ########BEGIN Layer 1 #########
        [
            
            {
             "namestandard": "CircuitPolygons",
             "alias": "aliasCircuitPolygons",
             "filesystem": None,
             "children" : 
              ########BEGIN Layer 2 #########
             [

               {
                "namestandard": "CircuitData",
                "alias": "aliasCircuitData",
                "filesystem": None,
                "children" : 
                ########BEGIN Layer 3 #########
                [
                  
                  {
                   "namestandard": "CircuitPoints",
                   "alias": "aliasCircuitPoints",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"CircuitPoints.shp":"aliasCircuitPoints.shp"},
                   "children" : None},

                   
                  {
                   "namestandard": "CircuitArea",
                   "alias": "CircuitArea",
                   "filesystem": {"CircuitArea.shp":"aliasCircuitArea.shp"},
                   "children" : None}
                   ]
                ########END Layer 3 #########
                },

                
               {
                  "namestandard": "Garage",
                  "alias": "Garage",
                  "filesystem": {"Garage.shp":"aliasGarage.shp"},
                  "children" : None},
               
               {
                  "namestandard": "CommonPolygons",
                  "alias": "CommonPolygons",
                  "filesystem": {"CommonPolygons.shp":"aliasCommonPolygons.shp"},
                  "children" : None},

                
               {
                  "namestandard": "UnLoading",
                  "alias": "UnLoading",
                  "filesystem": {"UnLoading.shp":"aliasUnLoading.shp"},
                  "children" : None}
                  
                  ]
           ########END Layer 2 #########
           },

            {
             "namestandard": "CircuitVoyages",
             "alias": "aliasCircuitVoyages",
             "filesystem": None,
             "children" :
             ########BEGIN Layer 2 #########
             [
                 
                 {
                  "namestandard": "ToDo",
                  "alias": "aliasToDo",
                  "filesystem": None,
                  "children" : None},
                 
                 {
                  "namestandard": "DoNe",
                  "alias": "aliasDoNe",
                  "filesystem": None,
                  "children" : None}
                  ]
             ########END Layer 2 #########
             }
           ]
        ########END Layer 1 #########
        }

        circuitpathsobject = DictionaryExplorer(self.pardir)
        self.circuitpaths = circuitpathsobject.recursive_dictglobalexplorer(CIRCUITJSONDIR)
    
    def getRealizacoesToDo(self):
        path = self.circuitpaths['CircuitName']['CircuitVoyages']['ToDo']['path']
        return [os.path.join(path,round) for round in os.listdir(path)]

    def getRealizacoesDoNe(self):
        path = self.circuitpaths['CircuitName']['CircuitVoyages']['DoNe']['path']
        return [os.path.join(path,round) for round in os.listdir(path)]

    def ProcessRealizacoesToDo():
        roundlist = getRealizacoesToDo()
        for shift in roundlist:
            Shift = ShiftDir(shift)
            Shift.GenerateResults()

    def ProcessRealizacoesDoNe(self):
        roundlist = getRealizacoesDoNe()
        for shift in roundlist:
            Shift = ShiftDir(shift)
            Shift.GenerateResults()


