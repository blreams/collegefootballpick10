from pick10.player_results import *
from pick10.database import *
from pick10.calculator import *

class CalculatePlayerResults:

    def __init__(self,year,week_number,player_id,private_names=False):
        self.year = year
        self.week_number = week_number
        self.player_id = player_id
        self.__use_private_names = private_names
        self.__calculate_player_results()

    def get_player_summary(self):
        return self.__results

    def get_results(self):
        return self.__results

    def __calculate_player_results(self):
        database = Database()
        self.__week_data = database.load_week_data(self.year,self.week_number)
        self.__calc = CalculateResults(self.__week_data)

        assert self.player_id in self.__week_data.players,"Bad player id"
        self.__player = self.__week_data.players[self.player_id]

        self.__calculate_player_summary()
        self.__calculate_player_game_results_sorted_by_game_number()

    def __calculate_player_summary(self):
        summary = PlayerSummary()
        summary.player_id = self.player_id
        summary.wins = self.__calc.get_number_of_wins(self.__player)
        summary.losses = self.__calc.get_number_of_losses(self.__player)
        summary.win_pct = self.__calc.get_win_percent_string(self.__player)
        summary.possible_wins = self.__calc.get_number_of_possible_wins(self.__player)
        summary.projected_wins = self.__calc.get_number_of_projected_wins(self.__player)
        summary.week_state = self.__calc.get_summary_state_of_all_games()

        if self.__use_private_names:
            summary.player_name = self.__player.private_name
        else:
            summary.player_name = self.__player.public_name

        self.__summary = summary

    def __calculate_player_game_results_sorted_by_game_number(self):
        game_results = [None]*10
        for game_number in self.__week_data.games:
            game = self.__week_data.games[game_number]
            result = self.__calculate_player_game_result(game)
            game_results[game_number-1] = result
        self.__results = game_results

    def __calculate_player_game_result(self,game):
        result = PlayerResult()
        result.player_pick = self.__calc.get_team_name_player_picked_to_win(self.__player,game)
        result.result = self.__calc.get_game_result_string(self.__player,game)
        result.team1 = game.team1.team_name
        result.team2 = game.team2.team_name
        result.game_state = game.game_state
        result.favored = self.__calc.get_favored_team_name(game)
        result.favored_spread = game.spread
        result.game_date = game.kickoff

        if game.game_state == FINAL:
            result.team1_score = game.team1_actual_points
            result.team2_score = game.team2_actual_points
            result.winning_team = self.__calc.get_game_winner_team_name(game)
            result.game_spread = self.__calc.get_game_score_spread(game)
        elif game.game_state == IN_PROGRESS:
            result.team1_score = game.team1_actual_points
            result.team2_score = game.team2_actual_points
            result.winning_team = self.__calc.get_team_name_winning_game(game)
            result.game_spread = self.__calc.get_game_score_spread(game)
            result.game_quarter = game.quarter
            result.game_time_left = game.time_left
        elif game.game_state == NOT_STARTED:
            result.team1_actual_points = ''
            result.team2_actual_points = ''
        else:
            raise AssertionError,"Game state %s is not valid" % (game.game_state)

        return result

