

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