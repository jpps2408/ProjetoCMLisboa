import os
import functools
import time
from distutils.dir_util import copy_tree
import shutil
import json
import traceback
import shutil as sh
def timer(func,*args, **kwargs):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        try:
           start_time = time.time()    # 1
           value = func(*args,**kwargs)
           end_time = time.time()      # 2
           run_time = end_time - start_time    # 3
           print("Finished " + func.__name__ + " in " + str(run_time) + " secs\n")
           return value
        except Exception as e:
           print("Error occurred.\n\t\t\tFunction: " + func.__name__ + "\n\t\t\tExcepion: " + str(traceback.print_exc()))
    return wrapper_timer


def signal(func,*args, **kwargs):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        try:

           value = func(*args,**kwargs)
           return value
        except Exception as e:
           print("Error occurred.\n\t\t\tFunction: " + func.__name__ + "\n\t\t\tExcepion: " + str(e))
    return wrapper_timer


@signal
def check_fileextension(file,extension):
    if os.path.splitext(file)[1] == extension:
        return True
    else:
        return False


@signal
def getfilesinpath(inpath,extension="*"):
    '''
    Lists all files in a directory

    Args:
       inpath (str): absolute path of the directory directory

    Returns:
       filesinpath (str list): list of the absolute paths of the files in the directory "inpath"

    '''

    #list of the relative paths of the files within the directory "inpath", excluding nested directories
    filesinpath = filter(lambda f: os.path.isfile(os.path.join(inpath,f)), os.listdir(os.path.join(inpath)))

    if extension=="*":
        #list of the absolute paths of the files
        filesinpath = [os.path.join(inpath,file) for file in filesinpath]
    else:
        filesinpath = [os.path.join(inpath,file) for file in filesinpath if check_fileextension(file,extension)]
    return filesinpath


@signal
def copy_directory(src,dest):
    copy_tree(src,dest)


@signal
def rename_shpfiles(dir,old,new,shpfile_filetypes = set((".cpg",".dbf",".prj",".sbn",".sbx",".shp",".shp.xml","xml",".shx",".accdb"))):
    for file in os.listdir(dir):
        basename,fileextension = os.path.splitext(os.path.basename(file))
        cumulative_fileextension = fileextension
        while not fileextension=="":
            basename,fileextension = os.path.splitext(os.path.basename(basename))
            cumulative_fileextension=fileextension+cumulative_fileextension
        if basename == old and cumulative_fileextension in shpfile_filetypes:
            
            old_path = os.path.abspath(os.path.join(dir,file))
            new_path = os.path.abspath(os.path.join(dir,new+cumulative_fileextension))
            if not os.path.exists(new_path):
                os.rename(old_path,new_path)
            else:
                os.remove(old_path)


@signal
def replace_bymatchorkeep(match_str,old_str,new_str):    
    if old_str == match_str:
        return new_str
    else:
        return old_str


@signal
def get_place(previous_string,current_string):
        if previous_string != current_string:
            return True
        else:
            return False


@timer
def copyandremove_directory(src,dst):
    dst = os.path.join(dst,os.path.basename(src))
    try:
        sh.copytree(src,dst)
        sh.rmtree(src)
    except Exception as e:
        print(e)
        print("A realizacao {} nao foi movida para {}.".format(src,dst))



@timer
def save_state2json(data,fp):
    with open(fp,'w') as json_file:
        json.dump(data,  json_file,sort_keys=True)

@timer
def load_stateOfjson(fp):
    with open(fp, 'r') as json_file:
        data = json.load(json_file)
    return data

@timer
def retrieve_filewithextension(directory,extension):
        for file in os.listdir(directory):
            filename, file_extension = os.path.splitext(file)
            if file_extension == extension:
                shpfile = os.path.join(directory,file)
                break
        return filename



   
  