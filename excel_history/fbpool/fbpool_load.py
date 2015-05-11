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
import datetime

class FBPoolLoad:

    def __init__(self,url,excel_dir,excel_workbook,quiet=False):
        self.url = url
        self.excel_dir = excel_dir
        self.excel_workbook = excel_workbook
        self.__modify_player_name = FBPoolPlayerName("hide_lastname")
        self.__verbose = FBPoolVerbose(quiet)
        self.__start_times = dict()

    def __excel_full_path(self):
        return "%s/%s" % (self.excel_dir,self.excel_workbook)

    def load_missing_teams(self,year):
        excel = PoolSpreadsheet(year,self.__excel_full_path())
        teams = excel.get_teams()

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            for team in teams:
                fbpool_api.createTeamIfDoesNotExist(team.name,team.conference)
        except FBAPIException as e:
            FBPoolError.exit_with_error("teams",e)

    def load_teams(self,year):
        self.__verbose.start("loading teams from year %d..." % (year))

        if year == 2012:
            msg = "2012 spreadsheet has an error, Nevada appears twice, need to fix"
            FBPoolError.exit_with_error("loading teams",additional_message=msg)

        excel = PoolSpreadsheet(year,self.__excel_full_path())
        teams = excel.get_teams()

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            for team in teams:
                fbpool_api.createTeam(team.name,team.conference)
        except FBAPIException as e:
            import pdb; pdb.set_trace()
            FBPoolError.exit_with_error("teams",e)

        self.__verbose.done("load teams")

    def load_players(self,year):
        self.__verbose.start("loading players from year %d..." % (year))

        excel = PoolSpreadsheet(year,self.__excel_full_path())
        excel_players = excel.get_players()

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            for excel_player_name in excel_players:
                player_name = self.__modify_player_name.get_name(excel_player_name)
                player = fbpool_api.createPlayerIfDoesNotExist(player_name,[year])
                self.__add_year_to_player_if_missing(fbpool_api,year,player)
        except FBAPIException as e:
            FBPoolError.exit_with_error("players",e)

        self.__verbose.done("load players")

    def __load_week_games(self,excel,year,week_number):
        excel_games = excel.get_games(week_number)

        self.__verbose.update("week games...")

        batch = []
        try:
            fbpool_api = FBPoolAPI(url=self.url)

            for excel_game in excel_games.values():
                team1 = fbpool_api.getTeam(excel_game.team1) 
                team2 = fbpool_api.getTeam(excel_game.team2) 

                data = dict()
                data['number'] = excel_game.number
                data['team1'] = team1['key']
                data['team2'] = team2['key']
                data['team1_score'] = excel_game.team1_score
                data['team2_score'] = excel_game.team2_score
                data['favored'] = excel_game.favored
                data['spread'] = excel_game.spread
                data['state'] = excel_game.state
                data['quarter'] = None
                data['time_left'] = None
                data['date'] = None

                batch.append(data)

            # creating all games at once is faster than creating one at a time
            week_games = fbpool_api.createMultipleGames(year,week_number,batch)

        except FBAPIException as e:
            FBPoolError.exit_with_error("week games",e)

        return week_games

    def __get_week_winner(self,excel,week):
        winner_name = excel.get_week_winner(week)
        if winner_name == None:
            return None

        winner_name = self.__modify_player_name.get_name(winner_name)

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            player = fbpool_api.getPlayer(winner_name)
            return player['key']
        except FBAPIException as e:
            FBPoolError.exit_with_error("week games",e)

        return None

    def __find_game_number(self,games,number):
        for game in games:
            if game['number'] == number:
                return game
        additional_message = "could not find game number %d" % (number)
        FBPoolError.exit_with_error("loading games",additional_message)


    def __load_week_picks(self,excel,week,week_games,batch_size=10):
        excel_picks = excel.get_picks(week['number'])

        self.__verbose.update("week picks...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)

            players = fbpool_api.getPlayersInYear(week['year'])
            player_lookup = { player['name']:player for player in players }

            batch = []
            number_of_picks = len(excel_picks)
            last_pick = number_of_picks - 1
            for i,excel_pick in enumerate(excel_picks):

                name = self.__modify_player_name.get_name(excel_pick.player_name)
                player = player_lookup[name]
                game = self.__find_game_number(week_games,excel_pick.game_number)

                data = dict()
                data['week'] = week['key']
                data['player'] = player['key']
                data['game'] = game['key']

                if excel_pick.default:
                    data['winner'] = None
                    data['team1_score'] = None
                    data['team2_score'] = None
                else:
                    data['winner'] = excel_pick.winner
                    data['team1_score'] = excel_pick.team1_score
                    data['team2_score'] = excel_pick.team2_score

                batch.append(data)

                # creating a batch of picks is faster than creating one pick at a time
                batch_size_reached = (len(batch) % batch_size) == 0
                if batch_size_reached or i == last_pick:
                    picks = fbpool_api.createMultiplePicks(week['year'],week['number'],batch)
                    self.__verbose.update_every("week picks...",i,batch_size,number_of_picks)
                    batch = []

        except FBAPIException as e:
            FBPoolError.exit_with_error("week picks",e)


    def load_week(self,year,week,load_teams_and_players=True,update_memcache=True):
        self.__record_start_time("load week")
        self.__verbose.start("loading year %d week %d..." % (year,week))

        if load_teams_and_players:
            self.__verbose.update("verifying week teams and players are loaded...")
            self.load_missing_teams(year)
            self.load_players(year)

        excel = PoolSpreadsheet(year,self.__excel_full_path())

        week_games = self.__load_week_games(excel,year,week)
        winner_key = self.__get_week_winner(excel,week)

        week_data = dict()
        week_data['year'] = year
        week_data['number'] = week
        week_data['winner'] = winner_key
        week_data['games'] = [ game['key'] for game in week_games ]
        week_data['lock_picks'] = None
        week_data['lock_scores'] = None

        self.__verbose.update("week object...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            created_week = fbpool_api.createWeek(week_data)
        except FBAPIException as e:
            FBPoolError.exit_with_error("week",e)

        self.__load_week_picks(excel,created_week,week_games)

        self.__verbose.update("cleaning up...")

        try:
            fbpool_api.deletePicksCache()
            fbpool_api.deleteGamesCache()
            fbpool_api.deleteWeeksCache()
        except FBAPIException as e:
            additional_message = "Not stopping because of exception..."
            FBPoolError.error_no_exit("deleting api cache",e,additional_message)

        if update_memcache:
            self.__verbose.update("updating memcache...")

            try:
                fbpool_api.updateCacheForWeek(year,week)
            except FBAPIException as e:
                additional_message = "Not stopping because of exception..."
                FBPoolError.error_no_exit("updating memcache",e,additional_message)

        self.__display_duration("load week")
        self.__verbose.done("load week %d" % (week))


    def load_year(self,year,load_teams_in_year=True,load_players_in_year=True):
        self.__record_start_time("load year")

        self.__verbose.start("loading year %d..." % (year))

        excel = PoolSpreadsheet(year,self.__excel_full_path())
        week_numbers = excel.get_week_numbers()

        if load_teams_in_year:
            self.__verbose.update("verifying teams are loaded...")
            self.load_missing_teams(year)

        if load_players_in_year:
            self.__verbose.update("verifying players are loaded...")
            self.load_players(year)

        for week_number in week_numbers:
            self.load_week(year,week_number,load_teams_and_players=False,update_memcache=False)

        self.__verbose.update("cleaning up...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            fbpool_api.deletePlayersCache()
        except FBAPIException as e:
            additional_message = "Not stopping because of exception..."
            FBPoolError.error_no_exit("deleting player api cache",e,additional_message)

        self.__verbose.update("updating memcache...")

        try:
            fbpool_api.updateCacheForYear(year)
        except FBAPIException as e:
            additional_message = "Not stopping because of exception..."
            FBPoolError.error_no_exit("updating memcache",e,additional_message)

        self.__display_duration("load year")
        self.__verbose.done("load year")


    def __add_year_to_player_if_missing(self,fbpool_api,year,player):
        if year not in player['years']:
            data = { "years":player['years'] + [year] }
            fbpool_api.editPlayerByKey(player['key'],data)

    def __record_start_time(self,name):
        self.__start_times[name] = datetime.datetime.now()

    def __display_duration(self,name):
        end_time = datetime.datetime.now()
        duration = end_time - self.__start_times[name]
        del self.__start_times[name]
        print "%s duration %s" % (name,duration)

