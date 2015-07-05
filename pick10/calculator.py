TEAM1 = 1
TEAM2 = 2
NOT_STARTED = 1
IN_PROGRESS = 2
FINAL = 3

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

    def get_team_player_picked_to_win(self,player,game):
        picks = self.__data.player_picks[player.id]
        pick = self.__find_player_pick_for_game(picks,game)
        assert pick != None,"Could not find a pick that matches the passed in game"
        return pick.winner

    def get_team_name_player_picked_to_win(self,player,game):
        assert game != None and self.__game_id_valid(game.id),"Game is not valid"

        if self.player_did_not_pick(player,game):
            return ""

        winner = self.get_team_player_picked_to_win(player,game)
        if winner == TEAM1: 
            return game.team1.team_name
        elif winner == TEAM2:
            return game.team2.team_name
        raise AssertionError,"Error determining winner name (winner=%s)" % (winner)

    def is_team1_winning_pool(self,game):
        score_diff = game.team2_actual_points-game.team1_actual_points
        if game.favored == TEAM2:
            spread = game.spread
        elif game.favored == TEAM1:
            spread = -game.spread
        else:
            raise AssertionError,"game.favored has an invalid value"
        return score_diff < spread

    def is_team2_winning_pool(self,game):
        score_diff = game.team2_actual_points-game.team1_actual_points
        if game.favored == TEAM2:
            spread = game.spread
        elif game.favored == TEAM1:
            spread = -game.spread
        else: 
            raise AssertionError,"game.favored has an invalid value"
        return score_diff > spread

    def get_pool_game_winner(self,game):
        if game.game_state == FINAL:
            if self.is_team1_winning_pool(game):
                return TEAM1
            elif self.is_team2_winning_pool(game):
                return TEAM2
            else:
                raise AssertionError,"Either team1 or team2 should be ahead"
        else:
            return None

    def get_pool_game_winner_team_name(self,game):
        winner = self.get_pool_game_winner(game)
        game_not_final = not(winner)
        if game_not_final:
            return None

        if winner == TEAM1:
            return game.team1.team_name
        elif winner == TEAM2:
            return game.team2.team_name
        else:
            raise AssertionError,"Either team1 or team2 should have won"

    def get_game_winner(self,game):
        if game.game_state == FINAL:

            assert game.team1_actual_points != game.team2_actual_points,\
                   "Game cannot end in a tie (%s to %s)" %\
                   (game.team1_actual_points,game.team2_actual_points)

            if game.team1_actual_points > game.team2_actual_points:
                return TEAM1
            else:
                return TEAM2
        else:
            return None

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

    def player_did_not_pick(self,player,game):
        assert game != None and self.__game_id_valid(game.id),"Game is not valid"
        picks = self.__data.player_picks[player.id]
        pick = self.__find_player_pick_for_game(picks,game)
        if pick == None:
            return True
                                                    
        return pick.winner == 0

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

    def __find_player_pick_for_game(self,picks,game):
        if game == None:
            return None
        for pick in picks:
            if pick.game.id == game.id:
                return pick
        return None

    def __game_id_valid(self,game_id):
        return game_id in self.__data.games_id

    def __player_key_valid(self,player_key):
        raise AssertionError,"Not implemented"

    def __submit_time_invalid(self,week,submit_time):
        raise AssertionError,"Not implemented"

