from pick10.week_results import *

class TestDataUtils:

    def __init__(self,players,use_private_names=False):
        self.__players = players
        self.__use_private_names = use_private_names

    def add_week_result(self,results,rank=None,projected_rank=None,player_name=None,wins=None,losses=None,win_pct=None,projected_wins=None,possible_wins=None,winner=None):
        player = self.find_player(player_name)

        result = WeekResults()
        result.rank = rank
        result.projected_rank = projected_rank
        result.player_id = player.id
        result.wins = wins
        result.losses = losses
        result.win_pct = "%0.3f" % (win_pct)
        result.projected_wins = projected_wins
        result.possible_wins = possible_wins

        if self.__use_private_names:
            result.player_name = player.private_name
        else:
            result.player_name = player.public_name

        result.winner = None
        if winner != None:
            result.winner = player.id
        else:
            result.winner = None
        results.append(result)

    def find_player(self,ss_name):
        for player_id in self.__players:
            player = self.__players[player_id]
            if player and player.ss_name == ss_name:
                return player
        raise AssertionError,"Could not find player %s" % (ss_name)
