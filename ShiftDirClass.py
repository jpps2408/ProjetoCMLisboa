import os
from DictionaryInstantiator import *
from DirectoryExlorer import *
from toolsgis import *
from toolsfis import *
import numpy as np
import shutil as sh

class ShiftDir(object):


    
    def __init__(self, shiftdirectory, CircuitDirObject ,*args, **kwargs):

            self.processedpolygonspaths = CircuitDirObject.ProcessedPolygon.processedpolygonspaths
            self.circuitobject = CircuitDirObject
            self.Field_Names_Groupby = {}
            self.shiftdirectory = os.path.abspath(shiftdirectory)
            self.pardir = os.path.abspath(os.path.join(shiftdirectory,os.path.pardir))
            self.create_metrics_dicts()
            self.setShiftPaths()

    
    
    @signal
    def setShiftPaths(self):

        shiftJSONDIR = {
        ########Layer 0 #########
        "namestandard": "ShiftName",
        "alias": os.path.basename(self.shiftdirectory),
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








    
    def create_metrics_dicts(self):
        
        self.Fields_Table_Parsed = {"Delete":["Name","TARGET_FID","Join_Count","Id","ORIG_FID"],
                                  "SERIAL_ID":"SERIAL",
                                  "SINGLESTRING":"descrp",
                                  "TIME":"timestamp",
                                  "ZONE": self.circuitobject.zone_classification["CODE_FIELD_NAME"],
                                  "BLOCK_ID":"BLOCK_ID"}

            
        self.Cartrack = {"SplitSep":'<br></br>',
                    "CarTrackTimeFieldName":"Time: ",
                    "TimeStampWithoutUTCOffset": (6,25),
                    "UTCOffset": (26,28)}


        self.Mission_Codes_Macro = {
                         "S2P":("G","P"),
                         "P2P":("P","P"),
                         "P2C":("P","C"),
                         "C2C":("C","C"),
                         "C2P":("C","P"),
                         "C2T":("C","G")}

        self.Mission_Codes_Micro = {
                         "S2P":("G","P"),
                         "P2P":("P","P"),
                         "P2C":("P","C"),
                         "C2C":("C","C"),
                         "C2P":("C","P"),
                         "C2T":("C","G")}

        
        self.zone_abbreviation = {
                    self.circuitobject.zone_classification['GARAGE']:"G",
                    self.circuitobject.zone_classification['CIRCUIT']:"R",
                    self.circuitobject.zone_classification['UNLOADING']:"C",
                    self.circuitobject.zone_classification['CONNECTION']:"L"}

        self.Fields_Display={"CIRCUIT_ID":"CIRCUITO",
                             "SHIFT":"PERCURSO",
                             "START_TIME":"H_INICIO",
                             "END_TIME":"H_FIM",
                             "UNLOADING_LASTTIME":"DESCARGA",
                             "CIRCUIT_TOLERANCE":"PARAMETRO_CIRCUITO (m)",
                             "VISITED_TOLERANCE":"PARAMETRO_VISITADOS (m)",
                             "ABSOLUTE_VISITED_STOPS":"NR_VISITADOS",
                             "RELATIVE_VISITED_STOPS":"%_VISITADOS",
                             "ABSOLUTE_IGNORED_STOPS":"NR_IGNORADOS",
                             "RELATIVE_IGNORED_STOPS":"%_IGNORADOS",
                             "TOTAL_TIME":"TEMPO_TOTAL (h)",
                             "TOTAL_DIST":"DIST_TOTAL (km)",
                             "GARAGE_TIME":"TEMP_GARAGEM (h)",
                             "GARAGE_DIST":"DIST_GARAGEM (km)",
                             "GARAGE_VELOCITY":"VELOCIDADE_GARAGEM (km/h)",
                             "UNLOADING_TIME":"TEMP_DESCARGA (h)",
                             "UNLOADING_DIST":"DIST_DESCARGA (km)",
                             "UNLOADING_VELOCITY":"VELOCIDADE_DESCARGA (km/h)",
                             "CIRCUIT_TIME":"TEMP_RECOLHA (h)",
                             "CIRCUIT_DIST":"DIST_RECOLHA (km)",
                             "CIRCUIT_VELOCITY":"VELOCIDADE_RECOLHA (km/h)",
                             "CONNECTION_TIME":"TEMP_LIGACAO (h)",
                             "CONNECTION_DIST":"DIST_LIGACAO (km)",
                             "CONNECTION_VELOCITY":"VELOCIDADE_LIGACAO (km/h)",
                             "OTHERS_TIME":"TEMP_OUTROS (h)",
                             "OTHERS_DIST":"DIST_OUTROS (km)",
                             "OTHERS_SPEED":"VELOCIDADE_OUTROS (km/h)"}



        self.Fields_Numbers={_ : None for _ in self.Fields_Display.keys()}
        self.Fields_Numbers["SHIFT"] = os.path.basename(self.shiftdirectory)
        self.Fields_Numbers.update(self.circuitobject.circuitdict)


        self.order =["CIRCUIT_ID",
                     "SHIFT",
                     "START_TIME","END_TIME","UNLOADING_LASTTIME",
                     "CIRCUIT_TOLERANCE","VISITED_TOLERANCE",
                     "TOTAL_TIME","TOTAL_DIST",
                     "ABSOLUTE_VISITED_STOPS", "RELATIVE_VISITED_STOPS",
                     "ABSOLUTE_IGNORED_STOPS","RELATIVE_IGNORED_STOPS",
                     "GARAGE_TIME","GARAGE_DIST","GARAGE_VELOCITY",
                     "UNLOADING_TIME","UNLOADING_DIST","UNLOADING_VELOCITY",
                     "CIRCUIT_TIME","CIRCUIT_DIST","CIRCUIT_VELOCITY",
                     "CONNECTION_TIME","CONNECTION_DIST","CONNECTION_VELOCITY",
                     "OTHERS_TIME","OTHERS_DIST"]

        self.zone_velfieldmapping = {
                    self.circuitobject.zone_classification['GARAGE']:"GARAGE_VELOCITY",
                    self.circuitobject.zone_classification['CIRCUIT']:"CIRCUIT_VELOCITY",
                    self.circuitobject.zone_classification['UNLOADING']:"UNLOADING_VELOCITY",
                    self.circuitobject.zone_classification['CONNECTION']:"CONNECTION_VELOCITY"}
        self.zone_timefieldmapping = {
                    self.circuitobject.zone_classification['GARAGE']:"GARAGE_TIME",
                    self.circuitobject.zone_classification['CIRCUIT']:"CIRCUIT_TIME",
                    self.circuitobject.zone_classification['UNLOADING']:"UNLOADING_TIME",
                    self.circuitobject.zone_classification['CONNECTION']:"CONNECTION_TIME"}
        self.zone_displfieldmapping = {
                    self.circuitobject.zone_classification['GARAGE']:"GARAGE_DIST",
                    self.circuitobject.zone_classification['CIRCUIT']:"CIRCUIT_DIST",
                    self.circuitobject.zone_classification['UNLOADING']:"UNLOADING_DIST",
                    self.circuitobject.zone_classification['CONNECTION']:"CONNECTION_DIST"}


        #Create the fieldnames that completely describe a circuit, by blocks of chronologically contiguous points that have the same classification        
        #create a transitions dictionary of lists. Note that this is defined inside a class method because if it was
        #defined outside a class method bu inside a class body, it would be a class variable and hence if we changed 
        #the instance we were dealing with we would get the same transition lists throughout all of the living objects/instances 
        self.Field_Names_Groupby ={"INI_SERIAL":[],
                                   "FIN_SERIAL":[],
                                   "TIME":[],
                                   "INTERVAL":[],
                                   "HOURS":[],
                                   "ZONE":[], 
                                   "BLOCK_ID":[],
                                   "DISPLACEMENT":[]}

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
        
        Columns = [self.Fields_Display[key] for key in self.order]
        Row = [self.Fields_Numbers[key] for key in self.order]

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
        self.Fields_Numbers['VISITED_TOLERANCE'] = buffersize
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
        self._get_zstats(df)
        #df.to_csv(self.shiftpaths["ShiftName"]["ReportAnalysis"]["filepathdicts"]["Time_History.csv"],sep=';')
        

    @timer
    def _get_zstats(self,df):
        m2km = 10**(-3)
        fieldnames = ["ZONE"]
        df_groupby = df.groupby(fieldnames)["HOURS","DISPLACEMENT"].sum()
        zones = df_groupby.index.values
        hours = df_groupby["HOURS"].values
        displacements = df_groupby["DISPLACEMENT"].values
        for i,zone in enumerate(zones):
            rounded_hour = round(hours[i],3)
            rounded_displacement = round(displacements[i],1)*m2km
            self.Fields_Numbers[self.zone_timefieldmapping[zone]] = rounded_hour
            self.Fields_Numbers[self.zone_displfieldmapping[zone]] = rounded_displacement
            speed = rounded_displacement/rounded_hour
            self.Fields_Numbers[self.zone_velfieldmapping[zone]] = round(speed,2)
        self.Fields_Numbers['TOTAL_TIME'] = round(df["HOURS"].sum(),2)
        self.Fields_Numbers['TOTAL_DIST'] = round(df["DISPLACEMENT"].sum(),1)*m2km


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
        
        previous_place = ""
        self.Field_Names_Groupby["ZONE"].append(previous_place)

        #Create the fieldnames that completely describe a circuit, by blocks of chronologically contiguous points that have the same classification
        Fields_Numbers = self.Fields_Numbers
        Field_Names_Groupby = self.Field_Names_Groupby
        

        #Update the Field Names with the row contents in order to 
        def update_Field_Names_Groupby(row):
           Field_Names_Groupby["INI_SERIAL"].append(row[field_names.index(serial_id)])
           Field_Names_Groupby["TIME"].append(row[field_names.index(time)])
           Field_Names_Groupby["ZONE"].append(row[field_names.index(zone)])
           #then we get the number of the current row -1 to get the last row of the previous block 
           Field_Names_Groupby["FIN_SERIAL"].append(row[field_names.index(serial_id)]-1)
           #append a block count each time a transition is reached
           Field_Names_Groupby["BLOCK_ID"].append(block_count)

        
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
        Field_Names_Groupby["FIN_SERIAL"].append(row[field_names.index(serial_id)])
        #Discard the first list element since the get_place() returned True in the transition "" to the first zone
        Field_Names_Groupby["FIN_SERIAL"] = Field_Names_Groupby["FIN_SERIAL"][1:]
        Field_Names_Groupby["ZONE"] = Field_Names_Groupby["ZONE"][1:]


        end_time = Field_Names_Groupby["TIME"][1:]
        end_time.append(row[field_names.index("timestamp")])
        start = Field_Names_Groupby["TIME"]
        Field_Names_Groupby["INTERVAL"] = subtract_oneforwardtime(start,end_time)
        Field_Names_Groupby["HOURS"] = map(string2hour,Field_Names_Groupby["INTERVAL"])
        Fields_Numbers["START_TIME"] = Field_Names_Groupby["TIME"][0]
        Fields_Numbers["END_TIME"] = row[field_names.index("timestamp")]

        aux_zone = Field_Names_Groupby["ZONE"][:]
        #aux_zone.reverse()
        last_timeunloadingbegan_index = aux_zone.index(self.circuitobject.zone_classification['UNLOADING'])
        last_timeunloadingbegan_index = len(Field_Names_Groupby["ZONE"][:]) - last_timeunloadingbegan_index
        Fields_Numbers["UNLOADING_LASTTIME"] = Field_Names_Groupby["TIME"][last_timeunloadingbegan_index]

        self.Fields_Numbers = Fields_Numbers
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

