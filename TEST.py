

#############ATTEMPT TO USE XY TO LINE######################
import arcpy
arcpy.env.overwriteOutput = True

def add_numattribute2shpfile(inputshpfile,field_name):
   """Adds a text field to  the input shpfile
   inputshpfile: (str)
   outputshpfile: (str)"""
   arcpy.AddField_management(inputshpfile,field_name,"FLOAT", "", "", "90", "", "NON_NULLABLE", "NON_REQUIRED", "")


def add_attribute2shpfile(inputpointsshpfile,attribute = 'LENGTH',attribute_unit = 'METERS'):
   """Adds an attribute to 
   inputshpfile: (str)
   outputshpfile: (str)"""
   arcpy.AddGeometryAttributes_management(inputpointsshpfile,attribute,attribute_unit)


def sort_shpfilebyidfield(inputshpfile,outputshpfile,intfield,desc=True):
    if desc:
        arcpy.Sort_management(inputshpfile, outputshpfile, [[intfield, "DESCENDING"]])
    else:
        arcpy.Sort_management(inputshpfile, outputshpfile, [[intfield, "ASCENDING"]])

def set_georeference(inputshpfile,reference):
     arcpy.DefineProjection_management(inputshpfile, arcpy.SpatialReference(reference))

def get_georeference(reference):
    return arcpy.SpatialReference(reference)
linha_shpfile = "C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01\I0104\aliasCircuitVoyages\aliasToDo\realizacao_2\Products\Line_Tranche_Code\Line_Tranche_Code.shp"



#sort in descending order. Inverting the table  will solve the age old problem of
#putting the next row info in the current row
sort_shpfilebyidfield(pontos_shpfile,pontos_shpfile_,"SERIAL",True)
nrrows = str(int(arcpy.GetCount_management(pontos_shpfile).getOutput(0)) -1)


#get the first row, but since it is inverted we get the row whose serial number is largest


linha_shpfile = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01\I0104\aliasCircuitVoyages\aliasToDo\realizacao_2\Products\Line_Tranche_Code\Line_Tranche_Code.shp"


field_names = ['ZONA','LENGTH',"BLOCK_ID"]

import geopandas as gpd

import pandas as pd