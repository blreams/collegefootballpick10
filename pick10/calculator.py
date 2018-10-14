TEAM1 = 1
TEAM2 = 2
TIED = 3
NOT_STARTED = 1
IN_PROGRESS = 2
FINAL = 3

class CalculateResults:

    def __init__(self,data):
        self.__data = data

    def get_game_state(self):
        raise AssertionError("Not implemented")

    def get_game_pick(self):
        raise AssertionError("Not implemented")

    def get_player_name(self,player_key):
        raise AssertionError("Not implemented")

    def get_game(self,game_key):
        raise AssertionError("Not implemented")

    def get_team_name(self,team_key):
        raise AssertionError("Not implemented")

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
        raise AssertionError("Error determining winner name (winner=%s)" % (winner))

    def is_team1_winning_pool(self,game):
        score_diff = game.team2_actual_points-game.team1_actual_points
        if game.favored == TEAM2:
            spread = game.spread
        elif game.favored == TEAM1:
            spread = -game.spread
        else:
            raise AssertionError("game.favored has an invalid value")
        return score_diff < spread

    def is_team2_winning_pool(self,game):
        score_diff = game.team2_actual_points-game.team1_actual_points
        if game.favored == TEAM2:
            spread = game.spread
        elif game.favored == TEAM1:
            spread = -game.spread
        else: 
            raise AssertionError("game.favored has an invalid value")
        return score_diff > spread

    def get_pool_game_winner(self,game):
        if game.game_state == FINAL:
            if self.is_team1_winning_pool(game):
                return TEAM1
            elif self.is_team2_winning_pool(game):
                return TEAM2
            else:
                raise AssertionError("Either team1 or team2 should be ahead")
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
            raise AssertionError("Either team1 or team2 should have won")

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

    def get_game_winner_team_name(self,game):
        winner = self.get_game_winner(game)
        game_not_final = not(winner)
        if game_not_final:
            return None

        if winner == TEAM1:
            return game.team1.team_name
        elif winner == TEAM2:
            return game.team2.team_name
        else:
            raise AssertionError("Either team1 or team2 should have won")

    def get_team_winning_pool_game(self,game):
        if game.game_state == IN_PROGRESS:
            if self.is_team1_winning_pool(game):
                return TEAM1
            elif self.is_team2_winning_pool(game):
                return TEAM2
            else:
                raise AssertionError("Either team1 or team2 should be ahead")
        else:
            return None

    def get_team_name_winning_pool_game(self,game):
        team = self.get_team_winning_pool_game(game)
        game_not_in_progress = not(team)
        if game_not_in_progress:
            return None

        if team == TEAM1:
            return game.team1.team_name
        elif team == TEAM2:
            return game.team2.team_name
        else:
            raise AssertionError("Either team1 or team2 should be ahead")

    def get_team_winning_game(self,game):
        if game.game_state == IN_PROGRESS:
            if game.team1_actual_points > game.team2_actual_points:
                return TEAM1
            elif game.team1_actual_points == game.team2_actual_points:
                return TIED
            else:
                return TEAM2
        else:
            return None

    def get_team_name_winning_game(self,game):
        team = self.get_team_winning_game(game)
        game_not_in_progress = not(team)
        if game_not_in_progress:
            return None

        if team == TEAM1:
            return game.team1.team_name
        elif team == TEAM2:
            return game.team2.team_name
        elif team == TIED:
            return "tied"
        else:
            raise AssertionError("Invalid team value")

    def player_did_not_pick(self,player,game):
        assert game != None and self.__game_id_valid(game.id),"Game is not valid"
        assert self.__player_id_valid(player.id),"Player is not valid"

        no_picks = player.id not in self.__data.player_picks
        if no_picks:
            return True

        picks = self.__data.player_picks[player.id]
        pick = self.__find_player_pick_for_game(picks,game)
        if pick == None:
            return True
                                                    
        return pick.winner == 0

    def did_player_win_game(self,player,game):
        if self.player_did_not_pick(player,game):
            return False

        game_winner = self.get_pool_game_winner(game)
        if game_winner:
            player_winner = self.get_team_player_picked_to_win(player,game)
            return player_winner == game_winner
        return False


    def did_player_lose_game(self,player,game):
        if self.player_did_not_pick(player,game):
            return True

        game_winner = self.get_pool_game_winner(game)
        if game_winner:
            player_winner = self.get_team_player_picked_to_win(player,game)
            return player_winner != game_winner
        return False

    def get_number_of_wins(self,player):
        wins = 0
        for game in self.__data.games.values():
            if self.did_player_win_game(player,game):
                wins += 1
        return wins

    def did_player_default(self,player):
        picks = 0
        for game in self.__data.games.values():
            if self.player_did_not_pick(player,game) == False:
                picks += 1
        return picks == 0

    def __debug_print_game(self,player_key,game_key):
        raise AssertionError("Not implemented")

    def get_number_of_losses(self,player):
        losses = 0
        for game in self.__data.games.values():
            if self.did_player_lose_game(player,game):
                losses += 1
        return losses

    def is_player_winning_game(self,player,game):
        assert game != None and self.__game_id_valid(game.id),"invalid game"
        assert player != None and self.__player_id_valid(player.id),"invalid player"

        if game.game_state == FINAL:
            return False

        if self.player_did_not_pick(player,game):
            return False

        team_ahead = self.get_team_winning_pool_game(game)

        if team_ahead:
            picks = self.__data.player_picks[player.id]
            pick = self.__find_player_pick_for_game(picks,game)
            assert pick != None, "Could not find pick for player id %s" % (player.id)

            return team_ahead == pick.winner

        return False


    def is_player_losing_game(self,player,game):
        assert game != None and self.__game_id_valid(game.id),"invalid game"
        assert player != None and self.__player_id_valid(player.id),"invalid player"

        if game.game_state == FINAL:
            return False

        if self.player_did_not_pick(player,game):
            return True

        team_ahead = self.get_team_winning_pool_game(game)

        if team_ahead:
            picks = self.__data.player_picks[player.id]
            pick = self.__find_player_pick_for_game(picks,game)
            assert pick != None, "Could not find pick for player id %s" % (player.id)

            return team_ahead != pick.winner

        return False


    def is_player_projected_to_win_game(self,player,game):
        assert game != None and self.__game_id_valid(game.id),"invalid game"
        assert player != None and self.__player_id_valid(player.id),"invalid player"

        if self.player_did_not_pick(player,game):
            return False

        if game.game_state == FINAL:
            return self.did_player_win_game(player,game)
        elif game.game_state == IN_PROGRESS:
            return self.is_player_winning_game(player,game)
        elif game.game_state == NOT_STARTED:
            return True
        else:
            raise AssertionError("invalid game state")

    def is_player_possible_to_win_game(self,player,game):
        assert game != None and self.__game_id_valid(game.id),"invalid game"

        if self.player_did_not_pick(player,game):
            return False

        if game.game_state == FINAL:
            return self.did_player_win_game(player,game)
        elif game.game_state == IN_PROGRESS:
            return True
        elif game.game_state == NOT_STARTED:
            return True
        else:
            raise AssertionError("invalid game state")

    def get_number_of_projected_wins(self,player):
        wins = 0
        for game in self.__data.games.values():
            if self.is_player_projected_to_win_game(player,game):
                wins += 1
        return wins

    def get_number_of_possible_wins(self,player):
        wins = 0
        for game in self.__data.games.values():
            if self.is_player_possible_to_win_game(player,game):
                wins += 1
        return wins

    def all_games_final(self):
        final_games = 0
        for game in self.__data.games.values():
            if game.game_state == FINAL:
                final_games += 1
        return final_games == len(self.__data.games)

    def no_games_started(self):
        not_started = 0
        for game in self.__data.games.values():
            if game.game_state == NOT_STARTED:
                not_started += 1
        return not_started == len(self.__data.games)

    def at_least_one_game_in_progress(self):
        in_progress = 0
        for game in self.__data.games.values():
            if game.game_state == IN_PROGRESS:
                in_progress += 1
        return in_progress > 0

    def get_summary_state_of_all_games(self):
        if self.all_games_final():
            return FINAL
        if self.no_games_started():
            return NOT_STARTED
        return IN_PROGRESS

    def get_game_result_string(self,player,game):
        assert game != None and self.__game_id_valid(game.id),"invalid game"
        assert player != None and self.__player_id_valid(player.id),"invalid player"

        if self.did_player_win_game(player,game):
            return "win"
        if self.did_player_lose_game(player,game):
            return "loss"
        if self.is_player_winning_game(player,game):
            return "ahead"
        if self.is_player_losing_game(player,game):
            return "behind"
        return ""

    def get_favored_team_name(self,game):
        assert game != None and self.__game_id_valid(game.id),"invalid game"

        if game.favored == TEAM1:
            return game.team1.team_name
        elif game.favored == TEAM2:
            return game.team2.team_name
        raise AssertionError("invalid favored value")

    def get_game_score_spread(self,game):
        assert game != None and self.__game_id_valid(game.id),"invalid game"
        assert game.game_state != NOT_STARTED,"a game that has not started has no spread"
        assert game.team1_actual_points != None,"invalid score value"
        assert game.team2_actual_points != None,"invalid score value"
        assert game.team1_actual_points >= 0,"invalid score value"
        assert game.team2_actual_points >= 0,"invalid score value"
        return abs(game.team1_actual_points-game.team2_actual_points)

    def get_pick_score_spread(self,pick):
        assert pick != None,"invalid pick value"
        assert pick.team1_predicted_points != None,"pick team1 score is invalid"
        assert pick.team2_predicted_points != None,"pick team2 score is invalid"
        assert pick.team1_predicted_points >= 0,"pick team1 score is invalid"
        assert pick.team2_predicted_points >= 0,"pick team2 score is invalid"
        return abs(pick.team1_predicted_points-pick.team2_predicted_points)

    def get_featured_game(self):
        game = self.__data.games.get(10)
        assert game != None, "did not find a featured game"
        return game

    def get_win_percent(self,player):
        wins = self.get_number_of_wins(player)
        losses = self.get_number_of_losses(player)
        num_games = wins+losses

        if num_games == 0:
            return 0.0
        return float(wins) / float(num_games)

    def get_win_percent_string(self,player):
        win_pct = self.get_win_percent(player)
        return "%0.3f" % (win_pct)

    def get_player_pick_for_game(self,player,game):
        picks = self.__data.player_picks[player.id]
        pick = self.__find_player_pick_for_game(picks,game)
        assert pick != None,"Could not find a pick that matches the passed in game"
        return pick

    def get_player_featured_game_pick(self,player):
        game10 = self.get_featured_game()
        return self.get_player_pick_for_game(player,game10)

    def get_player_submit_time(self,player,week=None):
        game10_pick = self.get_player_featured_game_pick(player)

        if game10_pick.submit_time == None:
            return None

        if self.__submit_time_invalid(week,game10_pick.submit_time):
            return None

        return game10_pick.submit_time

    def __find_player_pick_for_game(self,picks,game):
        if game == None:
            return None
        for pick in picks:
            if pick.game.id == game.id:
                return pick
        return None

    def __game_id_valid(self,game_id):
        return game_id in self.__data.games_id

    def __player_id_valid(self,player_id):
        return player_id in self.__data.players

    def __submit_time_invalid(self,week,submit_time):
        if week == None:
            return False

        pick_deadline_not_set = week.pick_deadline == None
        if pick_deadline_not_set:
            return True

        picks_entered_after_pick_deadline = submit_time > week.pick_deadline
        if picks_entered_after_pick_deadline:
            return True

        return False

