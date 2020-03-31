import os









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










## private class like
class DictionaryExplorer:
         
    def __init__(self,basefolder):
        #Set the current path as the base folder of all circuits
        self.currentpath_str = basefolder
    

    def recursive_dictglobalexplorer(self,dir):
        currentpath_str = self.currentpath_str
        def recursive_dictlocalexplorer(currentpath_str,dir):
            realname = dir['namestandard']
            maskname = dir['alias']
            #initialize the current child number as 0 (there may be no child whatsoever)
            child_i = 0
            #try to get the number of child folders inside the list of dictionaries associated with the key value "children". 
            try:
                children_nr = len(dir['children'])
            #if it is None, a TypeError will be thrown, and the children nr will be 0
            except TypeError:
                children_nr = 0
            #Then, instead of throwing two dictionaries (dirpath_dict and filepath_dict) around throughout the 
            #several calls of recursive_dictlocalexplorer, we will instead have them as instance variables, rather
            #than local variables
            local_dict = {}
            local_dict[realname]={}

            #information that will be used in this directory and child directories
            currentpath_str = os.path.join(currentpath_str,maskname)
            if not os.path.exists(currentpath_str):
                os.mkdir(currentpath_str)
            local_dict[realname]['path'] = currentpath_str
            partialdict = {}
            while child_i < children_nr:
                subdir = dir['children'][child_i]
                _,childdict = recursive_dictlocalexplorer(currentpath_str,subdir)
                partialdict.update(childdict)
                child_i+=1
            local_dict[realname].update(partialdict)
            
            #information in this directory
            if dir['filesystem'] is not None:
                local_dict[realname]['filepathdicts'] = {}
                try:
                     for key_namestandard in dir['filesystem']:
                       filename = dir['filesystem'][key_namestandard]
                       filepath = os.path.join(local_dict[realname]['path'],filename)
                       local_dict[realname]['filepathdicts'][key_namestandard] = filepath
                except:
                     print("The directory structure has errors.")
            else:
                local_dict[realname]['filepathdicts'] = {}
            return currentpath_str,local_dict

        _,self.dirpath_dict = recursive_dictlocalexplorer(currentpath_str,dir)
        return self.dirpath_dict

