import os
from ostools import *
from timeparsingtools import * 
from toolsgis import *
import geopandas as gpd
import pandas as pd
import numpy as np
import fiona as fi
import csv

GeoReferences = {
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



@timer
def write_dictcsv(place,data,fieldnames):
    '''
    Creates a .csv with the header and a single row
    '''
    print(place)
    print('writing csv - start')
    with open(place, 'wb') as myfile:
        wr = csv.DictWriter(myfile,fieldnames, quoting=csv.QUOTE_ALL, delimiter=';')
        wr.writeheader()
        for row in csv.DictWriter(myfile):
        # writes the reordered rows to the new file
            writer.writerow(row)
    print('writing csv - end')


@timer
def write_brandcsv(place,data):
    '''
    Creates a .csv with the header and a single row
    '''
    print(place)
    print('writing csv - start')
    with open(place, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=';')
        wr.writerow(data.keys())
        wr.writerows(zip(*data.values()))
    print('writing csv - end')


@timer
def add_line2csv(place,data):
    '''
    Appends a single row to existing csv
    '''
    print(place)
    print('appending csv - start')
    with open(place, 'ab') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=';')
        wr.writerows(zip(*data.values()))
    print('appending csv - end')


@timer
def choosewriteadd(csvpath, data):
    if not os.path.exists(csvpath):
        write_brandcsv(csvpath, data)
    else:
        add_line2csv(csvpath,data)


def subtract_oneforwardtime(start_time,end_time):
    start_time = map(string2datetime,start_time)
    end_time = map(string2datetime,end_time)
    start_time_np =  np.array(start_time)
    end_time_np =  np.array(end_time)
    period_time_np = end_time_np - start_time_np
    return map(tinterval_string,period_time_np) 


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