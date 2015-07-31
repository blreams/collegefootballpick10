from pick10.week_results import *
from utils import *

class WeekInProgressGamesInProgressResults:

    def __init__(self,players,use_private_names=False):
        self.utils = TestDataUtils(players,use_private_names)

    def week_results(self):
        results = []
        self.utils.add_week_result(results,rank=1,projected_rank=1,player_name='Brent',wins=6,losses=0,win_pct=1.000,projected_wins=9,possible_wins=10)
        self.utils.add_week_result(results,rank=1,projected_rank=2,player_name='Byron',wins=6,losses=0,win_pct=1.000,projected_wins=8,possible_wins=10)
        self.utils.add_week_result(results,rank=3,projected_rank=2,player_name='Alice',wins=5,losses=1,win_pct=0.833,projected_wins=8,possible_wins=9)
        self.utils.add_week_result(results,rank=3,projected_rank=5,player_name='Joan',wins=5,losses=1,win_pct=0.833,projected_wins=6,possible_wins=9)
        self.utils.add_week_result(results,rank=5,projected_rank=4,player_name='Bill',wins=4,losses=2,win_pct=0.667,projected_wins=7,possible_wins=8)
        self.utils.add_week_result(results,rank=5,projected_rank=6,player_name='David',wins=4,losses=2,win_pct=0.667,projected_wins=5,possible_wins=8)
        self.utils.add_week_result(results,rank=7,projected_rank=6,player_name='Amy',wins=3,losses=3,win_pct=0.500,projected_wins=5,possible_wins=7)
        self.utils.add_week_result(results,rank=7,projected_rank=8,player_name='Annie',wins=3,losses=3,win_pct=0.500,projected_wins=4,possible_wins=7)
        self.utils.add_week_result(results,rank=9,projected_rank=9,player_name='Kevin',wins=1,losses=5,win_pct=0.167,projected_wins=2,possible_wins=5)
        self.utils.add_week_result(results,rank=10,projected_rank=10,player_name='John',wins=0,losses=10,win_pct=0.000,projected_wins=0,possible_wins=0)
        return results
