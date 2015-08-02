from game_data import *
from database import *
from models import *
from calculator import *

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
            data.team1_score = game.team1_actual_points if game.team1_actual_points != None else ""
            data.team2_score = game.team2_actual_points if game.team2_actual_points != None else ""
            data.state = game.game_state
            data.quarter = game.quarter if game.quarter != None else ""
            data.time_left = game.time_left if game.time_left != None else ""
            data.date = game.kickoff
            games.append(data)

        return sorted(games,key=lambda game:game.number)

    def update_games(self,games):
        for game_info in games:
            game = get_game(self.year,self.week_number,game_info.number)
            game.team1_actual_points = game_info.team1_score
            game.team2_actual_points = game_info.team2_score
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
                raise AssertionError,"Unexpected game state value: %s" % (game_state)

            if game_state == "final":
                game.winner = CalculateResults(None).get_pool_game_winner(game)
            else:
                game.winner = 0

            game.save()

            # TODO set kickoff here?  or set kickoff when creating games?
