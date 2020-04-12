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
                   "filesystem": {"CircuitPoints.shp":  "CircuitPoints.shp"},
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
                  "filesystem": {"Garage.shp":"Garage.shp"},
                  "children" : None},
               
               {
                  "namestandard": "CommonPolygons",
                  "alias": "CommonPolygons",
                  "filesystem": None,
                  "children" : None},

                
               {
                  "namestandard": "UnLoading",
                  "alias": "Descarga",
                  "filesystem": {"UnLoading.shp":"UnLoading.shp"},
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
                  "alias": "Preparados",
                  "filesystem": None,
                  "children" : None}
                  
             ########END Layer 2 #########
             ,
                 {
                  "namestandard": "ToDo",
                  "alias": "Processados",
                  "filesystem": None,
                  "children" : None}
             ,
                 {
                  "namestandard": "Filled",
                  "alias": "Acabados",
                  "filesystem": None,
                  "children" : None}
                  ]
             ########END Layer 2 #########
             },
             {
             "namestandard": "Reports",
             "alias": "Reports",
             "filesystem": {"Reports.csv":"Reports.csv"},
             "children" : None}
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
    def start(self):
        if self.get_parameters():
            if self._check_CommonPolygonPath():
                print("The Circuit {} had a prepared polygon.".format(os.path.basename(self.circuitdirectory)))
                return True
            elif not self._check_CommonPolygonPath():
                 self.make_CircuitPolygonFromScratch()
                 return True
        else:
            return False





    


    @signal
    def get_parameters(self):
            v1 = self.get_polygon_filenames()
            v2 = self._get_jsontolerances()
            return all([v1,v2])










    def getRealizacoesDoNe(self):
        path = self.circuitpathdicts['CircuitName']['CircuitVoyages']['DoNe']['path']
        return [os.path.join(path,round) for round in os.listdir(path)]

    def getRealizacoesToDo(self):
        path = self.circuitpathdicts['CircuitName']['CircuitVoyages']['ToDo']['path']
        return [os.path.join(path,round) for round in os.listdir(path)]









    
    @signal
    def initialize_circuitparametersifnotexist(self):
        file = self.circuitpathdicts['CircuitName']['filepathdicts']['TOLERANCES.json']
        if not os.path.exists(file):
            save_state2json(self.circuitparameters,file)



    #Get the Polygon Path based on the Circuit Parameters
    def _get_CommonPolygonPath(self):
        bufferdistance = self.circuitparameters["PARAMETRO_CIRCUITO (m)"]
        CommonPolygons = self.circuitpathdicts["CircuitName"]['CircuitPolygons']['CommonPolygons']['path']
        Polygons_Dir_Name = "MergedPolygons_" + str(bufferdistance)
        Buffered_CircuitArea = os.path.join(CommonPolygons, Polygons_Dir_Name)
        self.ProcessedPolygon = ProcessedPolygonsDir(Buffered_CircuitArea)


    
    @signal
    def _check_CommonPolygonPath(self):
        self._get_CommonPolygonPath()
        ProcessedCircuitPolygon = self.ProcessedPolygon.processedpolygonspaths["ProcessedPolygonsName"]["SingleObjectBuffered"]["filepathdicts"]["SingleObjectBuffered.shp"]
        if os.path.exists(ProcessedCircuitPolygon):
            return True
        else:
            return False



        
    @signal
    def _get_jsontolerances(self):
        try:
            file = self.circuitpathdicts['CircuitName']['filepathdicts']['TOLERANCES.json']
            jsontolerances = load_stateOfjson(file)
            self._load_circuitparameters(jsontolerances)
            return True
        except:
            print("TOLERANCES.json of the circuit: {}".format(os.path.basename(self.circuitdirectory)))
            return False


    #Get the polygon filenames
    @signal
    def get_polygon_filenames(self):
        try:
            self.circuitpathdicts["CircuitName"]['CircuitPolygons']['CircuitData']['CircuitPoints']['filepathdicts']["CircuitPoints.shp"] = getfilesinpath(self.circuitpathdicts["CircuitName"]['CircuitPolygons']['CircuitData']['CircuitPoints']['path'],'.shp')[0]

            self.circuitpathdicts["CircuitName"]['CircuitPolygons']['Garage']['filepathdicts']["Garage.shp"] = getfilesinpath(self.circuitpathdicts["CircuitName"]['CircuitPolygons']['Garage']['path'],'.shp')[0]

            self.circuitpathdicts["CircuitName"]['CircuitPolygons']['UnLoading']['filepathdicts']["UnLoading.shp"] = getfilesinpath(self.circuitpathdicts["CircuitName"]['CircuitPolygons']['UnLoading']['path'],'.shp')[0]
            return True

        except:
            print("Polygons of the circuit are not present: {}".format(os.path.basename(self.circuitdirectory)))
            return False


    # Load the Circuit Parameters
    @signal
    def _load_circuitparameters(self,jsontolerances):
        self.circuitparameters["PARAMETRO_VISITADOS (m)"] = int(jsontolerances["PARAMETRO_VISITADOS (m)"])
        self.circuitparameters["PARAMETRO_CIRCUITO (m)"] = int(jsontolerances["PARAMETRO_CIRCUITO (m)"])
        self.circuitdict["CIRCUIT_TOLERANCE"] = self.circuitparameters["PARAMETRO_CIRCUITO (m)"]



        





    def make_CircuitPolygonFromCodedAreas(self):
        self._get_CommonPolygonPath()
        self._make_CircuitBuffer()
        self.make_CircuitPolygon()
        print("Prepared a polygon for circuit {} with parameters: \n\t{}:{} \n\t{}:{}".format(os.path.basename(self.circuitdirectory),
                                                                                                               "PARAMETRO_CIRCUITO (m)",
                                                                                                               self.circuitparameters["PARAMETRO_CIRCUITO (m)"],
                                                                                                               "PARAMETRO_VISITADOS (m)",
                                                                                                               self.circuitparameters["PARAMETRO_VISITADOS (m)"],
                                                                                                               ))


    def make_CircuitPolygonFromScratch(self):
        self._make_CircuitArea()
        print("Created a new Area Polygon From the Circuit Points in circuit {}".format(os.path.basename(self.circuitdirectory)))
        self._classify_polygonshpfiles()
        print("Added Zone Codes to the Area Polygon From the Circuit Points in circuit {}".format(os.path.basename(self.circuitdirectory)))
        self.make_CircuitPolygonFromCodedAreas()



###################################################### GEOPROCESSING begin  ################################################

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
    

        
    ###################################################### GEOPROCESSING end  ################################################

    

