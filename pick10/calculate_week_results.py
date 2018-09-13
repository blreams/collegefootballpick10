#from calculator import *
#from database import *
#from week_results import *
#from week_winner import *
from calculator import CalculateResults
from database import Database
from week_results import WeekResults
from week_winner import WeekWinner
from stats import Stats

class CalculateWeekResults:

    def __init__(self,year,week_number,private_names=False):
        self.year = year
        self.week_number = week_number
        self.week_stats = Stats()
        self.__use_private_names = private_names
        self.__calculate_week_results()

    def get_results(self):
        return self.__results

    def get_week_state(self):
        return self.__week_state

    def get_winner_info(self):
        return self.__winner.get_winner_data_object()

    def __calculate_week_results(self):
        database = Database()
        week_data = database.load_week_data(self.year,self.week_number)

        calc = CalculateResults(week_data)
        winner = WeekWinner(self.year,self.week_number,week_data)
        self.__week_state = calc.get_summary_state_of_all_games()
        self.__winner = winner

        results = []
        for player_id in week_data.players:
            player = week_data.players[player_id]

            player_results = WeekResults()
            player_results.rank = 1
            player_results.projected_rank = 1
            player_results.player_id = player_id
            player_results.wins = calc.get_number_of_wins(player)
            player_results.losses = calc.get_number_of_losses(player)
            player_results.win_pct = calc.get_win_percent_string(player)
            player_results.projected_wins = calc.get_number_of_projected_wins(player)
            player_results.possible_wins = calc.get_number_of_possible_wins(player)
            player_results.winner = self.__get_winner_message(player,winner)

            self.week_stats.add_score(player_results.wins, (player_results.wins + player_results.losses))

            if self.__use_private_names:
                player_results.player_name = player.private_name
            else:
                player_results.player_name = player.public_name

            results.append(player_results)

        self.week_stats.calc_stats()

        if len(results) > 0:
            winner_state = winner.get_winner_state()

            if winner_state == "no_winner_yet":
                results = self.assign_rank(results,winner=None)
                results = self.assign_projected_rank(results,projected_winner=None)
            elif winner_state == "official":
                calculated_winner = winner.get_winner()
                results = self.assign_rank(results,winner=calculated_winner)
                results = self.assign_projected_rank(results,projected_winner=calculated_winner)
            elif winner_state == "unofficial":
                calculated_winner = winner.get_winner()
                results = self.assign_rank(results,winner=calculated_winner)
                results = self.assign_projected_rank(results,projected_winner=None)
            elif winner_state == "projected":
                calculated_winner = winner.get_winner()
                results = self.assign_rank(results,winner=None)
                results = self.assign_projected_rank(results,projected_winner=calculated_winner)
            elif winner_state == "possible":
                calculated_winner = winner.get_winner()
                results = self.assign_rank(results,winner=None)
                results = self.assign_projected_rank(results,projected_winner=None)
            else:
                raise AssertionError,"unexpected winner state %s" % (winner_state)

            results = self.__sort_by_rank(results)

        self.__results = results

    def __get_winner_message(self,player,winner):
        winner_state = winner.get_winner_state()
        winning_player = winner.get_winner()
        if winning_player == None:
            return ""

        if winner_state == "no_winner_yet":
            return ""
        elif winner_state == "official" and player == winning_player:
            return "WINNER"
        elif winner_state == "unofficial" and player == winning_player:
            return "UNOFFICIAL WINNER"
        elif winner_state == "projected" and player == winning_player:
            return "PROJECTED WINNER"
        elif winner_state == "possible" and player in winning_player:
            return "POSSIBLE WINNER"
        else:
            return ""

    def __sort_by_rank(self,results):
        return sorted(results,key=lambda result:result.rank)

    def assign_rank(self,results,winner=None):
        # sort by losses first so that people with more losses get a lower rank
        # this is the case where a player did not enter any picks for a week
        # that player would have 10 losses before any games were started, and therefore
        # should be ranked lower
        sorted_by_losses = sorted(results,key=lambda result:result.losses)
        sorted_results = sorted(sorted_by_losses,key=lambda result:result.wins,reverse=True)

        assigned_results = []

        if winner != None:
            self.__move_winner_to_top_of_results(sorted_results,winner)
            self.__winner_sanity_check(sorted_results)
            next_rank = 2   # no ties for first place
        else:
            next_rank = 1   # there can be ties for first place

        wins = sorted_results[0].wins
        losses = sorted_results[0].losses

        for i,player_result in enumerate(sorted_results):

            first_place = i == 0
            second_place = i == 1

            if first_place:
                player_result.rank = 1
                assigned_results.append(player_result)
                continue

            if second_place and winner:
                player_result.rank = 2
                wins = player_result.wins
                losses = player_result.losses
            else:
                record_changed = player_result.wins != wins or player_result.losses != losses

                if record_changed:
                    next_rank = i+1
                    player_result.rank = next_rank
                    wins = player_result.wins
                    losses = player_result.losses
                else:
                    player_result.rank = next_rank

            assigned_results.append(player_result)

        return assigned_results



    def assign_projected_rank(self,results,projected_winner=None):
        sorted_results = sorted(results,key=lambda result:result.projected_wins,reverse=True)

        assigned_results = []

        if projected_winner != None:
            self.__move_winner_to_top_of_results(sorted_results,projected_winner)
            self.__projected_winner_sanity_check(sorted_results)
            next_rank = 2   # no ties for first place
        else:
            next_rank = 1   # there can be ties for first place

        projected_wins = sorted_results[0].projected_wins

        for i,player_result in enumerate(sorted_results):

            first_place = i == 0
            second_place = i == 1

            if first_place:
                player_result.projected_rank = 1
                assigned_results.append(player_result)
                continue

            if second_place and projected_winner:
                player_result.projected_rank = 2
                projected_wins = player_result.projected_wins
            else:
                wins_changed = player_result.projected_wins != projected_wins

                if wins_changed:
                    next_rank = i+1
                    player_result.projected_rank = next_rank
                    projected_wins = player_result.projected_wins
                else:
                    player_result.projected_rank = next_rank

            assigned_results.append(player_result)

        return assigned_results

    def __move_winner_to_top_of_results(self,results,winner):
        winner_index = None
        for i,player in enumerate(results):
            if player.player_id == winner.id:
                winner_index = i
        assert winner_index != None,"Could not find the winning player in the results"
        results.insert(0,results.pop(winner_index))

    def __winner_sanity_check(self,results):
        # the winner should have the best record or tied for the best record
        assert len(results) > 2, "Expected more than 1 player in the results"

        winner = results[0]
        next_best = results[1]

        assert winner.wins >= next_best.wins,"Winner had fewer wins than another (%d vs. %d)" % (winner.wins,next_best.wins)
        assert winner.losses <= next_best.losses,"Winner had more losses than another (%d vs. %d)" % (winner.losses,next_best.losses)

    def __projected_winner_sanity_check(self,results):
        # the winner should have the best record or tied for the best record
        assert len(results) > 2, "Expected more than 1 player in the results"

        winner = results[0]
        next_best = results[1]

        assert winner.projected_wins >= next_best.projected_wins,"Projected winner had fewer wins than another (%d vs. %d)" % (winner.projected_wins,next_best.projected_wins)
