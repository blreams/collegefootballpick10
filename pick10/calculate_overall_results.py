#from calculator import *
#from database import *
#from calculate_week_results import *
#from overall_results import *
from database import Database
from calculate_week_results import CalculateWeekResults
from overall_results import OverallResults

class CalculateOverallResults:

    def __init__(self,year,completed_games,private_names=False,use_weeks=None):
        self.year = year
        self.completed_games = completed_games
        self.__use_private_names = private_names
        self.__week_numbers = use_weeks
        self.__calculate_overall_results()

    def get_results(self):
        return self.__results

    def __calculate_overall_results(self):
        self.__database = Database()

        overall_results = self.__setup_overall_results()

        week_numbers = self.__get_week_numbers()
        last_week_number = 0
        if len(week_numbers) > 0:
            last_week_number = week_numbers[-1]

        for week_number in week_numbers:
            last_week = week_number == last_week_number

            calc_week = CalculateWeekResults(self.year,week_number,self.__use_private_names)
            week_results = calc_week.get_results()
            week_winner_info = calc_week.get_winner_info()

            for week_result in week_results:
                self.__update_overall_results(week_result.player_id,overall_results,week_result,last_week,week_winner_info)

        self.__update_overall_results_unplayed_weeks(overall_results,last_week_number)
        self.__update_overall_results_win_pct(overall_results,last_week_number)

        overall_results = self.__convert_overall_results_to_list(overall_results)
        overall_results = self.assign_overall_rank(overall_results)
        overall_results = self.assign_overall_projected_rank(overall_results)
        overall_results = self.__sort_by_rank(overall_results)

        self.__results = overall_results

    def __setup_overall_results(self):
        players = self.__database.load_players(self.year)

        results = dict()
        for player_id in players:
            player = players[player_id]

            result = OverallResults()
            result.rank = 1
            result.projected_rank = 1
            result.player_id = player_id
            result.overall = 0
            result.projected = 0
            result.possible = 0
            result.week_points = []
            result.week_winner = []
            result.last_week_projected = 0
            result.last_week_possible = 0

            if self.__use_private_names:
                result.player_name = player.private_name
            else:
                result.player_name = player.public_name

            results[player_id] = result

        return results

    def __update_week_winner(self,player_id,overall_results,winner_info):
        if winner_info.official and winner_info.winner.id == player_id:
            overall_results[player_id].week_winner += [ True ]
        else:
            overall_results[player_id].week_winner += [ False ]

    def __update_overall_results(self,player_id,overall_results,week_result,last_week,winner_info):
        overall_results[player_id].overall += week_result.wins
        overall_results[player_id].projected += week_result.projected_wins
        overall_results[player_id].possible += week_result.possible_wins
        overall_results[player_id].week_points += [ week_result.wins ]

        self.__update_week_winner(player_id,overall_results,winner_info)

        if last_week:
            overall_results[player_id].last_week_projected = week_result.projected_wins
            overall_results[player_id].last_week_possible = week_result.possible_wins

    def __update_overall_results_unplayed_weeks(self,overall_results,last_week_number):
        number_of_weeks = 13
        number_of_points_per_week = 10

        assert last_week_number <= number_of_weeks, "Unexpected last week number %d, only expected %d weeks" % (last_week_number,number_of_weeks)

        number_of_unplayed_weeks = number_of_weeks - last_week_number
        number_of_points_left = number_of_points_per_week * number_of_unplayed_weeks
        for player_id in overall_results:
            overall_results[player_id].projected += number_of_points_left
            overall_results[player_id].possible += number_of_points_left

    def __update_overall_results_win_pct(self,overall_results,last_week_number):
        number_of_points_per_week = 10
        number_of_total_points_so_far = last_week_number * number_of_points_per_week

        for player_id in overall_results:
            if overall_results[player_id].overall == 0:
                win_pct = 0.0
            else:
                #win_pct = float(overall_results[player_id].overall) / float(number_of_total_points_so_far)
                win_pct = float(overall_results[player_id].overall) / float(self.completed_games)

            overall_results[player_id].win_pct = "%0.3f" % (win_pct)

    def __convert_overall_results_to_list(self,overall_results_dict):
        return overall_results_dict.values()

    def assign_overall_rank(self,results):
        sorted_results = sorted(results,key=lambda result:result.overall,reverse=True)

        assigned_results = []
        next_rank = 1   

        overall = sorted_results[0].overall

        for i,player_result in enumerate(sorted_results):

            overall_changed = player_result.overall != overall

            if overall_changed:
                next_rank = i+1
                player_result.rank = next_rank
                overall = player_result.overall
            else:
                player_result.rank = next_rank

            assigned_results.append(player_result)

        return assigned_results


    def assign_overall_projected_rank(self,results):
        sorted_results = sorted(results,key=lambda result:result.projected,reverse=True)

        assigned_results = []
        next_rank = 1   

        projected = sorted_results[0].projected

        for i,player_result in enumerate(sorted_results):

            projected_changed = player_result.projected != projected

            if projected_changed:
                next_rank = i+1
                player_result.projected_rank = next_rank
                projected = player_result.projected
            else:
                player_result.projected_rank = next_rank

            assigned_results.append(player_result)

        return assigned_results

    def __sort_by_rank(self,results):
        return sorted(results,key=lambda result:result.rank)

    def __get_week_numbers(self):
        if self.__week_numbers == None:
            return self.__database.get_week_numbers(self.year)
        return self.__week_numbers
