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
#shift.join_pointswithpolygon()
#print("")
######################################################
################## ##################
######################################################





def inner1(**kwargs):
    a = "inner1"
    print("I'm inner1")
    print(kwargs["txttoprint1"])
    print("I'm  inner1")
    x = CD.CircuitDir(r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01")
    return x


def inner2(**kwargs):
    b = "inner2"
    print("I'm  inner2")
    print(kwargs["txttoprint2"])
    print("I'm  inner2")
    return kwargs["values_func2"]
    

def inner(*args,**kwargs):
    values1 = inner1(**kwargs)
    values2 = inner2(**kwargs)
    return values1,values2

def outer(**kwargs):
    print("I'm  outer2")
    print(str(kwargs["nrstoprint"]))
    print("I'm  outer2")
    return 0

def bread_func(func1,func2,**kwargs):
    kwargs['values_func2'] = func1(**kwargs)
    print(kwargs['values_func2'])
    for i in range(1):
       kwargs['values_func2'] =  func2(**kwargs)
    return kwargs['values_func2']

a  = bread_func(outer,inner,txttoprint1="YAY1",txttoprint2="YAY2", nrstoprint = 2000, number = 3)