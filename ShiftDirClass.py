import os
from DictionaryInstantiator import *
from DirectoryExlorer import *
from toolsgis import *
from toolsfis import *
import numpy as np
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

            self.create_metrics_dicts()
            self.processedpolygonspaths = CircuitDirObject.ProcessedPolygon.processedpolygonspaths
            self.circuitobject = CircuitDirObject
            self.zone_abbreviation = {
                    self.circuitobject.zone_classification['GARAGE']:"G",
                    self.circuitobject.zone_classification['CIRCUIT']:"R",
                    self.circuitobject.zone_classification['UNLOADING']:"C",
                    self.circuitobject.zone_classification['CONNECTION']:"L"}
            self.Field_Names_Groupby = {}
            self.shiftdirectory = os.path.abspath(shiftdirectory)
            self.pardir = os.path.abspath(os.path.join(shiftdirectory,os.path.pardir))
            self.Fields_Numbers["CIRCUIT"] = CircuitDirObject.circuito
            self.Fields_Numbers["SHIFT"] = os.path.basename(self.shiftdirectory)
            self.setShiftPaths()

    
    
    @signal
    def setShiftPaths(self):

        shiftJSONDIR = {
        ########Layer 0 #########
        "namestandard": "ShiftName",
        "alias": self.Fields_Numbers["SHIFT"],
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
                   "namestandard": "Circuit_Polygon_Original",
                   "alias": "Circuit_Polygon_Original",
                   #"filesystem": {"namestandard.shp":"alias.shp","namestandard2.shp":"alias2.shp",...}
                   "filesystem": {"Circuit_Polygon_Original.shp":"Circuit_Polygon_Original.shp"},
                   "children" : None},

                  {
                   "namestandard": "Points_Parsed_Zone",
                   "alias": "Points_Parsed_Zone",
                   "filesystem": {"Points_Parsed_Zone.shp":"Points_Parsed_Zone.shp"},
                   "children" : None}, 
                  
                  {
                   "namestandard": "Points_NotParsed_Zone",
                   "alias": "Points_NotParsed_Zone",
                   "filesystem": {"Points_NotParsed_Zone.shp":"Points_NotParsed_Zone.shp"},
                   "children" : None},

                    {
                   "namestandard": "Line_Tranche",
                   "alias": "Line_Tranche",
                   "filesystem": {"Line_Tranche.shp":"Line_Tranche.shp"},
                   "children" : None},
                   
                    {
                   "namestandard": "Line_Sole",
                   "alias": "Line_Sole",
                   "filesystem": {"Line_Sole.shp":"Line_Sole.shp"},
                   "children" : None},
                                     
                    {
                   "namestandard": "Line_Tranche_Code",
                   "alias": "Line_Tranche_Code",
                   "filesystem": {"Line_Tranche_Code.shp":"Line_Tranche_Code.shp"},
                   "children" : None},

                   {
                   "namestandard": "Line_Buffered",
                   "alias": "Line_Buffered",
                   "filesystem": {"Line_Buffered.shp":"Line_Buffered.shp"},
                   "children" : None},

                    {
                   "namestandard": "Circuit_Stops_Original",
                   "alias": "Circuit_Stops_Original",
                   "filesystem": {"Circuit_Stops_Original.shp":"Circuit_Stops_Original.shp"},
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
                  "filesystem": {"Time_History.csv":"Time_History.csv","Appendable.csv":"Appendable.csv"},
                  "children" : None}

                  ]
           ########END Layer 2 #########
           
        ########END Layer 1 #########
        }
        
        shiftpathsobject = DictionaryExplorer(self.pardir)
        self.shiftpaths = shiftpathsobject.recursive_dictglobalexplorer(shiftJSONDIR)

        self.Fields_Table_Parsed = {"Delete":["Name","TARGET_FID","Join_Count","Id","ORIG_FID"],
                              "SERIAL_ID":"SERIAL",
                              "SINGLESTRING":"descrp",
                              "TIME":"timestamp",
                              "ZONE": self.circuitobject.zone_classification["CODE_FIELD_NAME"],
                              "BLOCK_ID":"BLOCK_ID"}






    
    def create_metrics_dicts(self):
        
        self.Fields_Display={"CIRCUIT":"CIRCUITO",
                             "SHIFT":"PERCURSO",
                             "START_TIME":"H_INICIO",
                             "END_TIME":"H_FIM",
                             "CIRCUIT_TOLERANCE":"PARAMETRO_CIRCUITO",
                             "VISITED_TOLERANCE":"PARAMETRO_VISITADOS",
                             "ABSOLUTE_VISITED_STOPS":"NR_VISITADOS",
                             "RELATIVE_VISITED_STOPS":"%_VISITADOS",
                             "ABSOLUTE_IGNORED_STOPS":"NR_IGNORADOS",
                             "RELATIVE_IGNORED_STOPS":"%_IGNORADOS",
                             "GARAGE_TIME":"TEMP_GARAGEM",
                             "GARAGE_DIST":"DIST_GARAGEM",
                             "UNLOADING_TIME":"TEMP_DESCARGA",
                             "UNLOADING_DIST":"DIST_DESCARGA",
                             "CIRCUIT_TIME":"TEMP_RECOLHA",
                             "CIRCUIT_DIST":"DIST_RECOLHA",
                             "CONNECTION_TIME":"TEMP_LIGACAO",
                             "CONNECTION_DIST":"DIST_LIGACAO",
                             "OTHERS_TIME":"TEMP_OUTROS",
                             "OTHERS_DIST":"DIST_OUTROS"}

        self.Fields_Numbers={"CIRCUIT":None,
                    "SHIFT":None,
                    "START_TIME":None,
                    "END_TIME":None,
                    "CIRCUIT_TOLERANCE":None,
                    "VISITED_TOLERANCE":None,
                    "ABSOLUTE_VISITED_STOPS":None,
                    "RELATIVE_VISITED_STOPS":None,
                    "ABSOLUTE_IGNORED_STOPS":None,
                    "RELATIVE_IGNORED_STOPS":None,
                    "GARAGE_TIME":None,
                    "GARAGE_DIST":None,
                    "UNLOADING_TIME":None,
                    "UNLOADING_DIST":None,
                    "CIRCUIT_TIME":None,
                    "CIRCUIT_DIST":None,
                    "CONNECTION_TIME":None,
                    "CONNECTION_DIST":None,
                    "OTHERS_TIME":None,
                    "OTHERS_DIST":None}

        

    @timer
    def process_shift(self,buffersize):
        self._join_pointswithpolygon()
        self.parse_field()
        self.create_singlelinewithpoints()
        self._get_near_count(buffersize)
        self.get_reports()
        self.generate_reports()
        
    


    @timer
    def generate_reports(self):
        
        order =["CIRCUIT","SHIFT","START_TIME","END_TIME","CIRCUIT_TOLERANCE","VISITED_TOLERANCE",
                "ABSOLUTE_VISITED_STOPS", "RELATIVE_VISITED_STOPS","ABSOLUTE_IGNORED_STOPS",
                "RELATIVE_IGNORED_STOPS","GARAGE_TIME","GARAGE_DIST","UNLOADING_TIME",
                "UNLOADING_DIST","CIRCUIT_TIME","CIRCUIT_DIST","CONNECTION_TIME",
                "CONNECTION_DIST","OTHERS_TIME","OTHERS_DIST"]
        Columns = [self.Fields_Display[key] for key in order]
        Row = [self.Fields_Numbers[key] for key in order]

        f = pd.DataFrame([Row], columns=Columns)
        f.to_csv(self.shiftpaths["ShiftName"]["ReportAnalysis"]["filepathdicts"]["Appendable.csv"],sep=';')


    @timer
    def get_reports(self):
        self._get_abrupts_reports()


    @timer
    def _get_near_count(self,buffersize):
        self._join_linewithstaticstops(buffersize)
        near_shpfile = self.shiftpaths['ShiftName']['Products']['Circuit_Stops_Original']['filepathdicts']['Circuit_Stops_Original.shp']
        join_count = "Join_Count"
        field_names = [join_count]
        with arcpy.da.UpdateCursor(near_shpfile,field_names) as cursor:
           total_point_count = 0
           ignored_point_count = 0
           for row in cursor:
               if row[field_names.index(join_count)]==0:
                   ignored_point_count+=1
               total_point_count+=1
        visited_point_count = total_point_count - ignored_point_count
        visited_point_ratio = round(100*(visited_point_count/float(total_point_count)),2)
        ignored_point_ratio = round(100*(ignored_point_count/float(total_point_count)),2)

        self.Fields_Numbers["ABSOLUTE_VISITED_STOPS"] = visited_point_count
        self.Fields_Numbers["RELATIVE_VISITED_STOPS"] = visited_point_ratio
        self.Fields_Numbers["ABSOLUTE_IGNORED_STOPS"] = ignored_point_count
        self.Fields_Numbers["RELATIVE_IGNORED_STOPS"] = ignored_point_ratio
       
        
           
    @timer 
    def _join_linewithstaticstops(self,buffersize):
        line_sole = self.shiftpaths['ShiftName']['Products']['Line_Sole']['filepathdicts']['Line_Sole.shp']
        line_buffered = self.shiftpaths['ShiftName']['Products']['Line_Buffered']['filepathdicts']['Line_Buffered.shp']
        prs_shpfile = self.circuitobject.circuitpaths["CircuitName"]['CircuitPolygons']['CircuitData']['CircuitPoints']['filepathdicts']["CircuitPoints.shp"]
        near_shpfile = self.shiftpaths['ShiftName']['Products']['Circuit_Stops_Original']['filepathdicts']['Circuit_Stops_Original.shp']
        buffer_shpfiles(line_sole,line_buffered,buffersize)
        spatialjoin_shpfiles(prs_shpfile,line_buffered,near_shpfile)


    @timer
    def _get_abrupts_reports(self):
        df = pd.DataFrame(self.Field_Names_Groupby)
        fieldnames=["INI_SERIAL","FIN_SERIAL","BLOCK_ID","TIME","ZONE","INTERVAL","HOURS","DISPLACEMENT"]
        df = df[fieldnames]
        df.to_csv(self.shiftpaths["ShiftName"]["ReportAnalysis"]["filepathdicts"]["Time_History.csv"],sep=';')


    

    @timer
    def create_singlelinewithpoints(self):
        line_sole = self.shiftpaths['ShiftName']['Products']['Line_Sole']['filepathdicts']['Line_Sole.shp']
        line_part_uncoded = self.shiftpaths['ShiftName']['Products']['Line_Tranche']['filepathdicts']['Line_Tranche.shp']
        points = self.shiftpaths['ShiftName']['Products']['Points_Parsed_Zone']['filepathdicts']['Points_Parsed_Zone.shp']
        line_part_coded = self.shiftpaths['ShiftName']['Products']['Line_Tranche_Code']['filepathdicts']['Line_Tranche_Code.shp']

        convert_points2line(points,line_sole)
        split_linein2pairs(line_sole,line_part_uncoded)
        spatialjoin_shpfiles(line_part_uncoded,points,line_part_coded)
        add_attribute2shpfile(line_part_coded)

        blockid_array,length_array = self._get_gpdindexvalues(line_part_coded,self.Fields_Table_Parsed["BLOCK_ID"],'LENGTH')           
        length_array = self._fill_length_distwithzeros(self.Field_Names_Groupby["BLOCK_ID"],blockid_array,length_array)
        self.Field_Names_Groupby["DISPLACEMENT"] = length_array


    @timer
    def _fill_length_distwithzeros(self,blockid_time,blockid_dist,length_dist):
        differentblocks = set(blockid_time)-set(blockid_dist)
        for index in sorted(differentblocks):
            np.insert(length_dist,index,float(0))
        return length_dist
        

    @timer   
    def _get_gpdindexvalues(self,shpfile,groupfieldname,sumfieldname):
        pd_all = gpd.read_file(shpfile)
        pd_index_values = pd_all[[sumfieldname,groupfieldname]].groupby([groupfieldname])[sumfieldname].sum()
        pd_index = pd_index_values.index.values
        pd_values = pd_index_values.values
        return pd_index,pd_values

    


    @timer    
    def parse_field(self):
        #assign fieldnames strings to variables
        serial_id = self.Fields_Table_Parsed["SERIAL_ID"]
        singlestring = self.Fields_Table_Parsed["SINGLESTRING"]
        zone = self.Fields_Table_Parsed["ZONE"]
        time = "timestamp"
        block_id = self.Fields_Table_Parsed["BLOCK_ID"]
        field_names = [serial_id,singlestring,time,zone,block_id]

        #assign "connection" code to a variable
        ligacao_str = self.circuitobject.zone_classification['CONNECTION']

        #get the two fielpaths to that contains the non parsed points and the parsed poitns
        pointsnotparsedzonegraded = self.shiftpaths["ShiftName"]["Products"]["Points_NotParsed_Zone"]["filepathdicts"]["Points_NotParsed_Zone.shp"]
        pointsparsedzonegraded = self.shiftpaths["ShiftName"]["Products"]["Points_Parsed_Zone"]["filepathdicts"]["Points_Parsed_Zone.shp"]
        #copy the directory where the non parsed points are
        copy_directory(self.shiftpaths["ShiftName"]["Products"]["Points_NotParsed_Zone"]["path"],self.shiftpaths["ShiftName"]["Products"]["Points_Parsed_Zone"]["path"])
        #rename all of the files in the folder (they were copied and need renaming)
        rename_shpfiles(self.shiftpaths["ShiftName"]["Products"]["Points_Parsed_Zone"]["path"],
                     os.path.splitext(os.path.basename(pointsnotparsedzonegraded))[0],
                     os.path.splitext(os.path.basename(pointsparsedzonegraded))[0])
        
        add_longattribute2shpfile(pointsparsedzonegraded,block_id)
        #get a transitions dictionary of lists. Note that this is defined inside a class method because if it was
        #defined outside a class method bu inside a class body, it would be a class variable and hence if we changed 
        #the instance we were dealing with we would get the same transition lists throughout all of the living objects/instances 
        previous_place = ""

        #Create the fieldnames that completely describe a circuit, by blocks of chronologically contiguous points that have the same classification
        Field_Names_Groupby = {"INI_SERIAL":np.array([]),
                               "FIN_SERIAL":np.array([]),
                               "TIME":np.array([]),
                               "INTERVAL":np.array([]),
                               "HOURS":np.array([]),
                               "ZONE":np.array([previous_place]), 
                               "BLOCK_ID":np.array([]),
                               "DISPLACEMENT":np.array([])}
        
        #Update the Field Names with the row contents in order to 
        def update_Field_Names_Groupby(row):
           np.append(Field_Names_Groupby["INI_SERIAL"],row[field_names.index(serial_id)])
           np.append(Field_Names_Groupby["TIME"],row[field_names.index(time)])
           np.append(Field_Names_Groupby["ZONE"],row[field_names.index(zone)])
           #then we get the number of the current row -1 to get the last row of the previous block 
           np.append(Field_Names_Groupby["FIN_SERIAL"],row[field_names.index(serial_id)]-1)
           #append a block count each time a transition is reached
           np.append(Field_Names_Groupby["BLOCK_ID"],block_count)

        
        block_count = 0
        with arcpy.da.UpdateCursor(pointsparsedzonegraded,field_names) as cursor:
           for row in cursor:
              #parse the singlestring field, obtain the datetime of the string and convert it into a string
              row[field_names.index("timestamp")] = datetime2string(self._Cartrack2Time(row[field_names.index(singlestring)]))
              #get the current place
              current_place = row[field_names.index(zone)]
              #if the current place has no classification, then change it to ligacao
              row[field_names.index(zone)] = self._replace_emptyspacewithligacao(current_place,ligacao_str)

              #if there is a transition
              if get_place(previous_place,current_place):
                  #increase the block count each time a new transition is reached
                  block_count+=1
                  #update the field names row
                  update_Field_Names_Groupby(row)
                  #close the loop by stating that the previous place is current place, in order for the next loop to happen correctly
                  previous_place = current_place
              row[field_names.index(block_id)] = block_count
              cursor.updateRow(row)
        

        #Append the last row id to the last group fin_serial list, as this is the last point corresponding to the last block
        np.append(Field_Names_Groupby["FIN_SERIAL"],row[field_names.index(serial_id)])
        #Discard the first list element since the get_place() returned True in the transition "" to the first zone
        Field_Names_Groupby["FIN_SERIAL"] = Field_Names_Groupby["FIN_SERIAL"][1:]
        Field_Names_Groupby["ZONE"] = Field_Names_Groupby["ZONE"][1:]


        end_time = Field_Names_Groupby["TIME"][1:]
        np.append(end_time,row[field_names.index("timestamp")])
        start = Field_Names_Groupby["TIME"]
        Field_Names_Groupby["INTERVAL"] = subtract_oneforwardtime(start,end_time)
        Field_Names_Groupby["HOURS"] = string2hour(Field_Names_Groupby["INTERVAL"])
        self.Fields_Numbers["START_TIME"] = Field_Names_Groupby["TIME"][0]
        self.Fields_Numbers["END_TIME"] = row[field_names.index("timestamp")]
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
        polygon = self.shiftpaths["ShiftName"]["Products"]["Circuit_Polygon_Original"]["filepathdicts"]["Circuit_Polygon_Original.shp"]

        pointsnotparsedzonegraded = self.shiftpaths["ShiftName"]["Products"]["Points_NotParsed_Zone"]["filepathdicts"]["Points_NotParsed_Zone.shp"]
        spatialjoin_shpfiles(points,polygon,pointsnotparsedzonegraded)
        deletefieldnames = self.Fields_Table_Parsed["Delete"]
        discard_fieldsInshpfile(pointsnotparsedzonegraded,deletefieldnames)
        add_idfield2shpfile(pointsnotparsedzonegraded,self.Fields_Table_Parsed["SERIAL_ID"])
    


    @signal
    def _copy_mergedppolygon(self):
        self._convert_kml2shp()
        copy_directory(self.processedpolygonspaths["ProcessedPolygonsName"]["SingleObjectBuffered"]["path"],self.shiftpaths["ShiftName"]["Products"]["Circuit_Polygon_Original"]["path"])
        old_basename,_ = os.path.splitext(os.path.basename(self.processedpolygonspaths["ProcessedPolygonsName"]["SingleObjectBuffered"]["filepathdicts"]["SingleObjectBuffered.shp"]))
        new_basename,_ = os.path.splitext(os.path.basename(self.shiftpaths["ShiftName"]["Products"]["Circuit_Polygon_Original"]["filepathdicts"]["Circuit_Polygon_Original.shp"]))
        rename_shpfiles(self.shiftpaths["ShiftName"]["Products"]["Circuit_Polygon_Original"]["path"],old_basename,new_basename)


    @signal
    def _convert_kml2shp(self):
        kml_folder = self.shiftpaths["ShiftName"]["KML"]["path"]
        splitshp_folder = self.shiftpaths["ShiftName"]["SHP"]["SHPsplit"]["path"]
        mergedshp_file= self.shiftpaths["ShiftName"]["SHP"]["SHPmerged"]["filepathdicts"]["SHPmerged.shp"]
        convert_kmlfilesinkmlfolder(kml_folder,splitshp_folder)
        merge_shpfilesinshpfolder(splitshp_folder,mergedshp_file)

        

    

    def GenerateResults():
        print("")

