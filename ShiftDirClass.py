import os
from DictionaryInstantiator import *
import toolsgis
import toolsfis


class ShiftDir(object):


    def __init__(self, rounddirectory, *args, **kwargs):
            self.shiftdirectory = os.path.abspath(rounddirectory)
            self.shift = os.path.basename(self.shiftdirectory)
            self.pardir = os.path.abspath(os.path.join(rounddirectory,os.path.pardir))
            self.setShiftPaths()
    
    def setShiftPaths(self):

        shiftJSONDIR = {
        ########Layer 0 #########
        "namestandard": "ShiftName",
        "alias": self.shift,
        "filesystem": None,
        "children" :
         ########BEGIN Layer 1 #########
        [
            
               {
                "namestandard": "Products",
                "alias": "aliasProducts",
                "filesystem": None,
                "children" : 
                ########BEGIN Layer 3 #########
                [
                   {
                   "namestandard": "CircuitPolygons_Used",
                   "alias": "aliasMergedCircuitPolygons",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"MergedCircuitPolygons.shp":"aliasMergedCircuitPolygons.shp"},
                   "children" : None},

                  {
                   "namestandard": "Points_Parsed",
                   "alias": "aliasParsedPoints",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"ParsedPoints.shp":"aliasParsedPoints.shp"},
                   "children" : None}, 
                  
                  {
                   "namestandard": "Points_Parsed_Local",
                   "alias": "aliasPointsByZone",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"PointsByZone.shp":"aliasPointsByZone.shp"},
                   "children" : None},

                   {
                   "namestandard": "PointsTransition",
                   "alias": "aliasTransitionPoints",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"TransitionPoints.shp":"aliasTransitionPoints.shp"},
                   "children" : None},

                   {
                   "namestandard": "Points_Parsed_Transitioned",
                   "alias": "aliasPointsByZone",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"PointsByZone.shp":"aliasPointsByZone.shp"},
                   "children" : None},
                  
                  {
                   "namestandard": "Line_Default",
                   "alias": "aliasLine_Default",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"Line_Default.shp":"aliasLine_Default.shp"},
                   "children" : None},

                 
                   {
                   "namestandard": "Line_Split",
                   "alias": "aliasLine_Split",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"Line_Split.shp":"aliasLine_Split.shp"},
                   "children" : None},


                  {
                   "namestandard": "Line_Split_Graded",
                   "alias": "aliasLine_Split_Graded",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"Line_Split_Graded.shp":"aliasLine_Split_Graded.shp"},
                   "children" : None},
                                      
                  {
                   "namestandard": "Circuit_Near_Line",
                   "alias": "CircuitPointsNearLinealias",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"CircuitPointsNearLine.shp":"aliasCircuitPointsNearLine.shp"},
                   "children" : None}]
                   
                ########END Layer 3 #########
                },

               {
                  "namestandard": "KML",
                  "alias": "aliasKML",
                  "filesystem": {"SHP.shp":"aliasSHP.shp"},
                  "children" : None},
               {
                  "namestandard": "SHP",
                  "alias": "aliasSHP",
                  "filesystem": {"SHP.shp":"aliasSHP.shp"},
                  "children" : None},
               {
                  "namestandard": "ReportAnalysis",
                  "alias": "CommonPolygons",
                  "filesystem": {"CommonPolygons.shp":"aliasCommonPolygons.shp"},
                  "children" : None}

                  ]
           ########END Layer 2 #########
           
        ########END Layer 1 #########
        }

        shiftpathsobject = DictionaryExplorer(self.pardir)
        self.shiftpaths = shiftpathsobject.recursive_dictglobalexplorer(shiftJSONDIR)
    
    def GenerateResults():
        print("")

