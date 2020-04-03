import os
from DictionaryInstantiator import *
from DirectoryExlorer import *
import toolsgis
from toolsfis import *
import shutil as sh

class ShiftDir(object):

    
    
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
    
    
    @signal
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
                   "filesystem": {"CircuitPolygon.shp":"CircuitPolygon.shp"},
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

        number_field = self.Field_Names_Points["Incrementing_Int"]
        singlestring_field = "descrp"
        ligacao_str = self.zone_classification['CONNECTION']
        zone_field = self.zone_classification['CODE_FIELD_NAME']

        field_names = [number_field,singlestring_field,"timestamp",zone_field]
        copy_directory(self.shiftpaths["ShiftName"]["Products"]["Points_NotParsed_ZoneGraded"]["path"],self.shiftpaths["ShiftName"]["Products"]["Points_Parsed_ZoneGraded"]["path"])

        pointsnotparsedzonegraded = self.shiftpaths["ShiftName"]["Products"]["Points_NotParsed_ZoneGraded"]["filepathdicts"]["Points_NotParsed_ZoneGraded.shp"]
        pointsparsedzonegraded = self.shiftpaths["ShiftName"]["Products"]["Points_Parsed_ZoneGraded"]["filepathdicts"]["Points_Parsed_ZoneGraded.shp"]

        rename_shpfiles(self.shiftpaths["ShiftName"]["Products"]["Points_Parsed_ZoneGraded"]["path"],
                     os.path.splitext(os.path.basename(pointsnotparsedzonegraded))[0],
                     os.path.splitext(os.path.basename(pointsparsedzonegraded))[0])
        

              
        self.transitions = []
        previous_transition = ""
        with arcpy.da.UpdateCursor(pointsparsedzonegraded,field_names) as cursor:
           for row in cursor:
              prev_row = row
              row[field_names.index("timestamp")] = self._Cartrack2Time(row[field_names.index(singlestring_field)]) 
              current_row_int = row[field_names.index(number_field)]
              current_transition = row[field_names.index(zone_field)]
              row[field_names.index(zone_field)] = self.replace_emptyspacewithligacao(current_transition,ligacao_str)
              if get_transition(previous_transition,current_transition):
                  previous_transition = current_transition
                  self.transitions.append([row[field_names.index("timestamp")],row[field_names.index(zone_field)],row[field_names.index(number_field)]])
              row[field_names.index("timestamp")] = datetime2string(row[field_names.index("timestamp")])
              cursor.updateRow(row)
        print(self.transitions)
     
    @signal 
    def replace_emptyspacewithligacao(fieldzone_value,code_value):
            return replace_bymatchorkeep(" ",fieldzone_value, code_value)     


    @signal
    def _Cartrack2Time(self,descriptionstring):
        Cartrack = {"SplitSep":'<br></br>',
                "CarTrackTimeFieldName":"Time: ",
                "TimeStampWithoutUTCOffset": (6,25),
                "UTCOffset": (26,28)}
        #These are hardocded values: 4th place in the list, oly after the 6th character
        splitsep_str= Cartrack["SplitSep"]
        Cartrackfield_str = Cartrack["CarTrackTimeFieldName"] 
        string_list = descriptionstring.split(splitsep_str)
        time_string_1 = [string for string in string_list if Cartrackfield_str in string]
        dtime_string = time_string_1[0][Cartrack["TimeStampWithoutUTCOffset"][0]:Cartrack["TimeStampWithoutUTCOffset"][1]]

        offset_string = time_string_1[0][Cartrack["UTCOffset"][0]:Cartrack["UTCOffset"][1]]

        #convert the time offset string to a timedelta object
        offset_obj = datetime.timedelta(hours=int(offset_string))
        datetime_obj = string2datetime(dtime_string)

        #offset the time based on the +00 or +01 part of the string, so as to make times with different offsets comparables
        time_convertible = datetime_obj + offset_obj
        return time_convertible






    @signal
    def join_pointswithpolygon(self):
        self._copy_mergedppolygon()
        points = self.shiftpaths["ShiftName"]["SHP"]["SHPmerged"]["filepathdicts"]["SHPmerged.shp"]
        polygon = self.shiftpaths["ShiftName"]["Products"]["CircuitPolygon"]["filepathdicts"]["CircuitPolygon.shp"]

        pointsnotparsedzonegraded = self.shiftpaths["ShiftName"]["Products"]["Points_NotParsed_ZoneGraded"]["filepathdicts"]["Points_NotParsed_ZoneGraded.shp"]
        spatialjoin_shpfiles(points,polygon,pointsnotparsedzonegraded)
        deletefieldnames = self.Field_Names_Points["Delete"]
        discard_fieldsInshpfile(pointsnotparsedzonegraded,deletefieldnames)
        add_idfield2shpfile(pointsnotparsedzonegraded,self.Field_Names_Points["Incrementing_Int"])
    


    @signal
    def _copy_mergedppolygon(self):
        self._convert_kml2shp()
        copy_directory(self.processedpolygonspaths["ProcessedPolygonsName"]["SingleObjectBuffered"]["path"],self.shiftpaths["ShiftName"]["Products"]["CircuitPolygon"]["path"])
        old_basename,_ = os.path.splitext(os.path.basename(self.processedpolygonspaths["ProcessedPolygonsName"]["SingleObjectBuffered"]["filepathdicts"]["SingleObjectBuffered.shp"]))
        new_basename,_ = os.path.splitext(os.path.basename(self.shiftpaths["ShiftName"]["Products"]["CircuitPolygon"]["filepathdicts"]["CircuitPolygon.shp"]))
        rename_files(self.shiftpaths["ShiftName"]["Products"]["CircuitPolygon"]["path"],old_basename,new_basename)

    @signal
    def _convert_kml2shp(self):
        kml_folder = self.shiftpaths["ShiftName"]["KML"]["path"]
        splitshp_folder = self.shiftpaths["ShiftName"]["SHP"]["SHPsplit"]["path"]
        mergedshp_file= self.shiftpaths["ShiftName"]["SHP"]["SHPmerged"]["filepathdicts"]["SHPmerged.shp"]
        convert_kmlfilesinkmlfolder(kml_folder,splitshp_folder)
        merge_shpfilesinshpfolder(splitshp_folder,mergedshp_file)

        

    

    def GenerateResults():
        print("")

