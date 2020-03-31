import os

class CircuitDir(object):


    CIRCUITJSONDIR = {

        ########Layer 0 #########
        "namestandard": "CircuitName",
        "alias": "aliasCircuitName",
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

    circuitdictionary = {
        "Circuit": 
        {
            "alias":"Circuit",
            "dirpath":"",
            "filesaliasdict":None,
            "Circuit":
                {
                    "alias":"",
                    "dirpath":"",
                    "filesaliasdict":None,
                    "filespaths":"",
                    "CircuitPoints":
                       {
                           "alias":"CircuitPoints",
                           "dirpath":"",
                           "filesaliasdict":{"CircuitPoints":"CircuitPoints.shp"},
                           "filespaths":""
                           },
                    "CircuitArea":
                       {
                           "alias":"CircuitArea",
                           "dirpath":"",
                           "filesaliasdict":{"CircuitArea":"CircuitArea.shp"},
                           "filedicts":{}
                           }
                    },
            "Garage":
                {
                    "alias":"",
                    "dirpath":"",
                    "filedicts":None
                    }
            
            }
        
        }

    circuitdict = {
                  'CircuitPolygons':
                     {'Circuit': {'CircuitPoints': None,'CircuitArea': None},
                      'Garage': None, 'MergedPolygons': None, 'UnLoading': None},
                   'CircuitVoyages':
                      {'ToDo': None, 'DoNe': None}
                  }

    mergedpolygonsdict = {
                  'CircuitAreaBuffered',
                  'AllAreas'
                  }

    voyagedict = {
                 'kml':None,'shp':None,
                 'report_analysis':None,
                 'products':
                    {"CircuitPointsNearLine","ConnectedPointsLine",
                     "MarkedPoints","MergedObject","Points","SplittedLine",
                     "TransitionPoints"}
                 }

    

    def __init__(self, *args, **kwargs):
        print(self.circuitdict)

    pass





class DictionaryExplorer(object):

    def _init_(self):
        #Set the current path as the base folder of all circuits
        self.currentpath_str = ""
    
    def recursive_dictglobalexplorer(self,dir):
        self.currentpath_str = ""
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
            local_dict[realname]['path'] = currentpath_str

            while child_i < children_nr:
                subdir = dir['children'][child_i]
                subdirname = subdir["namestandard"]
                _,partialdict = recursive_dictlocalexplorer(currentpath_str,subdir)
                local_dict[realname][subdirname] = partialdict
                children_nr-=1

            
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

            return currentpath_str,local_dict

        self.dirpath_dict = recursive_dictlocalexplorer(currentpath_str,dir)
        return self.dirpath_dict

