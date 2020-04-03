

import DirectoryExlorer as CD
from ShiftDirClass import *
from toolsgis import *
from ostools import *
from timeparsingtools import *


#linha_split = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\I0104\realizacoes\I0104_V2520_12_01_2020\analysis_products\linha_split\linha_split.shp"
#merged = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\I0104\realizacoes\I0104_V2520_12_01_2020\analysis_products\merged\merged.shp"
#pontos = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\I0104\realizacoes\I0104_V2520_12_01_2020\analysis_products\pontos\pontos.shp"
#pontos_merged = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\I0104\realizacoes\I0104_V2520_12_01_2020\analysis_products\pontos_merged\pontos_merged.shp"
#pontos_merged1 = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\I0104\realizacoes\I0104_V2520_12_01_2020\analysis_products\pontos_merged\pontos_merged1.shp"
#pontos_merged_buffer = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\I0104\realizacoes\I0104_V2520_12_01_2020\analysis_products\pontos_merged_buffer\pontos_merged_buffer.shp"
#prs = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\I0104\realizacoes\I0104_V2520_12_01_2020\analysis_products\prs\prs.shp"
#prs_area = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\I0104\realizacoes\I0104_V2520_12_01_2020\analysis_products\prs_area\prs_area.shp"
#prs_near = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\I0104\realizacoes\I0104_V2520_12_01_2020\analysis_products\prs_near\prs_near.shp"
#prs_stops = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\I0104\realizacoes\I0104_V2520_12_01_2020\analysis_products\prs_stops\prs_stops.shp"
#I0104 = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\I0104\polygons\prs_unp\I0104.shp"
#CTRSU_AREA = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\I0104\polygons\descarga\CTRSU_Area.shp"
#GARAGEM = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\I0104\polygons\garagem\OFICINAS_CML_Group.shp"

#Test the various submodules
######################################################
################## Test  ##################
######################################################
# ix_circuito = -4
# ix_realizacao = -2
# self.circuito = base_path.split("\\")[ix_circuito]
# self.realizacao = self.base_path.split("\\")[ix_realizacao]

#x = CD.CircuitDir(r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01")
#x.setCircuitPaths()
#a = x.getRealizacoesDoNe()
#shift = CD.ShiftDir(r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01\trips\todo\trip_name")
#shift.setShiftPaths()
#print(shift.shiftpaths)

######################################################
################## ##################
######################################################

#add_idfield2shpfile(pontos_merged,"ID")
#discard_fieldsInshpfile(pontos_merged,["AIAIII","AIAI","AAD","ImD","ID"])
#addfieldcode(pontos_merged,"ZONE","CIRCUITO")
#


#circuit_folder = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01\I0104"
#circuit_object = CD.CircuitDir(circuit_folder)
#circuit_object.make_CircuitPolygon(50)

#realizacao = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01\I0104\aliasCircuitVoyages\aliasToDo\realizacao_2"
#shift = ShiftDir(realizacao,circuit_object)
#shift.parse_field()
##print("")
######################################################
################## ##################
######################################################


#pointsparsedzonegraded = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01\I0104\aliasCircuitVoyages\aliasToDo\realizacao_2\Products\Points_Parsed_ZoneCoded\Points_Parsed_ZoneCoded.shp"
#field_names = ["SERIAL","descrp","timestamp","ZONA"]
#previous_transition = ""
#transitions= []
#with arcpy.da.UpdateCursor(pointsparsedzonegraded,field_names,where_clause=) as cursor:
#    for row in cursor:
#        prev_row = row
#        row[field_names.index("timestamp")] = self._Cartrack2Time(row[field_names.index("descrp")]) 
#        current_row_int = row[field_names.index("SERIAL")]
#        current_transition = row[field_names.index("ZONA")]
#        row[field_names.index("ZONA")] = replace_emptyspacewithligacao(current_transition,"ligacao")
#        if get_transition(previous_transition,current_transition):
#            previous_transition = current_transition
#            transitions.append([row[field_names.index("timestamp")],row[field_names.index("ZONA")],row[field_names.index("SERIAL")]])
#        row[field_names.index("timestamp")] = datetime2string(row[field_names.index("timestamp")])
#        cursor.updateRow(row)

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
    splitsep_str= self.Cartrack["SplitSep"]
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


pointsparsedzonegraded = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01\I0104\aliasCircuitVoyages\aliasToDo\realizacao_2\Products\Points_Parsed_ZoneCoded\Points_Parsed_ZoneCoded.shp"
field_names = ["SERIAL","descrp","timestamp","ZONA"]
previous_transition = ""
transitions= []
var = arcpy.GetCount_management(pointsparsedzonegraded).getOutput(0)
with arcpy.da.UpdateCursor(pointsparsedzonegraded,field_names,where_clause="SERIAL="+str(int(arcpy.GetCount_management(pointsparsedzonegraded).getOutput(0))-1)) as cursor:
    for row in cursor:
        prev_row = row
        row[field_names.index("timestamp")] = _Cartrack2Time(row[field_names.index("descrp")]) 
        current_row_int = row[field_names.index("SERIAL")]
        current_transition = row[field_names.index("ZONA")]
        row[field_names.index("ZONA")] = replace_emptyspacewithligacao(current_transition,"ligacao")
        if get_transition(previous_transition,current_transition):
            previous_transition = current_transition
            transitions.append([row[field_names.index("timestamp")],row[field_names.index("ZONA")],row[field_names.index("SERIAL")]])
        row[field_names.index("timestamp")] = datetime2string(row[field_names.index("timestamp")])
        cursor.updateRow(row)

a = int(arcpy.GetCount_management(pointsparsedzonegraded).getOutput(0))-1