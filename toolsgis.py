import arcpy
import functools
import time


def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        try:
           start_time = time.time()    # 1
           value = func(*args,**kwargs)
           end_time = time.time()      # 2
           run_time = end_time - start_time    # 3
           print("Finished " + func.__name__ + " in " + str(run_time) + " secs")
           return value
        except Exception as e:
           print("Error occurred.\n\tFunction: " + func.__name__ + "\n\tExcepion: " + str(e))
    return wrapper_timer


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
def add_field2shpfile(inputshpfile,field_name):
   """Adds a text field to  the input shpfile
   inputshpfile: (str)
   outputshpfile: (str)"""
   arcpy.AddField_management(inputshpfile,field_name,"TEXT", "", "", "90", "", "NON_NULLABLE", "NON_REQUIRED", "")


@timer
def set_georeference(inputshpfile,reference):
     arcpy.DefineProjection_management(inputshpfile, arcpy.SpatialReference(reference))

