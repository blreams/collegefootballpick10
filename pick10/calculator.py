class CalculateResults:

    def __init__(self,data):
        self.__data = data

    def get_game_state(self):
        raise AssertionError,"Not implemented"

    def get_game_pick(self):
        raise AssertionError,"Not implemented"

    def get_player_name(self,player_key):
        raise AssertionError,"Not implemented"

    def get_game(self,game_key):
        raise AssertionError,"Not implemented"

    def get_team_name(self,team_key):
        raise AssertionError,"Not implemented"

    def get_team_player_picked_to_win(self,player_key,game_key):
        raise AssertionError,"Not implemented"

    def get_team_name_player_picked_to_win(self,player_key,game_key):
        raise AssertionError,"Not implemented"

    def is_team1_winning_pool(self,game):
        return None

    def is_team2_winning_pool(self,game_key):
        raise AssertionError,"Not implemented"

    def get_pool_game_winner(self,game_key):
        raise AssertionError,"Not implemented"

    def get_pool_game_winner_team_name(self,game_key):
        raise AssertionError,"Not implemented"

    def get_game_winner(self,game_key):
        raise AssertionError,"Not implemented"

    def get_game_winner_team_name(self,game_key):
        raise AssertionError,"Not implemented"

    def get_team_winning_pool_game(self,game_key):
        raise AssertionError,"Not implemented"

    def get_team_name_winning_pool_game(self,game_key):
        raise AssertionError,"Not implemented"

    def get_team_winning_game(self,game_key):
        raise AssertionError,"Not implemented"

    def get_team_name_winning_game(self,game_key):
        raise AssertionError,"Not implemented"

    def player_did_not_pick(self,player_key,game_key):
        raise AssertionError,"Not implemented"

    def did_player_win_game(self,player_key,game_key):
        raise AssertionError,"Not implemented"

    def did_player_lose_game(self,player_key,game_key):
        raise AssertionError,"Not implemented"

    def get_number_of_wins(self,player_key):
        raise AssertionError,"Not implemented"

    def __debug_print_game(self,player_key,game_key):
        raise AssertionError,"Not implemented"

    def get_number_of_losses(self,player_key):
        raise AssertionError,"Not implemented"

    def is_player_winning_game(self,player_key,game_key):
        raise AssertionError,"Not implemented"

    def is_player_losing_game(self,player_key,game_key):
        raise AssertionError,"Not implemented"

    def is_player_projected_to_win_game(self,player_key,game_key):
        raise AssertionError,"Not implemented"

    def is_player_possible_to_win_game(self,player_key,game_key):
        raise AssertionError,"Not implemented"

    def get_number_of_projected_wins(self,player_key):
        raise AssertionError,"Not implemented"

    def get_number_of_possible_wins(self,player_key):
        raise AssertionError,"Not implemented"

    def all_games_final(self):
        raise AssertionError,"Not implemented"

    def no_games_started(self):
        raise AssertionError,"Not implemented"

    def at_least_one_game_in_progress(self):
        raise AssertionError,"Not implemented"

    def get_summary_state_of_all_games(self):
        raise AssertionError,"Not implemented"

    def get_game_result_string(self,player_key,game_key):
        raise AssertionError,"Not implemented"

    def get_favored_team_name(self,game_key):
        raise AssertionError,"Not implemented"

    def get_game_score_spread(self,game_key):
        raise AssertionError,"Not implemented"

    def get_pick_score_spread(self,pick):
        raise AssertionError,"Not implemented"

    def get_featured_game(self):
        raise AssertionError,"Not implemented"

    def get_win_percent(self,player_key):
        raise AssertionError,"Not implemented"

    def get_win_percent_string(self,player_key):
        raise AssertionError,"Not implemented"

    def get_player_pick_for_game(self,player_key,game_key):
        raise AssertionError,"Not implemented"

    def get_player_submit_time(self,player_key,week=None):
        raise AssertionError,"Not implemented"

    def __find_player_pick_for_game(self,picks,game_key):
        raise AssertionError,"Not implemented"

    def __game_key_valid(self,game_key):
        raise AssertionError,"Not implemented"

    def __player_key_valid(self,player_key):
        raise AssertionError,"Not implemented"

    def __submit_time_invalid(self,week,submit_time):
        raise AssertionError,"Not implemented"

