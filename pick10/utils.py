import datetime
import time

def get_timestamp(datetime_value):
    return time.mktime(datetime_value.timetuple())

