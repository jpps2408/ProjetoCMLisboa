import os
from DictionaryInstantiator import *
from ShiftDirClass import *

import functools
#processedpolygons

class ProcessedPolygonsDir(object):

    
    def __init__(self, processedpolygonsdirectory, *args, **kwargs):
        self.processedpolygonsdirectory = os.path.abspath(processedpolygonsdirectory)
        self.processedpolygons = os.path.basename(self.processedpolygonsdirectory)
        self.pardir = os.path.abspath(os.path.join(processedpolygonsdirectory,os.path.pardir))
        self.setGluedPaths()
    
    def setGluedPaths(self):

        PROCESSEDPOLYGONSJSONDIR = {
        ########Layer 0 #########
        "namestandard": "ProcessedPolygonsName",
        "alias": self.processedpolygons,
        "filesystem": None,
        "children" :
         ########BEGIN Layer 1 #########
        [
            
            {
             "namestandard": "CircuitAreaBuffered",
             "alias": "aliasCircuitAreaBuffered",
             "filesystem": {"CircuitAreaBuffered.shp":"aliasCircuitAreaBuffered.shp"},
             "children" : None},
                
            {
               "namestandard": "SingleObjectBuffered",
                "alias": "aliasSingleObjectBuffered",
                "filesystem": {"SingleObjectBuffered.shp":"aliasSingleObjectBuffered.shp"},
                "children" : None}
           ]
        ########END Layer 1 #########
        }

        processedpolygonspathsobject = DictionaryExplorer(self.pardir)
        self.processedpolygonspaths = processedpolygonspathsobject.recursive_dictglobalexplorer(PROCESSEDPOLYGONSJSONDIR)



        



    



