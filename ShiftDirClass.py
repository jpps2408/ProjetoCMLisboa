import os
from DictionaryInstantiator import *
from DirectoryExlorer import *
import toolsgis
from toolsfis import *
import shutil as sh

class ShiftDir(object):

    
    Cartrack = {"SplitSep":'<br></br>',
                "CarTrackTimeFieldName":"Time: ",
                "TimeStampWithoutUTCOffset": (6,24),
                "UTCOffset": (26,27)}
    Field_Names_Points = {"Delete":["Name","TARGET_FID","Join_Count","Id","ORIG_FID"],
                          "Incrementing_Int":"SERIAL"}


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
        
    
        
    
    @timer    
    def parse_field(self):

        id_field = self.Field_Names_Points["Incrementing_Int"]
        convoluted_field = "descrp"
        timestamp_field = "timestamp"
        ligacao_str = self.zone_classification['CONNECTION']
        zone_field = self.zone_classification['CODE_FIELD_NAME']

        field_names = [id_field,convoluted_field,timestamp_field,zone_field]

        pointsnotparsedzonegraded = self.shiftpaths["ShiftName"]["Products"]["Points_NotParsed_ZoneGraded"]["filepathdicts"]["Points_NotParsed_ZoneGraded.shp"]
        pointsparsedzonegraded = self.shiftpaths["ShiftName"]["Products"]["Points_Parsed_ZoneGraded"]["filepathdicts"]["Points_Parsed_ZoneGraded.shp"]
        copy_directory(pointsnotparsedzonegraded,pointsparsedzonegraded)

        self.transitions = []
        previous_transition = ""
        with arcpy.da.UpdateCursor(pointsparsedzonegraded,field_names) as cursor:
           for row in cursor:  
              row[field_names.index(zone_field)] = self._replace_emptyspacewithligacao(row[field_names.index(zone_field)],ligacao_str)
              row[field_names.index(timestamp_field)] = self._Cartrack2Time(row[field_names.index(convoluted_field)])
              current_transition = row[field_names.index(zone_field)]
              if self._get_transition(previous_transition,current_transition):
                  previous_transition = current_transition
              cursor.updateRow(row)    
        
    @timer
    def _get_transition(previous_string,current_string):
        if previous_string != previous_string:
            return True
        else:
            return False

    @timer
    def _Cartrack2Time(descriptionstring):
        #These are hardocded values: 4th place in the list, oly after the 6th character
        splitsep_str= self.Cartrack["SplitSep"]
        Cartrackfield_str = self.Cartrack["CarTrackTimeFieldName"] 
        string_list = descriptionstring.split(splitsep)
        time_string_1 = [string for string in string_list if Cartrackfield_str in string]

        dtime_string = time_string_1[0][self.Cartrack["TimeStampWithoutUTCOffset"][0]:self.Cartrack["TimeStampWithoutUTCOffset"][1]]
        offset_string = time_string_1[0][self.Cartrack["UTCOffset"][0]:self.Cartrack["UTCOffset"][1]]

        #convert the time offset string to a timedelta object
        offset_obj = datetime.timedelta(hours=int(offset_string))
        datetime_obj = string2datetime(dtime_string)

        #offset the time based on the +00 or +01 part of the string, so as to make times with different offsets comparables
        time_convertible = datetime_obj + offset_obj
        return time_convertible


    def _replace_emptyspacewithligacao(self,fieldzone_value,code_value):
        return replace_bymatchorkeep(" ",fieldzone_value, code_value)




    def join_pointswithpolygon(self):
        self._copy_mergedppolygon()
        points = self.shiftpaths["ShiftName"]["SHP"]["SHPmerged"]["filepathdicts"]["SHPmerged.shp"]
        polygon = self.shiftpaths["ShiftName"]["Products"]["CircuitPolygon"]["filepathdicts"]["CircuitPolygon.shp"]

        pointsnotparsedzonegraded = self.shiftpaths["ShiftName"]["Products"]["Points_NotParsed_ZoneGraded"]["filepathdicts"]["Points_NotParsed_ZoneGraded.shp"]
        spatialjoin_shpfiles(points,polygon,pointsnotparsedzonegraded)
        deletefieldnames = self.Field_Names_Points["Delete"]
        discard_fieldsInshpfile(pointsnotparsedzonegraded,deletefieldnames)
        add_idfield2shpfile(pointsnotparsedzonegraded,self.Field_Names_Points["Incrementing_Int"])
    



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

        

    

    def GenerateResults():
        print("")

