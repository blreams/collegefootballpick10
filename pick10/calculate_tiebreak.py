from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

from .week_winner import WeekWinner
from .database import Database
from .calculator import CalculateResults
from .calculator import NOT_STARTED, IN_PROGRESS, FINAL
from .tiebreak_data import TiebreakSummary, Tiebreak1Summary, Tiebreak2Summary, Tiebreak3Summary, Tiebreak0Data, Tiebreak1Data, Tiebreak2Data, Tiebreak3Data

class CalculateTiebreak:

    def __init__(self,year,week_number,private_names=False):

        self.__use_private_names = private_names

        database = Database()

        self.__winners = WeekWinner(year,week_number)
        self.__week_data = database.load_week_data(year,week_number)
        self.__calc = CalculateResults(self.__week_data)

        self.__calculate_tiebreak_summary_details()
        self.__calculate_tiebreaker0_details()
        self.__calculate_tiebreaker1_details()
        self.__calculate_tiebreaker2_details()
        self.__calculate_tiebreaker3_details()

    def was_able_to_determine_winner(self):
        return self.__winners.is_winner_valid()

    def get_tiebreaker_summary(self):
        return self.__tiebreak_summary

    def get_tiebreaker0_details(self):
        return self.__tiebreak0_details

    def get_tiebreaker1_details(self):
        return self.__tiebreak1_details

    def get_tiebreaker2_details(self):
        return self.__tiebreak2_details

    def get_tiebreaker3_details(self):
        return self.__tiebreak3_details

    def get_tiebreaker1_summary(self):
        return self.__tiebreak1_summary

    def get_tiebreaker2_summary(self):
        return self.__tiebreak2_summary

    def get_tiebreaker3_summary(self):
        return self.__tiebreak3_summary

    def __calculate_tiebreak_summary_details(self):
        details = dict()

        winner_data = self.__winners.get_week_winner_data()
        if winner_data.featured_game.game_state == NOT_STARTED:
            self.__tiebreak_summary = []
            return

        players = self.__winners.get_players_tied_for_first()
        for player_id in players:
            d = TiebreakSummary()
            d.player_id = player_id
            d.player_name = self.__get_player_name(player_id)

            d.number_of_tiebreaks = 0
            d.tiebreak0 = ""
            d.tiebreak1 = ""
            d.tiebreak2 = ""
            d.tiebreak3 = ""

            details[player_id] = d

        t0_players_won = self.__winners.get_players_that_won_tiebreak_0()
        t0_players_lost = self.__winners.get_players_that_lost_tiebreak_0()
        t1_players_won = self.__winners.get_players_that_won_tiebreak_1()
        t1_players_lost = self.__winners.get_players_that_lost_tiebreak_1()
        t2_players_won = self.__winners.get_players_that_won_tiebreak_2()
        t2_players_lost = self.__winners.get_players_that_lost_tiebreak_2()
        t3_players_won = self.__winners.get_players_that_won_tiebreak_3()
        t3_players_lost = self.__winners.get_players_that_lost_tiebreak_3()

        if t0_players_won != None:
            for player_id in t0_players_won:
                result = self.__get_tiebreak_result("win")
                css_id = self.__get_tiebreak_id(result)

                details[player_id].tiebreak0 = result
                details[player_id].tiebreak0_id = css_id
                details[player_id].number_of_tiebreaks += 1

        if t0_players_lost != None:
            for player_id in t0_players_lost:
                result = self.__get_tiebreak_result("loss")
                css_id = self.__get_tiebreak_id(result)

                details[player_id].tiebreak0 = result
                details[player_id].tiebreak0_id = css_id
                details[player_id].number_of_tiebreaks += 1


        if t1_players_won != None:
            for player_id in t1_players_won:
                result = self.__get_tiebreak_result("win")
                css_id = self.__get_tiebreak_id(result)

                details[player_id].tiebreak1 = result
                details[player_id].tiebreak1_id = css_id
                details[player_id].number_of_tiebreaks += 1

        if t1_players_lost != None:
            for player_id in t1_players_lost:
                result = self.__get_tiebreak_result("loss")
                css_id = self.__get_tiebreak_id(result)
    
                details[player_id].tiebreak1 = result
                details[player_id].tiebreak1_id = css_id
                details[player_id].number_of_tiebreaks += 1

        if t2_players_won != None:
            for player_id in t2_players_won:
                result = self.__get_tiebreak_result("win")
                css_id = self.__get_tiebreak_id(result)
    
                details[player_id].tiebreak2 = result
                details[player_id].tiebreak2_id = css_id
                details[player_id].number_of_tiebreaks += 1

        if t2_players_lost != None:
            for player_id in t2_players_lost:
                result = self.__get_tiebreak_result("loss")
                css_id = self.__get_tiebreak_id(result)
    
                details[player_id].tiebreak2 = result
                details[player_id].tiebreak2_id = css_id
                details[player_id].number_of_tiebreaks += 1

        if t3_players_won != None:
            for player_id in t3_players_won:
                result = self.__get_tiebreak_result("win")
                css_id = self.__get_tiebreak_id(result)
    
                details[player_id].tiebreak3 = result
                details[player_id].tiebreak3_id = css_id
                details[player_id].number_of_tiebreaks += 1

        if t3_players_lost != None:
            for player_id in t3_players_lost:
                result = self.__get_tiebreak_result("loss")
                css_id = self.__get_tiebreak_id(result)
    
                details[player_id].tiebreak3 = result
                details[player_id].tiebreak3_id = css_id
                details[player_id].number_of_tiebreaks += 1

        self.__tiebreak_summary = self.__sort_tiebreak_summary(details.values())

    def __calculate_tiebreaker0_details(self):
        details = []

        winner_data = self.__winners.get_week_winner_data()
        featured_game = winner_data.featured_game

        if winner_data.featured_game.game_state == NOT_STARTED:
            self.__tiebreak0_details = []
            return

        players = self.__winners.get_players_that_won_tiebreak_0()
        if players != None:
            for player_id in players:
                player = self.__week_data.players[player_id]

                result = self.__get_tiebreak_result("win")
                css_id = self.__get_tiebreak_id(result)
    
                d = Tiebreak0Data()
                d.player_id = player_id
                d.player_name = self.__get_player_name(player_id)
                d.result = result
                d.result_id = css_id
                d.featured_game_winner = self.__get_featured_game_winner()

                if self.__calc.player_did_not_pick(player,featured_game):
                    d.player_pick = 'n/a'
                else:
                    d.player_pick = self.__calc.get_team_name_player_picked_to_win(player,featured_game)

                details.append(d)

        players = self.__winners.get_players_that_lost_tiebreak_0()
        if players != None:
            for player_id in players:
                player = self.__week_data.players[player_id]

                result = self.__get_tiebreak_result("loss")
                css_id = self.__get_tiebreak_id(result)
    
                d = Tiebreak0Data()
                d.player_id = player_id
                d.player_name = self.__get_player_name(player_id)
                d.result = result
                d.result_id = css_id
                d.featured_game_winner = self.__get_featured_game_winner()

                if self.__calc.player_did_not_pick(player,featured_game):
                    d.player_pick = 'n/a'
                else:
                    d.player_pick = self.__calc.get_team_name_player_picked_to_win(player,featured_game)

                details.append(d)

        self.__tiebreak0_details = self.__sort_tiebreak0(details)

    def __calculate_tiebreaker1_details(self):
        details = []

        winner_data = self.__winners.get_week_winner_data()
        featured_game = winner_data.featured_game

        if winner_data.featured_game.game_state == NOT_STARTED:
            self.__tiebreak1_summary = None
            self.__tiebreak1_details = []
            return

        summary = Tiebreak1Summary()
        summary.team1 = featured_game.team1.team_name
        summary.team2 = featured_game.team2.team_name
        summary.team1_score = featured_game.team1_actual_points
        summary.team2_score = featured_game.team2_actual_points
        summary.result_spread = summary.team1_score - summary.team2_score

        players = self.__winners.get_players_that_won_tiebreak_1()
        if players != None:
            for player_id in players:
                player = self.__week_data.players[player_id]

                result = self.__get_tiebreak_result("win")
                css_id = self.__get_tiebreak_id(result)
    
                d = Tiebreak1Data()
                d.player_id = player_id
                d.player_name = self.__get_player_name(player_id)
                d.result = result
                d.result_id = css_id
    
                if self.__calc.player_did_not_pick(player,featured_game):
                    d.team1_score = 'n/a'
                    d.team2_score = 'n/a'
                    d.pick_spread = 'n/a'
                    d.difference = 'n/a'
                else:
                    pick = self.__calc.get_player_pick_for_game(player,featured_game)
                    d.team1_score = pick.team1_predicted_points
                    d.team2_score = pick.team2_predicted_points
                    d.pick_spread = pick.team1_predicted_points - pick.team2_predicted_points
                    d.difference = abs(d.pick_spread - summary.result_spread)
    
                details.append(d)

        players = self.__winners.get_players_that_lost_tiebreak_1()
        if players != None:
            for player_id in players:
                player = self.__week_data.players[player_id]

                result = self.__get_tiebreak_result("loss")
                css_id = self.__get_tiebreak_id(result)
    
                d = Tiebreak1Data()
                d.player_id = player_id
                d.player_name = self.__get_player_name(player_id)
                d.result = result
                d.result_id = css_id

                if self.__calc.player_did_not_pick(player,featured_game):
                    d.team1_score = 'n/a'
                    d.team2_score = 'n/a'
                    d.pick_spread = 'n/a'
                    d.difference = 'n/a'
                else:
                    pick = self.__calc.get_player_pick_for_game(player,featured_game)
                    d.team1_score = pick.team1_predicted_points
                    d.team2_score = pick.team2_predicted_points
                    d.pick_spread = pick.team1_predicted_points - pick.team2_predicted_points
                    d.difference = abs(d.pick_spread - summary.result_spread)

                details.append(d)

        self.__tiebreak1_summary = summary
        self.__tiebreak1_details = self.__sort_tiebreak1(details)

    def __calculate_tiebreaker2_details(self):
        details = []

        winner_data = self.__winners.get_week_winner_data()
        featured_game = winner_data.featured_game

        if winner_data.featured_game.game_state == NOT_STARTED:
            self.__tiebreak2_summary = None
            self.__tiebreak2_details = []
            return

        summary = Tiebreak2Summary()
        summary.team1 = featured_game.team1.team_name
        summary.team2 = featured_game.team2.team_name
        summary.team1_score = featured_game.team1_actual_points
        summary.team2_score = featured_game.team2_actual_points
        summary.result_total = summary.team1_score + summary.team2_score

        players = self.__winners.get_players_that_won_tiebreak_2()
        if players != None:
            for player_id in players:
                player = self.__week_data.players[player_id]

                result = self.__get_tiebreak_result("win")
                css_id = self.__get_tiebreak_id(result)
    
                d = Tiebreak2Data()
                d.player_id = player_id
                d.player_name = self.__get_player_name(player_id)
                d.result = result
                d.result_id = css_id
    
                if self.__calc.player_did_not_pick(player,featured_game):
                    d.team1_score = 'n/a'
                    d.team2_score = 'n/a'
                    d.pick_total = 'n/a'
                    d.difference = 'n/a'
                else:
                    pick = self.__calc.get_player_pick_for_game(player,featured_game)
                    d.team1_score = pick.team1_predicted_points
                    d.team2_score = pick.team2_predicted_points
                    d.pick_total = pick.team1_predicted_points + pick.team2_predicted_points
                    d.difference = abs(summary.result_total - d.pick_total)
    
                details.append(d)

        players = self.__winners.get_players_that_lost_tiebreak_2()
        if players != None:
            for player_id in players:
                player = self.__week_data.players[player_id]

                result = self.__get_tiebreak_result("loss")
                css_id = self.__get_tiebreak_id(result)
    
                d = Tiebreak2Data()
                d.player_id = player_id
                d.player_name = self.__get_player_name(player_id)
                d.result = result
                d.result_id = css_id
    
                if self.__calc.player_did_not_pick(player,featured_game):
                    d.team1_score = 'n/a'
                    d.team2_score = 'n/a'
                    d.pick_total = 'n/a'
                    d.difference = 'n/a'
                else:
                    pick = self.__calc.get_player_pick_for_game(player,featured_game)
                    d.team1_score = pick.team1_predicted_points
                    d.team2_score = pick.team2_predicted_points
                    d.pick_total = pick.team1_predicted_points + pick.team2_predicted_points
                    d.difference = abs(summary.result_total - d.pick_total)

                details.append(d)

        self.__tiebreak2_summary = summary
        self.__tiebreak2_details = self.__sort_tiebreak2(details)

    def __calculate_tiebreaker3_details(self):
        details = []

        winner_data = self.__winners.get_week_winner_data()
        if winner_data.featured_game.game_state == NOT_STARTED:
            self.__tiebreak3_summary = None
            self.__tiebreak3_details = []
            return

        summary = Tiebreak3Summary()
        summary.valid = self.__winners.is_tiebreaker_3_valid()

        players = self.__winners.get_players_that_won_tiebreak_3()
        if players != None:
            for player_id in players:
                player = self.__week_data.players[player_id]

                result = self.__get_tiebreak_result("win")
                css_id = self.__get_tiebreak_id(result)
    
                d = Tiebreak3Data()
                d.player_id = player_id
                d.player_name = self.__get_player_name(player_id)
                d.result = result
                d.result_id = css_id

                datetime_value,date_as_string = self.__get_player_submit_time(player_id)
                d.pick_entry_time = date_as_string
                d.pick_entry_datetime = datetime_value

                details.append(d)

        players = self.__winners.get_players_that_lost_tiebreak_3()
        if players != None:
            for player_id in players:
                player = self.__week_data.players[player_id]

                result = self.__get_tiebreak_result("loss")
                css_id = self.__get_tiebreak_id(result)

                d = Tiebreak3Data()
                d.player_id = player_id
                d.player_name = self.__get_player_name(player_id)
                d.result = result
                d.result_id = css_id

                datetime_value,date_as_string = self.__get_player_submit_time(player_id)
                d.pick_entry_time = date_as_string
                d.pick_entry_datetime = datetime_value

                details.append(d)

        self.__tiebreak3_summary = summary
        self.__tiebreak3_details = self.__sort_tiebreak3(details)

    def __get_player_name(self,player_id):
        if self.__use_private_names:
            return self.__week_data.players[player_id].private_name
        else:
            return self.__week_data.players[player_id].public_name

    def __get_tiebreak_id(self,value):
        if value == "won":
            return "tiebreak-won"
        elif value == "lost":
            return "tiebreak-lost"
        elif value == "ahead":
            return "tiebreak-ahead"
        elif value == "behind":
            return "tiebreak-behind"
        else:
            return "tiebreak-blank"

    def __get_tiebreak_result(self,win_loss):
        winner_data = self.__winners.get_week_winner_data()
        featured_game = winner_data.featured_game

        if featured_game.game_state == NOT_STARTED:
            return ""

        if featured_game.game_state == IN_PROGRESS and win_loss == "win":
            return "ahead"

        if featured_game.game_state == IN_PROGRESS and win_loss == "loss":
            return "behind"

        if featured_game.game_state == FINAL and win_loss == "win":
            return "won"

        if featured_game.game_state == FINAL and win_loss == "loss":
            return "lost"

        if win_loss != "win" or win_loss != "loss":
            raise AssertionError("Bad win_loss value %s" % (win_loss))
            return

        raise AssertionError("Bad state value %s" % (featured_game.game_state))

    def get_featured_game_state(self):
        winner_data = self.__winners.get_week_winner_data()
        featured_game = winner_data.featured_game
        return featured_game.game_state

    def __get_featured_game_winner(self):
        winner_data = self.__winners.get_week_winner_data()
        featured_game = winner_data.featured_game

        if featured_game.game_state == NOT_STARTED:
            return ""

        if featured_game.game_state == IN_PROGRESS:
            return self.__calc.get_team_name_winning_pool_game(featured_game)

        if featured_game.game_state == FINAL:
            return self.__calc.get_pool_game_winner_team_name(featured_game)

        raise AssertionError("Bad state value %s" % (featured_game.game_state))

    def __get_player_submit_time(self,player_id):
        winner_data = self.__winners.get_week_winner_data()
        pick_entry_time = winner_data.player_submit_times[player_id]

        if pick_entry_time == None:
            return pick_entry_time,"indeterminate"

        return pick_entry_time,pick_entry_time.strftime("%m/%d/%y %I:%M:%S %p UTC")

    def __ahead_or_won(self,value):
        return value == "ahead" or value == "won"

    def __behind_or_lost(self,value):
        return value == "behind" or value == "lost"

    def __sort_by_number_of_tiebreaks_then_win_loss(self,item):
        if item.number_of_tiebreaks == 0:
            return 0

        if item.number_of_tiebreaks == 1:
            if self.__ahead_or_won(item.tiebreak0):
                return 2
            else:
                return 1

        if item.number_of_tiebreaks == 2:
            if self.__ahead_or_won(item.tiebreak1):
                return 4
            else:
                return 3

        if item.number_of_tiebreaks == 3:
            if self.__ahead_or_won(item.tiebreak2):
                return 6
            else:
                return 5

        if item.number_of_tiebreaks == 4:
            if self.__ahead_or_won(item.tiebreak3):
                return 8
            else:
                return 7

        raise AssertionError("unexpected number of tiebreaks")

    def __sort_tiebreak_summary(self,summary):
        # this will sort the data so that it appears in the following order:
        # number of tiebreaks, then "won" or "ahead", then "lost" or "behind"
        sort_by_name = sorted(summary,key=lambda item:item.player_name)
        sort_by_tie = sorted(sort_by_name,key=lambda item:self.__sort_by_number_of_tiebreaks_then_win_loss(item),reverse=True)
        return sort_by_tie

    def __sort_tiebreak0(self,details):
        sort_by_name = sorted(details,key=lambda item:item.player_name)
        sort_by_wins = sorted(sort_by_name,key=lambda item:item.result == "won",reverse=True)
        sort_by_ahead = sorted(sort_by_wins,key=lambda item:item.result == "ahead",reverse=True)
        move_na_to_end = sorted(sort_by_ahead,key=lambda item:item.player_pick != 'n/a',reverse=True)
        return move_na_to_end

    def __sort_tiebreak1(self,details):
        sort_by_name = sorted(details,key=lambda item:item.player_name)
        sort_by_difference = sorted(sort_by_name,key=lambda item:item.difference)
        move_na_to_end = sorted(sort_by_difference,key=lambda item:item.difference != 'n/a',reverse=True)
        return move_na_to_end

    def __sort_tiebreak2(self,details):
        sort_by_name = sorted(details,key=lambda item:item.player_name)
        sort_by_difference = sorted(sort_by_name,key=lambda item:item.difference)
        move_na_to_end = sorted(sort_by_difference,key=lambda item:item.difference != 'n/a',reverse=True)
        return move_na_to_end

    def __sort_tiebreak3(self,details):
        sort_by_name = sorted(details,key=lambda item:item.player_name)
        sort_by_submit_time = sorted(sort_by_name,key=lambda item:item.pick_entry_datetime)
        move_none_to_end = sorted(sort_by_submit_time,key=lambda item:item != None,reverse=True)
        return move_none_to_end

