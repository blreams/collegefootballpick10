from game_data import *
from database import *

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
