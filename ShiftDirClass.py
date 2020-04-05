import os
from DictionaryInstantiator import *
from DirectoryExlorer import *
import toolsgis
from toolsfis import *
import shutil as sh

class ShiftDir(object):

    
    Cartrack = {"SplitSep":'<br></br>',
                "CarTrackTimeFieldName":"Time: ",
                "TimeStampWithoutUTCOffset": (6,25),
                "UTCOffset": (26,28)}

    Mission_Codes_Macro = {
                     "S2P":("G","P"),
                     "P2P":("P","P"),
                     "P2C":("P","C"),
                     "C2C":("C","C"),
                     "C2P":("C","P"),
                     "C2T":("C","G")}


    Mission_Codes_Micro = {
                     "S2P":("G","P"),
                     "P2P":("P","P"),
                     "P2C":("P","C"),
                     "C2C":("C","C"),
                     "C2P":("C","P"),
                     "C2T":("C","G")}
    
    def __init__(self, shiftdirectory, CircuitDirObject ,*args, **kwargs):
            self.processedpolygonspaths = CircuitDirObject.ProcessedPolygon.processedpolygonspaths
            self.circuitobject = CircuitDirObject
            self.zone_classification = CircuitDirObject.zone_classification
            self.zone_abbreviation = {
                    self.zone_classification['GARAGE']:"G",
                    self.zone_classification['CIRCUIT']:"P",
                    self.zone_classification['UNLOADING']:"D",
                    self.zone_classification['CONNECTION']:"L"}
            self.Field_Names_Groupby = {}
            self.shiftdirectory = os.path.abspath(shiftdirectory)
            self.shift = os.path.basename(self.shiftdirectory)
            self.pardir = os.path.abspath(os.path.join(shiftdirectory,os.path.pardir))
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
                  "filesystem": {"Time_Intervals.csv":"Time_Intervals.csv"},
                  "children" : None}

                  ]
           ########END Layer 2 #########
           
        ########END Layer 1 #########
        }
        

        self.Field_Names_Points = {"Delete":["Name","TARGET_FID","Join_Count","Id","ORIG_FID"],
                              "SERIAL_ID":"SERIAL",
                              "SINGLESTRING":"descrp",
                              "TIME":"timestamp",
                              "ZONE": self.zone_classification["CODE_FIELD_NAME"]}

        shiftpathsobject = DictionaryExplorer(self.pardir)
        self.shiftpaths = shiftpathsobject.recursive_dictglobalexplorer(shiftJSONDIR)


        
    @timer
    def process_shift(self):
        self._join_pointswithpolygon()
        self.parse_field()
        self.get_timereports()
  
        
    



    

    @timer
    def get_timereports(self):
        write_brandcsv(self.shiftpaths["ShiftName"]["ReportAnalysis"]["filepathdicts"]["Time_Intervals.csv"],self.Field_Names_Groupby)


    @timer    
    def parse_field(self):
        #assign fieldnames strings to variables
        serial_id = self.Field_Names_Points["SERIAL_ID"]
        singlestring = self.Field_Names_Points["SINGLESTRING"]
        zone = self.Field_Names_Points["ZONE"]
        time = "timestamp"
        field_names = [serial_id,singlestring,time,zone]

        #assign "connection" code to a variable
        ligacao_str = self.zone_classification['CONNECTION']

        #get the two fielpaths to that contains the non parsed points and the parsed poitns
        pointsnotparsedzonegraded = self.shiftpaths["ShiftName"]["Products"]["Points_NotParsed_ZoneGraded"]["filepathdicts"]["Points_NotParsed_ZoneGraded.shp"]
        pointsparsedzonegraded = self.shiftpaths["ShiftName"]["Products"]["Points_Parsed_ZoneGraded"]["filepathdicts"]["Points_Parsed_ZoneGraded.shp"]
        #copy the directory where the non parsed points are
        copy_directory(self.shiftpaths["ShiftName"]["Products"]["Points_NotParsed_ZoneGraded"]["path"],self.shiftpaths["ShiftName"]["Products"]["Points_Parsed_ZoneGraded"]["path"])
        #rename all of the files in the folder (they were copied and need renaming)
        rename_shpfiles(self.shiftpaths["ShiftName"]["Products"]["Points_Parsed_ZoneGraded"]["path"],
                     os.path.splitext(os.path.basename(pointsnotparsedzonegraded))[0],
                     os.path.splitext(os.path.basename(pointsparsedzonegraded))[0])
        
        #get a transitions dictionary of lists. Note that this is defined inside a class method because if it was
        #defined outside a class method bu inside a class body, it would be a class variable and hence if we changed 
        #the instance we were dealing with we would get the same transition lists throughout all of the living objects/instances 
        previous_place = ""


        Field_Names_Groupby = {"INI_SERIAL":[],
                               "FIN_SERIAL":[],
                               "TIME":[],
                               "INTERVAL":[],
                               "ZONE":[previous_place]}

        def update_Field_Names_Groupby(row):
           Field_Names_Groupby["INI_SERIAL"].append(row[field_names.index(serial_id)])
           Field_Names_Groupby["TIME"].append(row[field_names.index(time)])
           Field_Names_Groupby["ZONE"].append(row[field_names.index(zone)])
        

        
        with arcpy.da.UpdateCursor(pointsparsedzonegraded,field_names) as cursor:
           for row in cursor:
              row[field_names.index("timestamp")] = datetime2string(self._Cartrack2Time(row[field_names.index(singlestring)]))
              current_row_int = row[field_names.index(serial_id)]
              current_place = row[field_names.index(zone)]
              row[field_names.index(zone)] = self._replace_emptyspacewithligacao(current_place,ligacao_str)

              if get_place(previous_place,current_place):
                  if previous_place == Field_Names_Groupby["ZONE"][-1]:
                     Field_Names_Groupby["FIN_SERIAL"].append(row[field_names.index(serial_id)]-1)
                  previous_place = current_place
                  update_Field_Names_Groupby(row)
              cursor.updateRow(row)

        Field_Names_Groupby["FIN_SERIAL"].append(row[field_names.index(serial_id)])
        Field_Names_Groupby["FIN_SERIAL"] = Field_Names_Groupby["FIN_SERIAL"][1:]
        Field_Names_Groupby["ZONE"] = Field_Names_Groupby["ZONE"][1:]
        end_time = Field_Names_Groupby["TIME"][1:]
        end_time.append(row[field_names.index("timestamp")])
        start_time = map(string2datetime,Field_Names_Groupby["TIME"])
        end_time = map(string2datetime,end_time)
        start_time_np =  np.array(start_time)
        end_time_np =  np.array(end_time)
        period_time_np = end_time_np - start_time_np
        Field_Names_Groupby["INTERVAL"] = map(tinterval_string,period_time_np) 
        self.Field_Names_Groupby = Field_Names_Groupby


    @signal 
    def _replace_emptyspacewithligacao(self,fieldzone_value,code_value):
            return replace_bymatchorkeep(" ",fieldzone_value, code_value)     


    @signal
    def _Cartrack2Time(self,descriptionstring):
        #These are hardocded values: 4th place in the list, oly after the 6th character
        splitsep_str= self.Cartrack["SplitSep"]
        Cartrackfield_str = self.Cartrack["CarTrackTimeFieldName"] 
        string_list = descriptionstring.split(splitsep_str)
        time_string_1 = [string for string in string_list if Cartrackfield_str in string]
        dtime_string = time_string_1[0][self.Cartrack["TimeStampWithoutUTCOffset"][0]:self.Cartrack["TimeStampWithoutUTCOffset"][1]]

        offset_string = time_string_1[0][self.Cartrack["UTCOffset"][0]:self.Cartrack["UTCOffset"][1]]

        #convert the time offset string to a timedelta object
        offset_obj = datetime.timedelta(hours=int(offset_string))
        datetime_obj = string2datetime(dtime_string)

        #offset the time based on the +00 or +01 part of the string, so as to make times with different offsets comparables
        time_convertible = datetime_obj + offset_obj
        return time_convertible






    @signal
    def _join_pointswithpolygon(self):
        self._copy_mergedppolygon()
        points = self.shiftpaths["ShiftName"]["SHP"]["SHPmerged"]["filepathdicts"]["SHPmerged.shp"]
        polygon = self.shiftpaths["ShiftName"]["Products"]["CircuitPolygon"]["filepathdicts"]["CircuitPolygon.shp"]

        pointsnotparsedzonegraded = self.shiftpaths["ShiftName"]["Products"]["Points_NotParsed_ZoneGraded"]["filepathdicts"]["Points_NotParsed_ZoneGraded.shp"]
        spatialjoin_shpfiles(points,polygon,pointsnotparsedzonegraded)
        deletefieldnames = self.Field_Names_Points["Delete"]
        discard_fieldsInshpfile(pointsnotparsedzonegraded,deletefieldnames)
        add_idfield2shpfile(pointsnotparsedzonegraded,self.Field_Names_Points["SERIAL_ID"])
    


    @signal
    def _copy_mergedppolygon(self):
        self._convert_kml2shp()
        copy_directory(self.processedpolygonspaths["ProcessedPolygonsName"]["SingleObjectBuffered"]["path"],self.shiftpaths["ShiftName"]["Products"]["CircuitPolygon"]["path"])
        old_basename,_ = os.path.splitext(os.path.basename(self.processedpolygonspaths["ProcessedPolygonsName"]["SingleObjectBuffered"]["filepathdicts"]["SingleObjectBuffered.shp"]))
        new_basename,_ = os.path.splitext(os.path.basename(self.shiftpaths["ShiftName"]["Products"]["CircuitPolygon"]["filepathdicts"]["CircuitPolygon.shp"]))
        rename_shpfiles(self.shiftpaths["ShiftName"]["Products"]["CircuitPolygon"]["path"],old_basename,new_basename)

    @signal
    def _convert_kml2shp(self):
        kml_folder = self.shiftpaths["ShiftName"]["KML"]["path"]
        splitshp_folder = self.shiftpaths["ShiftName"]["SHP"]["SHPsplit"]["path"]
        mergedshp_file= self.shiftpaths["ShiftName"]["SHP"]["SHPmerged"]["filepathdicts"]["SHPmerged.shp"]
        convert_kmlfilesinkmlfolder(kml_folder,splitshp_folder)
        merge_shpfilesinshpfolder(splitshp_folder,mergedshp_file)

        

    

    def GenerateResults():
        print("")

