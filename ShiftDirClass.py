import os
from DictionaryInstantiator import *
from DirectoryExlorer import *
from toolsgis import *
from toolsfis import *
import numpy as np
import shutil as sh

class ShiftDir(object):


    
    def __init__(self, shiftdirectory, CircuitDirObject ,*args, **kwargs):

            self.circuitobject = CircuitDirObject
            self.Field_Names_Groupby = {}
            self.shiftdirectory = os.path.abspath(shiftdirectory)
            self.pardir = os.path.abspath(os.path.join(shiftdirectory,os.path.pardir))
            self.setShiftPaths()
            self.create_metrics_dicts()

    
    
    @signal
    def setShiftPaths(self):

        shiftJSONDIR = {
        ########Layer 0 #########
        "namestandard": "ShiftName",
        "alias": os.path.basename(self.shiftdirectory),
        "filesystem": {"info.json":"info.json"},
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
                  "filesystem": {"History_Timline.csv":"History_Timline.csv","Appendable.csv":"Appendable.csv"},
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
                             "TOTAL_WEIGHT":"CARREGADO (kg)",
                             "NR_TRIPS":"NR_FRETES",
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
                     "START_TIME","END_TIME",
                     "TOTAL_WEIGHT","NR_TRIPS",
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
        
        self.state = {"CreationFinished":None,
                      "TimeOfCreation":None,
                      "WEIGHTING_END":None,
                      "WEIGHTING_TIMESTAMP":None}
    
        self.Fields_Numbers['CIRCUIT_TOLERANCE'] = self.circuitobject.circuitparameters["PARAMETRO_CIRCUITO (m)"]
        self.Fields_Numbers['VISITED_TOLERANCE'] = self.circuitobject.circuitparameters["PARAMETRO_VISITADOS (m)"]


    @timer
    def process_shift(self,delete=True):
        try:
                self._join_pointswithpolygon()
                self.parse_field()
                self.create_singlelinewithpoints()
                self._get_near_count(self.Fields_Numbers['VISITED_TOLERANCE'])
                self.get_reports()
                self.generate_reports()
                self.save_state()
        except:
            print("Was not able to process realizacao: {} in circuit {}".format(self.Fields_Numbers["SHIFT"],self.Fields_Numbers["CIRCUIT_ID"]))
        else:
            self.place_inToDo()
    




    @timer
    def place_inToDo(self):
        src= self.shiftpaths['ShiftName']['path']
        dst= self.circuitobject.circuitpathdicts['CircuitName']["CircuitVoyages"]['ToDo']['path']
        copyandremove_directory(src,dst)

    

    #@timer
    #def finalize_shift(self,db):
    #    row = pd.read_csv(self.shiftpaths["ShiftName"]["ReportAnalysis"]["filepathdicts"]["Appendable.csv"],sep=';')

    #    datetime_inicio = string2datetime(row['H_INICIO'].values[0])
    #    datetime_fim = string2datetime(row['H_FIM'].values[0])
    #    elapsedtime_ini_fim=datetime_fim-datetime_inicio

    #    fields=["Circuito","DIA","ANO","HORA","DATA","PESO","FT"]
    #    query = "SELECT "+','.join(fields)+" FROM a WHERE Circuito=? AND DIA=? AND MES=? AND ANO=?"
    #    querytuple = (row['CIRCUITO'].values[0],datetime_fim.day,datetime_fim.month,datetime_fim.year)
    #    row_tuples = db.query_db(query,querytuple)

    #    apd = pd.DataFrame(list(row_tuples),columns = ["Circuito","DIA","ANO","HORA","DATA","PESO","FT"])
    #    row["TOTAL_WEIGHT"] = apd["PESO"].sum()
    #    row["NR_TRIPS"] = apd["FT"].max()
        
    #    row.to_csv(self.shiftpaths["ShiftName"]["ReportAnalysis"]["filepathdicts"]["Appendable.csv"],sep=';')

    #    print(row_tuples)
            
    @timer
    def generate_reports(self):
        #Create a columns list with the fields ordered as in self.order. 
        #In order to ensure flexibility, the order list contains the names that are known within the code
        #And the self.Fields_Display maps them onto the names that will be displayed for the "outside workd", in the .csv file
        Columns = [self.Fields_Display[key] for key in self.order]
        #The Fields Values, which have the same keys as the Fields display will also be ordered too to accommodate the ordered Fields_Diplay
        Row = [self.Fields_Numbers[key] for key in self.order]

        #The DataFrame can now be created using pandas DataFrame object
        f = pd.DataFrame([Row], columns=Columns)
        #The pandas DataFrame object uses the method to_csv to write it to a csv file, with a separator ; to make sure it can be seen using 
        #a common .xlsx file reader
        f.to_csv(self.shiftpaths["ShiftName"]["ReportAnalysis"]["filepathdicts"]["Appendable.csv"],sep=';')


    @timer 
    def save_state(self):
        self.state["CreationFinished"] = True
        self.state["TimeOfCreation"] = datetime2string(datetime.datetime.now())
        self.state.update(self.circuitobject.circuitparameters)
        fp = self.shiftpaths['ShiftName']['filepathdicts']['info.json']
        save_state2json(self.state,fp)
    

    @timer
    def get_reports(self):
        self._get_abrupts_reports()

    
    @timer
    def _get_near_count(self,buffersize):
        '''
        This gets the number of points that were visited according to
        the buffersize that is given in
        '''

        #We must make sure that we already have the Circuit points file with a field that contains the count of how many objects each point was 
        ##inside of.
        ##If we had used the split line, we could have more than one buffered line (which becomes a blurred line in the sense 
        ##that it is no longer a line, but is instead an area) intersecting a single point, thus possibly rendering a value larger than 1 in the Join_Count field 
        ##Since it we are using a single line, there can only be a binary evaluation of 1 or 0 in the field Join_Count
        ## which tells us if the  points were intersected by the buffered line (evaluation of 1) or not (evaluation of 0)
        #In order to make the method more flexible, the evaluation is carried out by evaluating if it is a 0 or anything else
        self._join_linewithstaticstops(buffersize)
        #Get the Shapefile that has the processed points
        near_shpfile = self.shiftpaths['ShiftName']['Products']['Circuit_Stops_Original']['filepathdicts']['Circuit_Stops_Original.shp']
        #Get the field
        join_count = "Join_Count"
        #Create the fieldname list. Since it is a single field, it is not needed; However, if we had more fields it would be.
        field_names = [join_count]
        #Create an arcpy cursor (an iterable object) that iterated over the rows. This is useful as it only loads a single row into memory each time
        #it is yielded. We only give it the parameters we need: the shpfile path and the fieldname list of the fields we want
        with arcpy.da.UpdateCursor(near_shpfile,field_names) as cursor:
           #initialize a counter for the total number of points. There is an inbuilt function of arcpy that does this
           #but in order to minimize function overhead, this should not be too expensive
           total_point_count = 0
           #intialize a counter for the ignored point counts
           ignored_point_count = 0
           #Each row is a list with the values in the order specified by the field_name list we gave it as inpuy
           for row in cursor:
               #if the field join count has a 0 value
               #increment the counter
               if row[field_names.index(join_count)]==0:
                   ignored_point_count+=1
               #always increment the counter
               total_point_count+=1
        #the visited nr of points is trivial
        visited_point_count = total_point_count - ignored_point_count
        #note that in order for us to have a number that is not an int, we must cast at least one of the variables to float, otherwise the result
        #will not be cast to float
        #get the ratio of visited and ignored points and round it to 2 decimal places
        visited_point_ratio = round(100*(visited_point_count/float(total_point_count)),2)
        ignored_point_ratio = round(100*(ignored_point_count/float(total_point_count)),2)

        #update the dictionary that will hold the values of the fields in the Appendable csv
        self.Fields_Numbers["ABSOLUTE_VISITED_STOPS"] = visited_point_count
        self.Fields_Numbers["RELATIVE_VISITED_STOPS"] = visited_point_ratio
        self.Fields_Numbers["ABSOLUTE_IGNORED_STOPS"] = ignored_point_count
        self.Fields_Numbers["RELATIVE_IGNORED_STOPS"] = ignored_point_ratio
       
        
           
    @timer 
    def _join_linewithstaticstops(self,buffersize):
        '''
        This joins the single line, that is buffered with the input buffersize
        with the circuit points
        '''
        #When we get the buffersize, immediately assign it to the corresponding field in the dictionary that holds all the 
        #values that will be in the Appendable csv
        line_sole = self.shiftpaths['ShiftName']['Products']['Line_Sole']['filepathdicts']['Line_Sole.shp']
        line_buffered = self.shiftpaths['ShiftName']['Products']['Line_Buffered']['filepathdicts']['Line_Buffered.shp']
        prs_shpfile = self.circuitobject.circuitpathdicts["CircuitName"]['CircuitPolygons']['CircuitData']['CircuitPoints']['filepathdicts']["CircuitPoints.shp"]
        near_shpfile = self.shiftpaths['ShiftName']['Products']['Circuit_Stops_Original']['filepathdicts']['Circuit_Stops_Original.shp']
        #Buffer the line
        buffer_shpfiles(line_sole,line_buffered,buffersize)
        #Spatially join the line with the points and output it to near_shpfile
        spatialjoin_shpfiles(prs_shpfile,line_buffered,near_shpfile)

    
    @timer
    def _get_abrupts_reports(self):
        #Create a Pandas DataFrame object with the Dictionary that contains the changes of zone throughout the shift
        df = pd.DataFrame(self.Field_Names_Groupby)
        #Get the order in which we want to diplay them
        fieldnames=["INI_SERIAL","FIN_SERIAL","BLOCK_ID","TIME","ZONE","INTERVAL","HOURS","DISPLACEMENT"]
        #Reorder the dataframe
        df = df[fieldnames]
        #Finally get the statistics that the client wants
        self._get_zstats(df)
        #We can output this in order to get the history timeline of the shift. THIS IS GOLD
        df["DISPLACEMENT"] = df["DISPLACEMENT"].apply(lambda num: round(num,2))
        df["HOURS"] = df["HOURS"].apply(lambda num: round(num,3))
        

    @timer
    def _get_zstats(self,df):
        '''
        Note that this is easily the most changeable part of the class, as this generates what the client will have as the procesing output
        '''
        #Get the conversion factor from meters to kmeters
        m2km = 10**(-3)
        #Get the fieldnames on which the dataframe will be grouped by. Not
        fieldnames = ["ZONE"]
        #Groupby zone and sum the Hours and length Columns
        df_groupby = df.groupby(fieldnames)["HOURS","DISPLACEMENT"].sum()
        #get the index, which are the index values
        zones = df_groupby.index.values
        #get the hours, which are in the Hours column
        hours = df_groupby["HOURS"].values
        #get the length which are in the length columns
        displacements = df_groupby["DISPLACEMENT"].values
        for i,zone in enumerate(zones):
            #round the hour to 3 decimal places
            rounded_hour = round(hours[i],3)
            #round the displacement in meters to one decimal place and multiply the m2km
            rounded_displacement = round(displacements[i],1)*m2km
            #put it in the main dictionary if the zone matches the code of the zone
            self.Fields_Numbers[self.zone_timefieldmapping[zone]] = rounded_hour
            self.Fields_Numbers[self.zone_displfieldmapping[zone]] = rounded_displacement
            #put the speed in the dicitonary
            speed = rounded_displacement/rounded_hour
            self.Fields_Numbers[self.zone_velfieldmapping[zone]] = round(speed,2)
        #put the totals inside the dictionary. this will always be outside the sum
        self.Fields_Numbers['TOTAL_TIME'] = round(df["HOURS"].sum(),2)
        self.Fields_Numbers['TOTAL_DIST'] = round(df["DISPLACEMENT"].sum(),1)*m2km


    @timer
    def create_singlelinewithpoints(self):
        line_sole = self.shiftpaths['ShiftName']['Products']['Line_Sole']['filepathdicts']['Line_Sole.shp']
        line_part_uncoded = self.shiftpaths['ShiftName']['Products']['Line_Tranche']['filepathdicts']['Line_Tranche.shp']
        points = self.shiftpaths['ShiftName']['Products']['Points_Parsed_Zone']['filepathdicts']['Points_Parsed_Zone.shp']
        line_part_coded = self.shiftpaths['ShiftName']['Products']['Line_Tranche_Code']['filepathdicts']['Line_Tranche_Code.shp']

        #convert the points to a line
        convert_points2line(points,line_sole)
        #split the line into several parts
        split_linein2pairs(line_sole,line_part_uncoded)
        #join the split line with the shift points, which will give the points classification to the line
        spatialjoin_shpfiles(line_part_uncoded,points,line_part_coded)
        #Calculate the length of each of the split lines, which are now with a code and the block id classification of the points
        add_attribute2shpfile(line_part_coded)


        #pass in the shpfile, the original block id array and the field name which contains the length of each split line
        blockid_array,length_array = self._get_gpdindexvalues(line_part_coded,self.Fields_Table_Parsed["BLOCK_ID"],'LENGTH')
        
        #Since there is the possibility that a block id of the points did not make it into the lines block id (because the split line was joined with multiple points
        #and kept another classification) I decided to compare the block id arrays from the points and the line
        length_array = self._fill_length_distwithzeros(self.Field_Names_Groupby["BLOCK_ID"],blockid_array,length_array)
        #Finally assign it to the array
        self.Field_Names_Groupby["DISPLACEMENT"] = length_array


    @timer
    def _fill_length_distwithzeros(self,blockid_time,blockid_dist,length_dist):
        #check if there are differences in the block ids of the points and the lines (which makes a non empty set)
        differentblocks = set(blockid_time)-set(blockid_dist)
        #if there is a difference in the block id arrays of the lines and the points, insert a 0 at the length array in the position of the block id
        #I need to sort the set because if the length array has 9 elements and the pooints array has 20 elements and I att
        length_dist_filled = np.zeros((len(blockid_time),))
        zero = float(0)
        for index_iter in sorted(differentblocks):
            try:
                length_dist = np.insert(length_dist,index_iter,zero)
            except:
                length_dist = np.append(length_dist,zero)
        return length_dist
        

    @timer   
    def _get_gpdindexvalues(self,shpfile,groupfieldname,sumfieldname):
        #read the lines shpfile
        pd_all = gpd.read_file(shpfile)
        #select the rows sumfieldname and the field on which the groupby operation will operate 
        #group the dataframe containing the lines by the groupfield (which is given by the block ids) and sum the lines'lengths.
        pd_index_values = pd_all[[sumfieldname,groupfieldname]].groupby([groupfieldname])[sumfieldname].sum()
        #get the block ids
        pd_index = pd_index_values.index.values
        #and the sums of lengths
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
        #initialize the previous_place as somethin
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

        #aux_zone = Field_Names_Groupby["ZONE"][:]
        #aux_zone.reverse()
        #last_timeunloadingbegan_index = aux_zone.index(self.circuitobject.zone_classification['UNLOADING'])
        #last_timeunloadingbegan_index = len(Field_Names_Groupby["ZONE"][:]) - last_timeunloadingbegan_index
        #Fields_Numbers["UNLOADING_LASTTIME"] = Field_Names_Groupby["TIME"][last_timeunloadingbegan_index]

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
        self.processedpolygonspaths = self.circuitobject.ProcessedPolygon.processedpolygonspaths
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

        

    

