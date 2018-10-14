class WeekData:
    week = None
    games = None
    games_id = None
    player_picks = None
    picks = None
    teams = None
    players = None

    def get_player(self,private_name):
        for player_id in self.players:
            player = self.players[player_id]
            if player and player.private_name == private_name:
                return player
        raise AssertionError("Could not find player %s" % (private_name))

