class WeekResults:
    rank = None
    projected_rank = None
    player_id = None
    player_name = None
    wins = None
    losses = None
    win_pct = None
    projected_wins = None
    possible_wins = None
    winner = None

    def get_dict(self):
        d = dict()
        d['rank'] = self.rank
        d['projected_rank'] = self.projected_rank
        d['player_id'] = self.player_id
        d['player_name'] = self.player_name
        d['wins'] = self.wins
        d['losses'] = self.losses
        d['win_pct'] = self.win_pct
        d['projected_wins'] = self.projected_wins
        d['possible_wins'] = self.possible_wins
        d['winner'] = self.winner
        return d
        
