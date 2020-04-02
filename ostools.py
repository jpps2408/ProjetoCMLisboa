import os
import functools
import time
from distutils.dir_util import copy_tree

def timer(func,*args, **kwargs):
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



def check_fileextension(file,extension):
    if os.path.splitext(file)[1] == extension:
        return True
    else:
        return False


@timer
def getfilesinpath(inpath,extension="*"):
    '''
    Lists all files in a directory

    Args:
       inpath (str): absolute path of the directory directory

    Returns:
       filesinpath (str list): list of the absolute paths of the files in the directory "inpath"

    '''

    #list of the relative paths of the files within the directory "inpath", excluding nested directories
    filesinpathlist = filter(lambda f: os.path.isfile(os.path.join(inpath,f)), os.listdir(os.path.join(inpath)))

    if extension=="*":
        #list of the absolute paths of the files
        filesinpath = [os.path.join(inpath,file) for file in filesinpathlist]
    else:
        filesinpath = [os.path.join(inpath,file) for file in filesinpathlist if check_fileextension(file,extension)]
    return filesinpath


@timer
def copy_directory(src,dest):
    copy_tree(src,dest)

