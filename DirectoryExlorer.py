import os
from DictionaryInstantiator import *
from ShiftDirClass import *
from ProcessedPolygonsDirClass import *
from toolsgis import *
import functools

class CircuitDir(object):

    zone_classification = {
                       'GARAGE':'garagem',
                       'CIRCUIT':'recolha',
                       'UNLOADING':'descarga',
                       'CONNECTION':'ligacao',
                       'CODE_FIELD_NAME':'ZONA'}

    def __init__(self, circuitdirectory, *args, **kwargs):
        self.circuitdirectory = os.path.abspath(circuitdirectory)
        self.circuito = os.path.basename(self.circuitdirectory)
        self.pardir = os.path.abspath(os.path.join(circuitdirectory,os.path.pardir))
        self.__setCircuitPaths()
    
    def __setCircuitPaths(self):

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
                "alias": "CircuitData",
                "filesystem": None,
                "children" : 
                ########BEGIN Layer 3 #########
                [
                  
                  {
                   "namestandard": "CircuitPoints",
                   "alias": "CircuitPoints",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"CircuitPoints.shp": self.circuito + ".shp"},
                   "children" : None},

                   
                  {
                   "namestandard": "CircuitArea",
                   "alias": "CircuitArea",
                   "filesystem": {"CircuitArea.shp":"CircuitArea.shp"},
                   "children" : None}
                   ]
                ########END Layer 3 #########
                },

                
               {
                  "namestandard": "Garage",
                  "alias": "Garagem",
                  "filesystem": {"Garage.shp":"Garagem.shp"},
                  "children" : None},
               
               {
                  "namestandard": "CommonPolygons",
                  "alias": "CommonPolygons",
                  "filesystem": None,
                  "children" : None},

                
               {
                  "namestandard": "UnLoading",
                  "alias": "Descarga",
                  "filesystem": {"UnLoading.shp":"Descarga.shp"},
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
        self.__assert_polygonfileexistance()

    

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



    

    
    
        # Merge all of the polygons
    def make_CircuitPolygon(self,bufferdistance):
        #Get all of the important files for producing the polygons
        self.make_CircuitBuffer(bufferdistance)
        AreaBuffered = self.ProcessedPolygon.processedpolygonspaths["ProcessedPolygonsName"]["CircuitAreaBuffered"]["filepathdicts"]["CircuitAreaBuffered.shp"]
        Garage = self.circuitpaths["CircuitName"]['CircuitPolygons']['Garage']['filepathdicts']["Garage.shp"]
        Unloading = self.circuitpaths["CircuitName"]['CircuitPolygons']['UnLoading']['filepathdicts']["UnLoading.shp"]
        
        

        #Merge it with the old ones
        ProcessedCircuitPolygon = self.ProcessedPolygon.processedpolygonspaths["ProcessedPolygonsName"]["SingleObjectBuffered"]["filepathdicts"]["SingleObjectBuffered.shp"]
        merge_polygons([AreaBuffered,Garage,Unloading],ProcessedCircuitPolygon)

    


    
    def make_CircuitBuffer(self,bufferdistance):
        
        self.classify_polygonshpfiles()
        self.bufferdistance = bufferdistance

        CommonPolygons = self.circuitpaths["CircuitName"]['CircuitPolygons']['CommonPolygons']['path']
        Polygons_Dir_Name = "MergedPolygons_" + str(self.bufferdistance)

        Buffered_CircuitArea = os.path.join(CommonPolygons, Polygons_Dir_Name)
        self.ProcessedPolygon = ProcessedPolygonsDir(Buffered_CircuitArea)

        #Create a new buffered Prs Object
        Area = self.circuitpaths["CircuitName"]['CircuitPolygons']['CircuitData']['CircuitArea']['filepathdicts']["CircuitArea.shp"]
        AreaBuffered = self.ProcessedPolygon.processedpolygonspaths["ProcessedPolygonsName"]["CircuitAreaBuffered"]["filepathdicts"]["CircuitAreaBuffered.shp"]
        
        buffer_prsarea(Area,
                       AreaBuffered,
                       self.bufferdistance)
        

    

        #Classify all of the polygons with their respective codes
    def classify_polygonshpfiles(self):

        #Create a Polygon of the Area from the Points with NO buffer
        self.make_CircuitArea()

        #Classify the Circuit Area
        addfieldcode(self.circuitpaths["CircuitName"]['CircuitPolygons']['CircuitData']['CircuitArea']['filepathdicts']["CircuitArea.shp"], 
                     self.zone_classification['CODE_FIELD_NAME'],self.zone_classification['CIRCUIT'])

        #Classify the Garage
        addfieldcode(self.circuitpaths["CircuitName"]['CircuitPolygons']['Garage']['filepathdicts']["Garage.shp"], 
                     self.zone_classification['CODE_FIELD_NAME'],self.zone_classification['GARAGE'])

        #Classify the unloading Polygon
        addfieldcode(self.circuitpaths["CircuitName"]['CircuitPolygons']['UnLoading']['filepathdicts']["UnLoading.shp"], 
                     self.zone_classification['CODE_FIELD_NAME'],self.zone_classification['UNLOADING'])



    def make_CircuitArea(self):
        convert_prspoints2prsarea(self.circuitpaths["CircuitName"]['CircuitPolygons']['CircuitData']['CircuitPoints']['filepathdicts']["CircuitPoints.shp"],
                               self.circuitpaths["CircuitName"]['CircuitPolygons']['CircuitData']['CircuitArea']['filepathdicts']["CircuitArea.shp"])
    
      

    
    def __assert_polygonfileexistance(self):
        Points = self.circuitpaths["CircuitName"]['CircuitPolygons']['CircuitData']['CircuitPoints']['filepathdicts']["CircuitPoints.shp"]
        Garage = self.circuitpaths["CircuitName"]['CircuitPolygons']['Garage']['filepathdicts']["Garage.shp"]
        Unloading = self.circuitpaths["CircuitName"]['CircuitPolygons']['UnLoading']['filepathdicts']["UnLoading.shp"]
        for path in [Points,Garage,Unloading]:
            if not os.path.exists(path):
                print("There is no file:\n",{os.path.basename(path)},
                        "\nat the folder:\n",{os.path.join(path,os.path.pardir)})
            else:
                print("Good to go")



    

    

