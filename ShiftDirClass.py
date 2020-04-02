import os
from DictionaryInstantiator import *
from DirectoryExlorer import *
import toolsgis
from toolsfis import *
import shutil as sh

class ShiftDir(object):


    def __init__(self, rounddirectory, CircuitDir ,*args, **kwargs):
            self.processedpolygonspaths = CircuitDir.ProcessedPolygon.processedpolygonspaths
            self.circuitobject = CircuitDir
            self.zone_classification = CircuitDir.zone_classification
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
                "alias": "Products",
                "filesystem": None,
                "children" : 
                ########BEGIN Layer 3 #########
                [
                   {
                   "namestandard": "CircuitPolygon",
                   "alias": "CircuitPolygon",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"CircuitPolygon.shp":"nonexistantCircuitPolygon.shp"},
                   "children" : None},

                  {
                   "namestandard": "Points_Parsed_ZoneGraded",
                   "alias": "Points_Parsed_ZoneCoded",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"Points_Parsed_ZoneGraded.shp":"Points_Parsed_ZoneCoded.shp"},
                   "children" : None}, 
                  
                  {
                   "namestandard": "Points_NotParsed_ZoneGraded",
                   "alias": "Points_NotParsed_ZoneCoded",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"Points_NotParsed_ZoneGraded.shp":"Points_NotParsed_ZoneCoded.shp"},
                   "children" : None},

                   {
                   "namestandard": "Transitions",
                   "alias": "Transitions",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"Transitions.csv":"Transitions.csv"},
                   "children" : None},

                   {
                   "namestandard": "Points_Parsed_TransitionGraded",
                   "alias": "Points_Parsed_TransitionCoded",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"Points_Parsed_TransitionGraded.shp":"Points_Parsed_TransitionCoded.shp"},
                   "children" : None},
                  
                  {
                   "namestandard": "Line_Merged_TransitionGraded",
                   "alias": "Line_Merged_TransitionGraded",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"Line_Merged_TransitionGraded.shp":"Line_Merged_TransitionGraded.shp"},
                   "children" : None},

                 
                   {
                   "namestandard": "Line_Splitted_TransitionGraded",
                   "alias": "Line_Splitted_TransitionGraded",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"Line_Splitted_TransitionGraded.shp":"Line_Splitted_TransitionGraded.shp"},
                   "children" : None},
                                                         
                  {
                   "namestandard": "Circuit_Near_Line",
                   "alias": "Circuit_Near_Line",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"Circuit_Near_Line.shp":"Circuit_Near_Line.shp"},
                   "children" : None}]
                   
                ########END Layer 3 #########
                },

               {
                  "namestandard": "KML",
                  "alias": "KML",
                  "filesystem": None,
                  "children" : None},
               {
                  "namestandard": "SHP",
                  "alias": "SHP",
                  "filesystem": None,
                  "children" : [
                      {
                  "namestandard": "SHPsplit",
                  "alias": "SHPsplit",
                  "filesystem": None,
                  "children" : None},
                  {
                  "namestandard": "SHPmerged",
                  "alias": "SHPmerged",
                  "filesystem": {"SHPmerged.shp":"SHPmerged.shp"},
                  "children" : None}
                  ]},

               {
                  "namestandard": "ReportAnalysis",
                  "alias": "ReportAnalysis",
                  "filesystem": None,
                  "children" : None}

                  ]
           ########END Layer 2 #########
           
        ########END Layer 1 #########
        }

        shiftpathsobject = DictionaryExplorer(self.pardir)
        self.shiftpaths = shiftpathsobject.recursive_dictglobalexplorer(shiftJSONDIR)
        
    
        
    

    def join_pointswithpolygon(self):
        self._copy_mergedppolygon()
        points = self.shiftpaths["ShiftName"]["SHP"]["SHPmerged"]["filepathdicts"]["SHPmerged.shp"]
        polygon = self.shiftpaths["ShiftName"]["Products"]["CircuitPolygon"]["filepathdicts"]["CircuitPolygon.shp"]

        pointszonegraded = self.shiftpaths["ShiftName"]["Products"]["Points_NotParsed_ZoneGraded"]["filepathdicts"]["Points_NotParsed_ZoneGraded.shp"]
        spatialjoin_shpfiles(points,polygon,pointszonegraded)
        deletefieldnames = ["Name","TARGET_FID","Join_Count","Id","ORIG_FID"]
        discard_fieldsInshpfile(pointszonegraded,deletefieldnames)
    
    

    def _copy_mergedppolygon(self):
        self._convert_kml2shp()
        copy_directory(self.processedpolygonspaths["ProcessedPolygonsName"]["SingleObjectBuffered"]["path"],self.shiftpaths["ShiftName"]["Products"]["CircuitPolygon"]["path"])
        file_list = getfilesinpath(self.shiftpaths["ShiftName"]["Products"]["CircuitPolygon"]["path"],".shp")
        self.shiftpaths["ShiftName"]["Products"]["CircuitPolygon"]["filepathdicts"]["CircuitPolygon.shp"] = file_list[0]


    def _convert_kml2shp(self):
        kml_folder = self.shiftpaths["ShiftName"]["KML"]["path"]
        splitshp_folder = self.shiftpaths["ShiftName"]["SHP"]["SHPsplit"]["path"]
        mergedshp_file= self.shiftpaths["ShiftName"]["SHP"]["SHPmerged"]["filepathdicts"]["SHPmerged.shp"]
        convert_kmlfilesinkmlfolder(kml_folder,splitshp_folder)
        merge_shpfilesinshpfolder(splitshp_folder,mergedshp_file)
        deletefieldnames= ["Name"]
        discard_fieldsInshpfile(mergedshp_file,deletefieldnames)

        

    

    def GenerateResults():
        print("")

