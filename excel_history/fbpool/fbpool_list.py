ROOT_PATH = '../../.'
import sys
sys.path.append(ROOT_PATH)

from scripts.api.fbpool_api import *
from scripts.api.fbpool_api_exception import *
from fbpool_error import *
from fbpool_verbose import *
import string

class FBPoolList:

    def __init__(self,url,quiet=False):
        self.url = url
        self.__verbose = FBPoolVerbose(quiet)

    def list_all_teams(self):
        self.__verbose.start("reading teams from database...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            teams = fbpool_api.getAllTeams()
        except FBAPIException as e:
            FBPoolError.exit_with_error("list all teams",e,"error getting teams")

        teams_sorted = sorted(teams,key=lambda team:team['name'])

        print("")
        print("Teams: (%d)" % (len(teams_sorted)))
        print("----------------------------------------------------------------------------------")
        for team in teams_sorted:
            print("%-40s %s" % (team['name'],team['conference']))
        print("----------------------------------------------------------------------------------")
        print("")

    def list_all_players(self):
        self.__verbose.start("reading players from database...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            players = fbpool_api.getAllPlayers()
        except FBAPIException as e:
            FBPoolError.exit_with_error("list all players",e,"error getting players")

        players_sorted = sorted(players,key=lambda player:player['name'])

        print("")
        print("Players:")
        print("----------------------------------------------------------------------------------")
        for player in players_sorted:
            print("%-40s %s" % (player['name'],self.__array_str(player['years'])))
        print("----------------------------------------------------------------------------------")
        print("")


    def list_all_weeks(self):
        self.__verbose.start("reading weeks from database...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            weeks = fbpool_api.getAllWeeks()
        except FBAPIException as e:
            FBPoolError.exit_with_error("list all weeks",e,"error getting weeks")

        years = sorted(set([week['year'] for week in weeks ]))

        print("")
        print("Weeks:")
        print("----------------------------------------------------------------------------------")
        for year in years:
            numbers = sorted([ week['number'] for week in weeks if week['year'] == year])

            for week_number in numbers:
                print("%d Week %d" % (year,week_number))

            print("")

        print("----------------------------------------------------------------------------------")
        print("")

    def list_player_picks(self,year,week_number,player_name):
        self.__verbose.start("reading player picks from database...")

        # get the picks
        try:
            fbpool_api = FBPoolAPI(url=self.url)
            picks = fbpool_api.getPlayerPicks(year,week_number,player_name)
        except FBAPIException as e:
            FBPoolError.exit_with_error("list player picks",e,"error getting picks")


        # get team name for each game pick
        try:
            game_picks = dict()
            for pick in picks:
                game_key = pick['game']
                game = fbpool_api.getGameByKey(game_key)
                game_number = game['number']

                if pick['winner'] == "team1":
                    team1_key = game['team1']
                    team1 = fbpool_api.getTeamByKey(team1_key)
                    game_picks[game_number] = team1['name']
                elif pick['winner'] == "team2":
                    team2_key = game['team2']
                    team2 = fbpool_api.getTeamByKey(team2_key)
                    game_picks[game_number] = team2['name']
                else:
                    game_picks[game_number] = "No Pick Made."

        except FBAPIException as e:
            FBPoolError.exit_with_error("list player picks",e,"error getting games")

        print("")
        print("%s Picks for %d Week %d:" % (player_name,year,week_number))
        print("----------------------------------------------------------------------------------")
        game_numbers = sorted(game_picks.keys())
        for game_number in game_numbers:
            if game_number < 10:
                print("Game  %d: %s" % (game_number,game_picks[game_number]))
            else:
                print("Game %d: %s" % (game_number,game_picks[game_number]))

        print("----------------------------------------------------------------------------------")
        print("")

    def list_week_games(self,year,week_number):
        self.__verbose.start("reading week games from database...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            week = fbpool_api.getWeek(year,week_number)

            game_teams = dict()
            for game_key in week['games']:
                game = fbpool_api.getGameByKey(game_key)
                game_number = game['number']

                team1_key = game['team1']
                team1 = fbpool_api.getTeamByKey(team1_key)

                team2_key = game['team2']
                team2 = fbpool_api.getTeamByKey(team2_key)

                game_teams[game_number] = (team1['name'],team2['name'])

        except FBAPIException as e:
            FBPoolError.exit_with_error("list week games",e)

        print("")
        print("%d Week %d Games:" % (year,week_number))
        print("----------------------------------------------------------------------------------")
        game_numbers = sorted(game_teams.keys())
        for game_number in game_numbers:

            teams = game_teams[game_number]
            team1 = teams[0]
            team2 = teams[1]

            if game_number < 10:
                print("Game  %d: %s vs. %s" % (game_number,team1,team2))
            else:
                print("Game %d: %s vs. %s" % (game_number,team1,team2))

        print("----------------------------------------------------------------------------------")
        print("")

    def __array_str(self,a):
        s = ""
        last = len(a)-1
        for i in range(last+1):
            if i == last:
                s += str(a[i])
            else:
                s += "%s, " % (a[i])
        return s

