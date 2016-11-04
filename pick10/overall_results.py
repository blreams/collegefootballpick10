class OverallResults:
    rank = None
    projected_rank = None
    player_id = None
    player_name = None
    overall = None
    projected = None
    possible = None
    win_pct = None
    week_points_info = None
    last_week_projected = None
    last_week_possible = None

    def get_dict(self):
        d = dict()
        d['rank'] = self.rank
        d['projected_rank'] = self.projected_rank
        d['player_id'] = self.player_id
        d['player_name'] = self.player_name
        d['overall'] = self.overall
        d['projected'] = self.projected
        d['possible'] = self.possible
        d['win_pct'] = self.win_pct
        d['week_points'] = self.week_points
        d['last_week_projected'] = self.last_week_projected
        d['last_week_possible'] = self.last_week_possible
        return d
