from pick_data import *
from database import *

class EnterPicks:

    def __init__(self,year,week_number,player_id):
        self.year = year
        self.week_number = week_number
        self.player_id = player_id

    def get_game_picks(self):
        database = Database()
        week_data = database.load_week_data(self.year,self.week_number)

        player_already_picked = self.player_id in week_data.player_picks
        if player_already_picked:
            picks = { pick.game.gamenum:pick for pick in week_data.player_picks[self.player_id] }

        game_picks = []
        for game in week_data.games.values():
            data = PickData()
            data.number = game.gamenum
            data.team1 = game.team1.team_name
            data.team2 = game.team2.team_name

            if player_already_picked:
                data.pick = picks[game.gamenum].winner
            else:
                data.pick = 0

            if game.favored == TEAM1:
                data.team1_spread = game.spread
                data.team2_spread = ""
            elif game.favored == TEAM2:
                data.team1_spread = ""
                data.team2_spread = game.spread
            else:
                raise AssertionError,"Invalid favored value"

            if game.gamenum == 10:
                if player_already_picked:
                    data.team1_predicted_points = picks[game.gamenum].team1_predicted_points
                    data.team2_predicted_points = picks[game.gamenum].team2_predicted_points
                else:
                    data.team1_predicted_points = -1
                    data.team2_predicted_points = -1

            game_picks.append(data)

        return sorted(game_picks,key=lambda pick:pick.number)

