import arcpy
import time
import functools
from timeparsingtools import *

@timer
def convert_shpfile2convexhull(inputshpfile,outputshpfile):
   """Converts the shpfile containing the points into a convex hull polygon
   inputshpfile: (str)
   outputshpfile: (str)"""
   arcpy.management.MinimumBoundingGeometry(inputshpfile, outputshpfile, 
                                             "CONVEX_HULL", "ALL")


@timer
def buffer_shpfiles(inputshpfile,outputshpfile,buffersize):
   """Creates a buffer for the input polygon with the specified buffer size and creates a output shp file
   inputshpfile: (str)
   outputshpfile: (str)
   buffersize: (int)"""
   arcpy.analysis.Buffer(inputshpfile,outputshpfile,str(buffersize) + ' METERS', "FULL", "ROUND", "LIST")   


@timer
def merge_shpfiles(inputshpfilpath_list,outputshpfile):
   """Merges the input shpfiles and places the output shp file in output
      inputshpfilpath_list: (list of str)
      outputshpfile: (str)"""
   arcpy.management.Merge(inputshpfilpath_list, outputshpfile)


@timer
def spatialjoin_shpfiles(inputshpfiletobeclassified,inputshpfilewithcode,outputshpfile):
   """It is a type of intersection, that handles shp files of different types. We use it to classify the points"""
   arcpy.analysis.SpatialJoin(inputshpfiletobeclassified, inputshpfilewithcode, outputshpfile)


@timer
def convert_points2line(inputpointsshpfile,outputlineshpfilepath):
   """Convert all of the points into a single line
   inputshpfile: (str)
   outputshpfile: (str)"""
   arcpy.PointsToLine_management(inputpointsshpfile,outputlineshpfilepath)


@timer
def split_linein2pairs(linha_shpfile,linha_splitshpfile):
   """Split the input line shpfiles into lines that are pairs of points
   inputshpfile: (str)
   outputshpfile: (str)"""
   arcpy.SplitLine_management(linha_shpfile,linha_splitshpfile)


@timer
def add_attribute2shpfile(inputpointsshpfile,attribute = 'LENGTH',attribute_unit = 'METERS'):
   """Adds an attribute to 
   inputshpfile: (str)
   outputshpfile: (str)"""
   arcpy.AddGeometryAttributes_management(inputpointsshpfile,attribute,attribute_unit)


@timer
def add_textattribute2shpfile(inputshpfile,field_name):
   """Adds a text field to  the input shpfile
   inputshpfile: (str)
   outputshpfile: (str)"""
   arcpy.AddField_management(inputshpfile,field_name,"TEXT", "", "", "90", "", "NON_NULLABLE", "NON_REQUIRED", "")


@timer
def addfieldcode(inputshpfile,field_name,code):
   add_textattribute2shpfile(inputshpfile,field_name)
   try:
          with arcpy.da.UpdateCursor(inputshpfile,field_name) as cursor:
             for row in cursor:  
                row[0] = code
                cursor.updateRow(row)
   except Exception as identifier:
      print(identifier)
      discard_fieldsInshpfile(inputshpfile,field_name)


@timer
def add_longattribute2shpfile(inputshpfile,field_name):
   """Adds a text field to  the input shpfile
   inputshpfile: (str)
   field_name: (str)"""
   arcpy.AddField_management(inputshpfile,field_name,"LONG", "", "", "", "", "", "", "")


@timer
def add_idfield2shpfile(inputshpfile,field_name):
    add_longattribute2shpfile(inputshpfile,field_name)
    def add_increasingint():  
        try:
            #nr_max = arcpy.GetCount_management(pontos_shpfile).getOutput(0)-1
            with arcpy.da.UpdateCursor(inputshpfile,field_name) as cursor:
                count = 0
                for row in cursor:
                    row[0] = count
                    count+=1
                    cursor.updateRow(row)
        except Exception as e:
            print(e)
    add_increasingint()    


@timer
def set_georeference(inputshpfile,reference):
     arcpy.DefineProjection_management(inputshpfile, arcpy.SpatialReference(reference))


#Needs to create an additional file: not worth it
@timer
def sort_shpfilebyidfield(inputshpfile,outputshpfile,intfield,desc=False):
    if desc:
        arcpy.Sort_management(inputshpfile, outputshpfile, [[intfield, "DESCENDING"]])
    else:
        arcpy.Sort_management(inputshpfile, outputshpfile, [[intfield, "ASCENDING"]])


@timer
def list_fieldsInshpfile(shpfile):
    fields_list = [field.name for field in arcpy.ListFields(shpfile)]
    return fields_list

@timer
def discard_fieldsInshpfile(inputshpfile,fieldstrings_list):
    arcpy.DeleteField_management(inputshpfile,fieldstrings_list)


@timer
def keep_fieldsInshpfile(inputshpfile,fieldstrings_list):
    fields_to_discard = [field for field in list_fieldsInshpfile(inputshpfile) if field not in fieldstrings_list]
    arcpy.DeleteField_management(inputshpfile,fields_to_discard)


#Only works if the table is registered within a geo database. 
#No need to complicate
#@timer
#def func(shpfile,field_name_list,sorter="ORDER BY intfield DESC",*args):
#    try:
#        #nr_max = arcpy.GetCount_management(pontos_shpfile).getOutput(0)-1
#        with arcpy.da.UpdateCursor(shpfile,field_name_list,sql_clause = sorter) as cursor:
#            for row in cursor:
#                print(row)
#    except Exception as e:
#        print('Raised error ocurred at store_table_as_list')
#        print(e)


