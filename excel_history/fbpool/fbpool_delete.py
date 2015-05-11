ROOT_PATH = '../../.'
import sys
sys.path.append(ROOT_PATH)

from scripts.api.fbpool_api import *
from scripts.api.fbpool_api_exception import *
from scripts.excel.pool_spreadsheet import *
from scripts.excel.team import *
from fbpool_player_name import *
from fbpool_error import *
from fbpool_verbose import *
import string

class FBPoolDelete:

    def __init__(self,url,quiet=False):
        self.url = url
        self.__verbose = FBPoolVerbose(quiet)

    def delete_year(self,year):
        self.__verbose.start("deleting year %d..." % (year))

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            weeks = fbpool_api.getWeeksInYear(year)
        except FBAPIException as e:
            msg = "could not get weeks in %d" % (year)
            FBPoolError.delete_error("year",e,msg)

        for week in weeks:
            self.__verbose.update("deleting %d week %d..." % (year,week['number']))
            self.__delete_week(fbpool_api,week)

        self.__verbose.done("deleting year")


    def delete_week(self,year,week_number):
        self.__verbose.start("deleting year %d week %d..." % (year,week_number))

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            week = fbpool_api.getWeek(year,week_number)
        except FBAPIException as e:
            msg = "could not get %d week %d" % (year,week_number)
            FBPoolError.delete_error("week",e,msg)

        self.__delete_week(fbpool_api,week)

        self.__verbose.done("deleting week")

    def __delete_week(self,fbpool_api,week):
        year = week['year']
        week_number = week['number']

        # try to delete as many games as possible, ignore errors
        self.__verbose.update("deleting week games...")

        for game_key in week['games']:
            try:
                fbpool_api.deleteGameByKey(game_key)
            except FBAPIException as e:
                FBPoolError.error_no_exit("delete week",e,"error deleting week game")
                continue

        # try to delete as many picks as possible, ignore errors
        self.__verbose.update("deleting week picks...")

        try:
            picks = fbpool_api.getWeekPicks(year,week_number)
        except FBAPIException as e:
            picks = None

        if picks != None:
            number_of_picks = len(picks)
            for i,pick in enumerate(picks):
                self.__verbose.update_every("deleting week picks",i,50,number_of_picks)

                try:
                    fbpool_api.deletePickByKey(pick['key'])
                except FBAPIException as e:
                    FBPoolError.error_no_exit("delete week",e,"error deleting week pick")
                    continue

        # finally try and delete the week
        try:
            fbpool_api.deleteWeekByKey(week['key'])
        except FBAPIException as e:
            msg = "could not delete %d week %d" % (year,week_number)
            FBPoolError.delete_error("week",e,msg)


    def delete_teams(self):
        self.__verbose.start("deleting all teams...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            fbpool_api.deleteAllTeams()
        except FBAPIException as e:
            FBPoolError.delete_error("teams",e)

        self.__verbose.done("deleting teams")

    def delete_players(self):
        self.__verbose.start("deleting all players...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            fbpool_api.deleteAllPlayers()
        except FBAPIException as e:
            FBPoolError.delete_error("players",e)

        self.__verbose.done("deleting players")

    def delete_players_from_year(self,year):
        self.__verbose.start("deleting players from %d..." % (year))

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            players = fbpool_api.getPlayersInYear(year)
            for player in players:
                year_not_in_player = 'years' not in player or year not in player['years']
                if year_not_in_player:
                    continue

                if len(player['years']) == 1:
                    fbpool_api.deletePlayerByKey(player['key'])
                else:
                    data = dict()
                    data['years'] = players['years']
                    data['years'].remove(year)
                    fbpool_api.editPlayerByKey(player['key'],data)

        except FBAPIException as e:
            FBPoolError.delete_error("players",e)

        self.__verbose.done("deleting players")


    def delete_all(self):
        self.__verbose.start("deleting entire database...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)

            self.__verbose.update("deleting teams...")
            fbpool_api.deleteAllTeams()

            self.__verbose.update("deleting players...")
            fbpool_api.deleteAllPlayers()

            self.__verbose.update("deleting weeks...")
            fbpool_api.deleteAllWeeks()

            self.__verbose.update("deleting games...")
            fbpool_api.deleteAllGames()

            self.__verbose.update("deleting picks...")
            fbpool_api.deleteAllPicks()

            self.__verbose.update("flushing memcache...")
            fbpool_api.deleteCache()

        except FBAPIException as e:
            FBPoolError.delete_error("database",e)

        self.__verbose.done("deleting database")

