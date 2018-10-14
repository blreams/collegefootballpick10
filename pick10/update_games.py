from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

from .game_data import GameData
from .database import Database
from .models import get_week, get_game
from .calculator import CalculateResults
from .calculator import NOT_STARTED, IN_PROGRESS, FINAL

class UpdateGames:

    def __init__(self,year,week_number):
        self.year = year
        self.week_number = week_number

    def get_games(self):
        database = Database()
        week_data = database.load_week_data(self.year,self.week_number)

        games = []
        for game in week_data.games.values():
            data = GameData()
            data.number = game.gamenum
            data.team1 = game.team1.team_name
            data.team2 = game.team2.team_name
            data.team1_score = self.__get_team1_score(game)
            data.team2_score = self.__get_team2_score(game)
            data.state = game.game_state
            data.quarter = self.__get_quarter(game)
            data.time_left = self.__get_time_left(game)
            data.date = game.kickoff
            games.append(data)

        return sorted(games,key=lambda game:game.number)

    def update_games(self,games):
        for game_info in games:
            game = get_game(self.year,self.week_number,game_info.number)
            game.team1_actual_points = game_info.team1_score if game_info.team1_score != '' else -1
            game.team2_actual_points = game_info.team2_score if game_info.team2_score != '' else -1
            game.quarter = game_info.quarter
            game.time_left = game_info.time_left

            game_state = game_info.state
            if game_state == "not_started":
                game.game_state = NOT_STARTED
            elif game_state == "in_progress":
                game.game_state = IN_PROGRESS
            elif game_state == "final":
                game.game_state = FINAL
            else:
                raise AssertionError("Unexpected game state value: %s" % (game_state))

            if game_state == "final":
                game.winner = CalculateResults(None).get_pool_game_winner(game)
            else:
                game.winner = 0

            game.save()

            # TODO not entirely sure about this, but if the update games page gets submitted,
            # change the Week.winner field to None since it will no longer be accurate
            # if any scores were changed
            week = get_week(self.year,self.week_number)
            week.winner = None
            week.save()

    def __get_team1_score(self,game):
        valid_score = game.team1_actual_points != None and game.team1_actual_points >= 0
        return game.team1_actual_points if valid_score else ""

    def __get_team2_score(self,game):
        valid_score = game.team2_actual_points != None and game.team2_actual_points >= 0
        return game.team2_actual_points if valid_score else ""

    def __get_quarter(self,game):
        if game.game_state == IN_PROGRESS:
            return game.quarter if game.quarter != None else ""
        else:
            return ""

    def __get_time_left(self,game):
        if game.game_state == IN_PROGRESS:
            return game.time_left if game.time_left != None else ""
        else:
            return ""
