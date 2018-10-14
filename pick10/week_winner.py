from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

from .database import Database
from .calculator import CalculateResults
from .calculator import NOT_STARTED, IN_PROGRESS, FINAL

class WeekWinnerData:
    featured_game_state = None
    winner = None
    projected = None
    official = None
    num_tied_for_first = None

class WeekWinnerCalculationData:
    player_wins = None
    player_projected_wins = None
    featured_game = None
    featured_game_winner = None
    featured_game_ahead = None
    player_featured_game_picks = None
    player_submit_times = None
    week_state = None
    week = None  # TODO unsure if needed

class WeekWinner:
    calculated_winner = None
    players_tied_for_first = None
    players_won_tiebreak0 = None
    players_lost_tiebreak0 = None
    players_won_tiebreak1 = None
    players_lost_tiebreak1 = None
    players_won_tiebreak2 = None
    players_lost_tiebreak2 = None
    players_won_tiebreak3 = None
    players_lost_tiebreak3 = None

    # if week_data is None, then the data is loaded from the database
    # if week_data passed in, then it is used as the week data
    # this avoids having to reload data from the database multiple times
    def __init__(self,year,week_number,week_data=None):
        self.__data = self.__setup_data_to_use(year,week_number,week_data)

        if self.__data.week_state == IN_PROGRESS:
            self.use_projected_winner = True
        else:
            self.use_projected_winner = False

        self.__calculate_tied_for_first()
        self.__calculate_tiebreaker_0()
        self.__calculate_tiebreaker_1()
        self.__calculate_tiebreaker_2()
        self.__calculate_tiebreaker_3()
        self.__calculate_winner()

    def get_winner_state(self):
        if self.__data.week_state == NOT_STARTED:
            return "no_winner_yet"

        if self.__data.featured_game.game_state == NOT_STARTED:
            return "no_winner_yet"

        if self.__data.featured_game.game_state == IN_PROGRESS:
            if self.__tiebreaker_3_indeterminate:
                return "possible"
            else:
                return "projected"

        if self.__data.week_state == IN_PROGRESS and self.__data.featured_game.game_state == FINAL:
            if self.__tiebreaker_3_indeterminate:
                return "possible"
            else:
                return "projected"

        if self.__data.week_state == FINAL and self.__data.featured_game.game_state == FINAL:
            if self.__data.week.winner == None:
                if self.__tiebreaker_3_indeterminate:
                    return "possible"
                else:
                    return "unofficial"
            else:
                return "official"

        raise AssertionError("should not get here")


    def get_winner(self):
        if self.__data.week.winner != None:
            return self.__data.week.winner

        if self.__data.featured_game.game_state == NOT_STARTED:
            return None

        if self.is_tiebreaker_3_indeterminate():
            players = [ self.__players[player_id] for player_id in self.calculated_winner ]
            return players

        if not self.is_winner_valid():
            return None

        player = self.__players[self.calculated_winner]
        return player

    def get_projected_winner(self):
        if self.__data.featured_game.game_state == IN_PROGRESS:

            multiple_winners = type(self.calculated_winner) == list and len(self.calculated_winner) > 1
            if multiple_winners:
                players = [ self.__players[w] for w in self.calculated_winner ]
                return players

            player = self.__players[self.calculated_winner]
            return player
        return None

    def verify_winner(self):
        if self.__data.featured_game.game_state != FINAL:
            return None
        return self.calculated_winner != None and len(self.calculated_winner) == 1 and self.calculated_winner[0] == self.__data.week.winner.id

    def get_players_tied_for_first(self):
        return self.players_tied_for_first

    def get_players_that_won_tiebreak_0(self):
        return self.players_won_tiebreak0

    def get_players_that_lost_tiebreak_0(self):
        return self.players_lost_tiebreak0

    def get_players_that_won_tiebreak_1(self):
        return self.players_won_tiebreak1

    def get_players_that_lost_tiebreak_1(self):
        return self.players_lost_tiebreak1

    def get_players_that_won_tiebreak_2(self):
        return self.players_won_tiebreak2

    def get_players_that_lost_tiebreak_2(self):
        return self.players_lost_tiebreak2

    def get_players_that_won_tiebreak_3(self):
        return self.players_won_tiebreak3

    def get_players_that_lost_tiebreak_3(self):
        return self.players_lost_tiebreak3

    # if cannot determine correct winner, this will be False
    # example use case:  cannot determine winner of tiebreak 3
    def is_winner_valid(self):
        return self.__winner_valid

    def __calculate_winner(self):
        self.__winner_valid = True

        if self.is_tiebreaker_3_valid():
            if self.players_won_tiebreak3 == None or len(self.players_won_tiebreak3) != 1:
                self.calculated_winner = None  # unexpected error
                self.__winner_valid = False
                return
            self.calculated_winner = self.players_won_tiebreak3[0]
            return
        elif self.is_tiebreaker_3_indeterminate():
            self.__winner_valid = False
            self.calculated_winner = self.players_won_tiebreak3
            return
        else:
            unable_to_determine_winner = self.players_won_tiebreak2 != None and len(self.players_won_tiebreak2) > 1
            if unable_to_determine_winner:
                self.calculated_winner = self.players_won_tiebreak3
                self.__winner_valid = False
                return

        if self.players_won_tiebreak2 != None and len(self.players_won_tiebreak2) == 1:
            self.calculated_winner = self.players_won_tiebreak2[0]
            return

        if self.players_won_tiebreak1 != None and len(self.players_won_tiebreak1) == 1:
            self.calculated_winner = self.players_won_tiebreak1[0]
            return

        if self.players_won_tiebreak0 != None and len(self.players_won_tiebreak0) == 1:
            self.calculated_winner = self.players_won_tiebreak0[0]
            return

        if self.players_tied_for_first != None and len(self.players_tied_for_first) == 1:
            self.calculated_winner = self.players_tied_for_first[0]
            return

        self.calculated_winner = None
        self.__winner_valid = False

    def is_winner_official(self):
        return self.__data.week.winner != None

    def __calculate_tied_for_first(self):
        if self.use_projected_winner:
            player_wins = self.__data.player_projected_wins
        else:
            player_wins = self.__data.player_wins

        most_wins = max(player_wins.values())
        self.players_tied_for_first = [player_id for player_id in player_wins if player_wins[player_id] == most_wins]


    def __calculate_tiebreaker_0(self):
        if self.tiebreaker_0_unnecessary():
            self.players_won_tiebreak0 = None
            self.players_lost_tiebreak0 = None
            return

        if self.__data.featured_game.game_state == NOT_STARTED:
            self.players_won_tiebreak0 = None
            self.players_lost_tiebreak0 = None
            return

        if self.__data.featured_game.game_state == FINAL:
            featured_winner = self.__data.featured_game_winner
        elif self.__data.featured_game.game_state == IN_PROGRESS:
            featured_winner = self.__data.featured_game_ahead
        else:
            raise AssertionError("Should not reach here")

        self.players_won_tiebreak0 = []
        self.players_lost_tiebreak0 = []

        for player_id in self.players_tied_for_first:
            player_pick = self.__data.player_featured_game_picks[player_id]

            if player_pick == None:
                self.players_lost_tiebreak0.append(player_id)
            elif player_pick.winner == featured_winner:
                self.players_won_tiebreak0.append(player_id)
            else: 
                self.players_lost_tiebreak0.append(player_id)

    def __calculate_tiebreaker_1(self):
        if self.tiebreaker_1_unnecessary():
            self.players_won_tiebreak1 = None
            self.players_lost_tiebreak1 = None
            return

        players = self.__get_players_to_use(tiebreaker_number=1)

        game = self.__data.featured_game
        result_spread = game.team1_actual_points - game.team2_actual_points

        # find the min difference
        min_difference = 0
        first_valid_pick = True
        for player_id in players:
            pick = self.__data.player_featured_game_picks[player_id]

            if self.__pick_score_not_entered(pick):
                continue

            pick_spread = pick.team1_predicted_points - pick.team2_predicted_points
            pick_difference = abs(pick_spread-result_spread) 
            if first_valid_pick or pick_difference < min_difference:
                min_difference = pick_difference
                first_valid_pick = False

        # calculate who won/lost
        self.players_won_tiebreak1 = []
        self.players_lost_tiebreak1 = []
        for player_id in players:
            pick = self.__data.player_featured_game_picks[player_id]

            if self.__pick_score_not_entered(pick):
                self.players_lost_tiebreak1.append(player_id)
                continue

            pick_spread = pick.team1_predicted_points - pick.team2_predicted_points
            pick_difference = abs(pick_spread-result_spread) 
            if pick_difference == min_difference:
                self.players_won_tiebreak1.append(player_id)
            else:
                self.players_lost_tiebreak1.append(player_id)


    def __calculate_tiebreaker_2(self):
        if self.tiebreaker_2_unnecessary():
            self.players_won_tiebreak2 = None
            self.players_lost_tiebreak2 = None
            return

        players = self.__get_players_to_use(tiebreaker_number=2)

        game = self.__data.featured_game
        result_total = game.team1_actual_points + game.team2_actual_points

        # find the min difference
        min_difference = 0
        first_valid_pick = True
        for player_id in players:
            pick = self.__data.player_featured_game_picks[player_id]

            if self.__pick_score_not_entered(pick):
                continue

            pick_total = pick.team1_predicted_points + pick.team2_predicted_points
            pick_difference = abs(result_total-pick_total)
            if first_valid_pick or pick_difference < min_difference:
                min_difference = pick_difference
                first_valid_pick = False

        # calculate who won/lost
        self.players_won_tiebreak2 = []
        self.players_lost_tiebreak2 = []
        for player_id in players:
            pick = self.__data.player_featured_game_picks[player_id]

            if self.__pick_score_not_entered(pick):
                self.players_lost_tiebreak2.append(player_id)
                continue

            pick_total = pick.team1_predicted_points + pick.team2_predicted_points
            pick_difference = abs(result_total-pick_total)
            if pick_difference == min_difference:
                self.players_won_tiebreak2.append(player_id)
            else:
                self.players_lost_tiebreak2.append(player_id)

    def __calculate_tiebreaker_3(self):
        self.__tiebreaker_3_valid = False
        self.__tiebreaker_3_indeterminate = False

        if self.tiebreaker_3_unnecessary():
            self.players_won_tiebreak3 = None
            self.players_lost_tiebreak3 = None
            return

        players = self.__get_players_to_use(tiebreaker_number=3)
        self.players_won_tiebreak3 = []
        self.players_lost_tiebreak3 = []

        entry_times = [ value for value in self.__data.player_submit_times.values() if value != None ]
        if len(entry_times) == 0:
            self.__tiebreaker_3_indeterminate = True
            for player_id in players:
                self.players_won_tiebreak3.append(player_id)
            return

        self.__tiebreaker_3_valid = True
        earliest_time = min(entry_times)
        for player_id in players:
            if self.__data.player_submit_times[player_id] == earliest_time:
                self.players_won_tiebreak3.append(player_id)
            else:
                self.players_lost_tiebreak3.append(player_id)

    def tiebreaker_0_unnecessary(self):
        return self.__data.week_state == NOT_STARTED or \
               self.__data.featured_game.game_state == NOT_STARTED or \
               len(self.players_tied_for_first) == 1

    def tiebreaker_1_unnecessary(self):
        one_player_won_tiebreak0 = self.players_won_tiebreak0 != None and len(self.players_won_tiebreak0) == 1
        return self.tiebreaker_0_unnecessary() or one_player_won_tiebreak0

    def tiebreaker_2_unnecessary(self):
        one_player_won_tiebreak1 = self.players_won_tiebreak1 != None and len(self.players_won_tiebreak1) == 1
        return self.tiebreaker_1_unnecessary() or one_player_won_tiebreak1

    def tiebreaker_3_unnecessary(self):
        one_player_won_tiebreak2 = self.players_won_tiebreak2 != None and len(self.players_won_tiebreak2) == 1
        return self.tiebreaker_2_unnecessary() or one_player_won_tiebreak2

    # tiebreaker 3 is valid when: 
    # - week.pick_deadline is set (i.e a pick deadline set)
    # - the picks were entered before the pick deadline
    # - the submit time makes sense (i.e. submit time year matches the week.year)
    def is_tiebreaker_3_valid(self):
        return self.__tiebreaker_3_valid

    def is_tiebreaker_3_indeterminate(self):
        return self.__tiebreaker_3_indeterminate

    def __get_players_to_use(self,tiebreaker_number):
        # tiebreak0:  use players tied for first
        # tiebreak1:  use tiebreak0 or players tied for first
        # tiebreak2:  use tiebreak1, tiebreak0, players tied for first
        # tiebreak3:  use tiebreak2, tiebreak1, tiebreak0, players_tied_for_first
        if tiebreaker_number == 0:
            return self.players_tied_for_first

        no_tiebreak_0_players =  self.players_won_tiebreak0 == None or len(self.players_won_tiebreak0) == 0
        no_tiebreak_1_players =  self.players_won_tiebreak1 == None or len(self.players_won_tiebreak1) == 0
        no_tiebreak_2_players =  self.players_won_tiebreak2 == None or len(self.players_won_tiebreak2) == 0

        if tiebreaker_number == 1:
            if no_tiebreak_0_players:
                return self.players_tied_for_first
            return self.players_won_tiebreak0

        if tiebreaker_number == 2:
            if no_tiebreak_1_players:
                if no_tiebreak_0_players:
                    return self.players_tied_for_first
                else:
                    return self.players_won_tiebreak0
            else:
                return self.players_won_tiebreak1

        if tiebreaker_number == 3:
            if no_tiebreak_2_players:
                if no_tiebreak_1_players:
                    if no_tiebreak_0_players:
                        return self.players_tied_for_first
                    else:
                        return self.players_won_tiebreak0
                else:
                    return self.players_won_tiebreak1
            else:
                return self.players_won_tiebreak2

        raise AssertionError("tiebreaker_number %d is invalid." % (tiebreaker_number))

    def get_winner_data_object(self):
        w = WeekWinnerData()
        w.featured_game_state = self.__data.featured_game.game_state
        w.winner = self.get_winner()
        w.projected = self.get_projected_winner()
        w.official = self.is_winner_official()
        w.num_tied_for_first = len(self.players_tied_for_first)
        return w

    def get_week_winner_data(self):
        return self.__data

    def __pick_score_not_entered(self,pick):
        return pick == None or\
               pick.team1_predicted_points == None or pick.team2_predicted_points == None or\
               pick.team1_predicted_points < 0 or pick.team2_predicted_points < 0

    def __setup_data_to_use(self,year,week_number,week_data_supplied=None):
        if week_data_supplied != None:
            week_data = week_data_supplied
        else:
            database = Database()
            week_data = database.load_week_data(year,week_number)

        calc = CalculateResults(week_data)
        self.__players = week_data.players  # save to lookup player by id

        data = WeekWinnerCalculationData()
        data.player_wins = dict()
        data.player_projected_wins = dict()
        data.player_featured_game_picks = dict()
        data.player_submit_times = dict()
        data.week_state = calc.get_summary_state_of_all_games()
        data.featured_game = calc.get_featured_game()
        data.week = week_data.week

        if data.featured_game.game_state == NOT_STARTED:
            data.featured_game_winner = None
            data.featured_game_ahead = None
        if data.featured_game.game_state == IN_PROGRESS:
            data.featured_game_winner = None
            data.featured_game_ahead = calc.get_team_winning_pool_game(data.featured_game)
        if data.featured_game.game_state == FINAL:
            data.featured_game_winner = calc.get_pool_game_winner(data.featured_game)
            data.featured_game_ahead = None

        for player_id in week_data.players:
            player = week_data.players[player_id]
            data.player_wins[player_id] = calc.get_number_of_wins(player)
            data.player_projected_wins[player_id] = calc.get_number_of_projected_wins(player)

            if calc.player_did_not_pick(player,data.featured_game):
                data.player_featured_game_picks[player_id] = None
                data.player_submit_times[player_id] = None
            else:
                data.player_featured_game_picks[player_id] = calc.get_player_pick_for_game(player,data.featured_game)
                data.player_submit_times[player_id] = calc.get_player_submit_time(player,data.week)
        return data
