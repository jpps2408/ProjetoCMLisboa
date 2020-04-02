import datetime
import time
import functools
from ostools import *


def string2datetime(time_string):
    dtime_obj = datetime.datetime.strptime(time_string , '%Y-%m-%d %H:%M:%S')
    return dtime_obj


def string2deltatime(time_string):
    dtime_obj = datetime.datetime.strptime(time_string , '%H:%M:%S') - datetime.datetime(1900, 1, 1, 0, 0, 0)
    return dtime_obj


def datetime2string(datetime_obj):
    time_convertible_str = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    return time_convertible_str


def tinterval_string(timediff):
    totalMinute, second = divmod(timediff.seconds, 60)
    hour, minute = divmod(totalMinute, 60)
    timediff_string = str(hour) + ':' + str(minute) + ':' + str(second)
    return timediff_string


def Cartrack2Time(descriptionstring,splitsep):
    try:
        #These are hardocded values: 4th place in the list, oly after the 6th character
        string_list = descriptionstring.split(splitsep)
        time_string_1 = [string for string in string_list if 'Time' in string]
        time_string = time_string_1[0][6:]
        dtime_string = time_string[0:-3]
        datetime_obj = string2datetime(dtime_string)

        offset_string = time_string[-2:]
        #convert the time offset string to a timedelta object
        offset_obj = datetime.timedelta(hours=int(offset_string))

        #offset the time based on the +00 or +01 part of the string, so as to make times with different offsets comparables
        time_convertible = datetime_obj + offset_obj
    
    except exception as identifier:
       print('\n exception at Cartrack2Time')
    return time_convertible

def tintervalns2hour(nstime):
    return nstime.total_seconds()/3600
