ROOT_PATH = '../../.'
import sys
sys.path.append(ROOT_PATH)

from scripts.api.fbpool_api import *
from scripts.api.fbpool_api_exception import *
from scripts.excel.pool_spreadsheet import *
from fbpool_player_name import *
from fbpool_error import *
from fbpool_verbose import *
import string

class FBPoolCache:

    def __init__(self,url,quiet=False):
        self.url = url
        self.__verbose = FBPoolVerbose(quiet)

    def cleanup_api(self):
        self.__verbose.start("Flushing API data from the memcache...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            fbpool_api.deletePicksCache()
            fbpool_api.deleteGamesCache()
            fbpool_api.deleteWeeksCache()
            fbpool_api.deletePlayersCache()
        except FBAPIException as e:
            FBPoolError.error_no_exit("flushing api cache",e)

        self.__verbose.done("flushing API cache")

    def flush_memcache(self):
        self.__verbose.start("flushing entire memcache...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            fbpool_api.deleteCache()
        except FBAPIException as e:
            FBPoolError.error_no_exit("flushing memcache",e)

        self.__verbose.done("flushing memcache")

    def load_memcache(self):
        self.__verbose.start("loading entire memcache...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            fbpool_api.updateCache()
        except FBAPIException as e:
            FBPoolError.error_no_exit("loading memcache",e)

        self.__verbose.done("loading memcache")

    def load_memcache_for_year(self,year):
        self.__verbose.start("loading %d into memcache..." % (year))

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            fbpool_api.updateCacheForYear(year)
        except FBAPIException as e:
            FBPoolError.error_no_exit("loading year in memcache",e)

        self.__verbose.done("loading memcache")

    def load_memcache_for_week(self,year,week_number):
        self.__verbose.start("loading %d week %d into memcache..." % (year,week_number))

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            fbpool_api.updateCacheForWeek(year,week_number)
        except FBAPIException as e:
            FBPoolError.error_no_exit("loading week in memcache",e)

        self.__verbose.done("loading memcache")

