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


def tintervalns2hour(nstime):
    return nstime.total_seconds()/3600

def string2hour(nstime):
    nstime = string2deltatime(nstime)
    return nstime.total_seconds()/3600

