import os
from DictionaryInstantiator import *
from ShiftDirClass import *

import functools
attacheddir
class GluedDir(object):

    
    def __init__(self, glueddirectory, *args, **kwargs):
        self.glueddirectory = os.path.abspath(glueddirectory)
        self.glued = os.path.basename(self.glueddirectory)
        self.pardir = os.path.abspath(os.path.join(glueddirectory,os.path.pardir))
        self.setGluedPaths()
    
    def setGluedPaths(self):

        GLUEDJSONDIR = {
        ########Layer 0 #########
        "namestandard": "GluedName",
        "alias": self.glued,
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

        gluedpathsobject = DictionaryExplorer(self.pardir)
        self.gluedpaths = gluedpathsobject.recursive_dictglobalexplorer(GLUEDJSONDIR)


    
    def make_CircuitBuffer(self,ringdistance):
        Area = self.circuitpaths['CircuitPolygons']['CircuitData']['CircuitArea']['filepathdicts']["CircuitArea.shp"]
        make_CircuitArea(self)
        CommonPolygons = self.circuitpaths['CircuitPolygons']['CommonPolygons']['path']
        CircuitPolygons_Name = "MergedPolygons_" + str(ringdistance)
        Buffered_CircuitArea = os.path.join(CommonPolygons, CircuitPolygons_Name)
        



    



