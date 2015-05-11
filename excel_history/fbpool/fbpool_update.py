ROOT_PATH = '../../.'
import sys
sys.path.append(ROOT_PATH)

from scripts.api.fbpool_api import *
from scripts.api.fbpool_api_exception import *
from scripts.excel.pool_spreadsheet import *
from scripts.excel.team import *
from fbpool_error import *
from fbpool_verbose import *
from fbpool_player_name import *
import string

class FBPoolUpdate:

    def __init__(self,url,excel_dir,excel_workbook,quiet=False):
        self.url = url
        self.excel_dir = excel_dir
        self.excel_workbook = excel_workbook
        self.__verbose = FBPoolVerbose(quiet)
        self.__modify_player_name = FBPoolPlayerName("hide_lastname")

    def __excel_full_path(self):
        return "%s/%s" % (self.excel_dir,self.excel_workbook)

    def update_week(self,year,week_number):
        self.__verbose.start("updating results for year %d week %d..." % (year,week_number))

        excel = PoolSpreadsheet(year,self.__excel_full_path())

        excel_player_name = excel.get_week_winner(week_number)
        if excel_player_name == None:
            week_winner_name = None
        else:
            week_winner_name = self.__modify_player_name.get_name(excel_player_name)

        excel_games = excel.get_games(week_number)

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            week = fbpool_api.getWeek(year,week_number)

            # update the week winner
            if week_winner_name == None and week['winner'] != None:
                edit_data = dict()
                edit_data['winner'] = None
                fbpool_api.editWeekByKey(week['key'],edit_data)
            elif week_winner_name != None:
                player = fbpool_api.getPlayer(week_winner_name)
                winner_key = player['key']
                winner_changed = winner_key != week['winner']
                if winner_changed:
                    edit_data = dict()
                    edit_data['winner'] = winner_key
                    fbpool_api.editWeekByKey(week['key'],edit_data)

            # update the game info
            for game_key in week['games']:
                game = fbpool_api.getGameByKey(game_key)
                excel_game = excel_games.get(game['number'])
                if excel_game == None:
                    continue

                edit_data = dict()
                edit_data['team1_score'] = excel_game.team1_score
                edit_data['team2_score'] = excel_game.team2_score
                edit_data['state'] = excel_game.state

                fbpool_api.editGameByKey(game_key,edit_data)

            # update the cache
            self.__verbose.update("updating memcache...")
            fbpool_api.updateCacheForWeek(year,week_number)

        except FBAPIException as e:
            FBPoolError.exit_with_error("updating week",e)

        self.__verbose.done("updating week")
