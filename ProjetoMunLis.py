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


circuit_folder = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01\I0104"
circuit_object = CD.CircuitDir(circuit_folder)
circuit_object.make_CircuitPolygon(50)

realizacao = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01\I0104\aliasCircuitVoyages\aliasToDo\realizacao_2"
shift = ShiftDir(realizacao,circuit_object)
shift.join_pointswithpolygon()
shift.parse_field()
#print("")
######################################################
################## ##################
######################################################




