import os
from ostools import *
from timeparsingtools import * 
from toolsgis import *
import geopandas as gpd
import fiona as fi


GeoReferences =  {
      "Portugal_CRS": "+proj=tmerc +lat_0=39.66825833333333 +lon_0=-8.133108333333334 +k=1 +x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs "
      ,
      "Portugal_ArcGIS": "ETRS 1989 Portugal TM06"
      }


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
        fi_intialization()

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



@timer
def convert_kmlfilesinkmlfolder(kmlfolderabsolutepath,shpfolderabsolutepath):
    kmlfile_list = getfilesinpath(kmlfolderabsolutepath,extension=".kml")
    shpfile_list = []
    if kmlfile_list:
        for kmlfilepath_str in kmlfile_list:
            shpfilename_str = os.path.splitext(os.path.basename(kmlfilepath_str))[0] + ".shp"
            shpfilepath_str = os.path.join(shpfolderabsolutepath,shpfilename_str)
            kml2shp(kmlfilepath_str,shpfilepath_str)
            shpfile_list.append(shpfilepath_str)
    return shpfile_list


@timer
def merge_shpfilesinshpfolder(shpsplitfolderabsolutepath,shpconvertedfileabsolutepath):
    shpfiles_list = getfilesinpath(shpsplitfolderabsolutepath,".shp")
    merge_polygons(shpfiles_list,shpconvertedfileabsolutepath)







#@timer
#def rename_filesv1(dir,old,new):
#    for file in os.listdir(dir):
#        basename = file
#        while not fileextension=="":
#            basename,fileextension = os.path.splitext(os.path.basename(basename))
#        if basename==old:
#            old_path = os.path.abspath(os.path.join(dir,file))
#            new_path = os.path.abspath(os.path.join(dir,new+fileextension))
#            os.rename(old_path,new_path)