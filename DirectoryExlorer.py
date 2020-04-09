import os
from DictionaryInstantiator import *
from ShiftDirClass import *
from ProcessedPolygonsDirClass import *
from toolsgis import *
import functools

class CircuitDir(object):


    def __init__(self, circuitdirectory, *args, **kwargs):
        self.circuitdirectory = os.path.abspath(circuitdirectory)
        self.pardir = os.path.abspath(os.path.join(circuitdirectory,os.path.pardir))
        self.setcircuitpathdicts()
        self._make_circuitinfo()
    

    def setcircuitpathdicts(self):

        CIRCUITJSONDIR = {
        ########Layer 0 #########
        "namestandard": "CircuitName",
        "alias": os.path.basename(self.circuitdirectory),
        "filesystem": {"TOLERANCES.json":"TOLERANCIAS.json"},
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
                   "filesystem": {"CircuitPoints.shp":  os.path.basename(self.circuitdirectory) + ".shp"},
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
        self.circuitpathdicts = circuitpathsobject.recursive_dictglobalexplorer(CIRCUITJSONDIR)


    def _make_circuitinfo(self):


        self.zone_classification = {
                           'GARAGE':'garagem',
                           'CIRCUIT':'recolha',
                           'UNLOADING':'descarga',
                           'CONNECTION':'ligacao',
                           'CODE_FIELD_NAME':'ZONA'}


        self.circuitdict = {"CIRCUIT_ID":os.path.basename(self.circuitdirectory),
                            "CIRCUIT_TOLERANCE":None}


        self.circuitstate = {"CreationFinished":None,
                             "TimeOfCreation":None,
                             "CIRCUIT_TOLERANCE":None}


        self.circuitparameters = {"PARAMETRO_CIRCUITO (m)":None,
                                  "PARAMETRO_VISITADOS (m)":None}

        self.initialize_circuitparametersifnotexist()


    
    @signal
    def __call__(self, override = False):
         if self.runnable():
            self._get_CommonPolygonPath()
            self.load_circuitparameters()
            if override:
                 try:
                     self.make_CircuitPolygonFromCodedAreas()
                 except:
                     self.make_CircuitPolygonFromScratch()
            elif self._check_CommonPolygonPath():
                print("The Circuit is ready")





    def getRealizacoesDoNe(self):
        path = self.circuitpathdicts['CircuitName']['CircuitVoyages']['DoNe']['path']
        return [os.path.join(path,round) for round in os.listdir(path)]





    @signal
    def runnable(self):
         return all([self._check_polygonfileexistance(),self._check_validjsontolerances()])

    
    @signal
    def _check_validjsontolerances(self):
        file = self.circuitpathdicts['CircuitName']['filepathdicts']['TOLERANCES.json']
        if os.path.exists(file):
            jsontolerances = load_stateOfjson(file)
            allintegervalues = [type(jsontolerances[key]) is int for key in jsontolerances.keys()]
            if all(allintegervalues):
                return True
            else:
                return False
        else:
            return False






    @signal
    def load_circuitparameters(self,file):
        jsontolerances = load_stateOfjson(file)
        self.circuitparameters["PARAMETRO_VISITADOS (m)"] = int(jsontolerances["PARAMETRO_VISITADOS (m)"])
        self.circuitparameters["PARAMETRO_CIRCUITO (m)"] = int(jsontolerances["PARAMETRO_CIRCUITO (m)"])
        self.circuitdict["CIRCUIT_TOLERANCE"] = bufferdistance


    @signal
    def initialize_circuitparametersifnotexist(self):
        file = self.circuitpathdicts['CircuitName']['filepathdicts']['TOLERANCES.json']
        if not os.path.exists(file):
            save_state2json(self.circuitparameters,file)







    
    @signal
    def _check_CommonPolygonPath(self):
        self._get_CommonPolygonPath()
        ProcessedCircuitPolygon = self.ProcessedPolygon.processedpolygonspaths["ProcessedPolygonsName"]["SingleObjectBuffered"]["filepathdicts"]["SingleObjectBuffered.shp"]
        if os.path.exists(ProcessedCircuitPolygon):
            return True
        else:
            return False

        
    @signal
    def _check_polygonfileexistance(self):
        Points = self.circuitpathdicts["CircuitName"]['CircuitPolygons']['CircuitData']['CircuitPoints']['filepathdicts']["CircuitPoints.shp"]
        Garage = self.circuitpathdicts["CircuitName"]['CircuitPolygons']['Garage']['filepathdicts']["Garage.shp"]
        Unloading = self.circuitpathdicts["CircuitName"]['CircuitPolygons']['UnLoading']['filepathdicts']["UnLoading.shp"]

        for path in [Points,Garage,Unloading]:
            if not os.path.exists(path):
                print("There is no file:\n {} \nat the folder:\n {}".format(os.path.basename(path),os.path.join(path,os.path.pardir)))
                return False
        return True

    






    def _get_CommonPolygonPath(self):
        bufferdistance = self.circuitparameters["PARAMETRO_CIRCUITO (m)"]
        CommonPolygons = self.circuitpathdicts["CircuitName"]['CircuitPolygons']['CommonPolygons']['path']
        Polygons_Dir_Name = "MergedPolygons_" + str(bufferdistance)
        Buffered_CircuitArea = os.path.join(CommonPolygons, Polygons_Dir_Name)
        self.ProcessedPolygon = ProcessedPolygonsDir(Buffered_CircuitArea)

    






    def make_CircuitPolygonFromCodedAreas(self):
        self._get_CommonPolygonPath()
        self._make_CircuitBuffer()
        self.make_CircuitPolygon()


    def make_CircuitPolygonFromScratch(self):
        self._make_CircuitArea()
        self._classify_polygonshpfiles()
        self.make_CircuitPolygonFromCodedAreas()

        





    @signal    # Merge all of the polygons
    def make_CircuitPolygon(self):
        #Get all of the important files for producing the polygons
        AreaBuffered = self.ProcessedPolygon.processedpolygonspaths["ProcessedPolygonsName"]["CircuitAreaBuffered"]["filepathdicts"]["CircuitAreaBuffered.shp"]
        Garage = self.circuitpathdicts["CircuitName"]['CircuitPolygons']['Garage']['filepathdicts']["Garage.shp"]
        Unloading = self.circuitpathdicts["CircuitName"]['CircuitPolygons']['UnLoading']['filepathdicts']["UnLoading.shp"]
        ProcessedCircuitPolygon = self.ProcessedPolygon.processedpolygonspaths["ProcessedPolygonsName"]["SingleObjectBuffered"]["filepathdicts"]["SingleObjectBuffered.shp"]
        #Merge it with the old ones
        
        merge_polygons([AreaBuffered,
                        Garage,
                        Unloading],
                        ProcessedCircuitPolygon)


    @signal
    def _make_CircuitBuffer(self):
        #Create a new buffered Prs Object
        Area = self.circuitpathdicts["CircuitName"]['CircuitPolygons']['CircuitData']['CircuitArea']['filepathdicts']["CircuitArea.shp"]
        AreaBuffered = self.ProcessedPolygon.processedpolygonspaths["ProcessedPolygonsName"]["CircuitAreaBuffered"]["filepathdicts"]["CircuitAreaBuffered.shp"]
        
        buffer_prsarea(Area,
                       AreaBuffered,
                       self.circuitparameters["PARAMETRO_CIRCUITO (m)"])


    @signal    #Classify all of the polygons with their respective codes
    def _classify_polygonshpfiles(self):

        #Classify the Circuit Area
        addfieldcode(self.circuitpathdicts["CircuitName"]['CircuitPolygons']['CircuitData']['CircuitArea']['filepathdicts']["CircuitArea.shp"], 
                     self.zone_classification['CODE_FIELD_NAME'],
                     self.zone_classification['CIRCUIT'])

        #Classify the Garage
        addfieldcode(self.circuitpathdicts["CircuitName"]['CircuitPolygons']['Garage']['filepathdicts']["Garage.shp"], 
                     self.zone_classification['CODE_FIELD_NAME'],
                     self.zone_classification['GARAGE'])

        #Classify the unloading Polygon
        addfieldcode(self.circuitpathdicts["CircuitName"]['CircuitPolygons']['UnLoading']['filepathdicts']["UnLoading.shp"], 
                     self.zone_classification['CODE_FIELD_NAME'],
                     self.zone_classification['UNLOADING'])



    #Create a Polygon of the Area from the Points with NO buffer
    @signal
    def _make_CircuitArea(self):
        convert_prspoints2prsarea(self.circuitpathdicts["CircuitName"]['CircuitPolygons']['CircuitData']['CircuitPoints']['filepathdicts']["CircuitPoints.shp"],
                               self.circuitpathdicts["CircuitName"]['CircuitPolygons']['CircuitData']['CircuitArea']['filepathdicts']["CircuitArea.shp"])
    

        
    

    

