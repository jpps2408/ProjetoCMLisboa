import os
import toolsgis
import geopandas as gpd
import fiona as fi


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


GeoReferences =  {
      "Portugal_CRS": "+proj=tmerc +lat_0=39.66825833333333 +lon_0=-8.133108333333334 +k=1 +x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs "
      ,
      "Portugal_ArcGIS": "ETRS 1989 Portugal TM06"
      }


@timer
def fi_intialization():
    fi.drvsupport.supported_drivers['libkml'] = 'rw' # enable KML support which is disabled by default
    fi.drvsupport.supported_drivers['LIBKML'] = 'rw'


@timer
def kml2shp(kml_file,shp_file):
    '''
    Converts a kml file into a shape file

    Args:
        kml_file (str): absolute path of the kml file
        shp_file (str): absolute path of the shape shapefile


    '''
    try:
        mygpd = gpd.read_file(kml_file)

        #Spatial reference for Portugal
        mygpd = mygpd.to_crs(GeoReferences["Portugal_CRS"])

        #There is no harm in hardcoding these strings, since they are always the same
        dropcolumns = ['altitudeMode','begin','drawOrder','end','extrude','icon','tessellate','visibility']
        unicode_dropcolumns = [unicode(column) for column in dropcolumns]

        #Droping the columns requires an assignment
        mygpd = mygpd.drop(columns = unicode_dropcolumns)

        #column with information
        mygpd.rename(columns={unicode('description'): unicode('descrp')}, inplace=True)

        #Write file to disk
        mygpd.to_file(shp_file,driver='ESRI Shapefile', encoding='utf-8')
        
        #Spatial reference for Portugal
        set_georeference(shp_file,GeoReferences["Portugal_ArcGIS"])

    except Exception as e:
        print(e)
        print("Please check the following file: {}".format(kml_file))



