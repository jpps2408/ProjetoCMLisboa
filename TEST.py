

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

#######Add start_x,start_y,end_x,end_y fields to each row ###############
pontos_shpfile=r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01\I0104\aliasCircuitVoyages\aliasToDo\realizacao_2\Products\Points_Parsed_ZoneGraded\Points_Parsed_ZoneGraded.shp"
pontos_shpfile_upsidedown=r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01\I0104\aliasCircuitVoyages\aliasToDo\realizacao_2\Products\Points_Parsed_ZoneGraded\Points_Parsed_ZoneGraded.shp"
pontos_shpfile_=r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01\I0104\aliasCircuitVoyages\aliasToDo\realizacao_2\Products\Points_Parsed_Coded\Points_Parsed_Coded.shp"

add_numattribute2shpfile(pontos_shpfile,'start_x')
add_numattribute2shpfile(pontos_shpfile,'start_y')
add_numattribute2shpfile(pontos_shpfile,'end_x')
add_numattribute2shpfile(pontos_shpfile,'end_y')

#Create the shp 
set_georeference(pontos_shpfile,"ETRS 1989 Portugal TM06")
add_attribute2shpfile(pontos_shpfile,attribute="POINT_X_Y_Z_M")
arcpy.CalculateField_management(pontos_shpfile, "start_x", "!POINT_X!", "PYTHON_9.3", "")
arcpy.CalculateField_management(pontos_shpfile, "start_y", "!POINT_Y!", "PYTHON_9.3", "")



#sort in descending order. Inverting the table  will solve the age old problem of
#putting the next row info in the current row
sort_shpfilebyidfield(pontos_shpfile,pontos_shpfile_,"SERIAL",True)
nrrows = str(int(arcpy.GetCount_management(pontos_shpfile).getOutput(0)) -1)


#get the first row, but since it is inverted we get the row whose serial number is largest
field_names = ['start_x','start_y','end_x','end_y']
with arcpy.da.UpdateCursor(pontos_shpfile_,field_names,where_clause = "SERIAL="+nrrows) as cursor:
    for row in cursor:
        prev_row = row
        break

#update the end x and end y
with arcpy.da.UpdateCursor(pontos_shpfile_,field_names) as cursor:
    for row in cursor:
        row[field_names.index('end_x')] = prev_row[field_names.index('start_x')]
        row[field_names.index('end_y')] = prev_row[field_names.index('start_y')]
        prev_row = row
        cursor.updateRow(row)



sr = get_georeference("ETRS 1989 Portugal TM06")
outlines = r"C:\Users\JoaoPedro\Desktop\ArcGISTestMaker\Circuit_01\I0104\aliasCircuitVoyages\aliasToDo\realizacao_2\Products\Line_Separate_NotCoded\Line_Separate_NotCoded.shp"
sort_shpfilebyidfield(pontos_shpfile_,pontos_shpfile_upsidedown,"SERIAL",False)
arcpy.XYToLine_management(pontos_shpfile_upsidedown,outlines,"start_x","start_y","end_x","end_y",spatial_reference = "ETRS 1989 Portugal TM06")