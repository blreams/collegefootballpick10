from pick10.week_results import *
from utils import *

class WeekNotStartedWithDefaultersResults:

    def __init__(self,players,use_private_names=False):
        self.utils = TestDataUtils(players,use_private_names)

    def week_results(self):
        results = []
        self.utils.add_week_result(results,rank=1,projected_rank=1,player_name='Brent',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.utils.add_week_result(results,rank=1,projected_rank=1,player_name='Byron',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.utils.add_week_result(results,rank=1,projected_rank=1,player_name='Alice',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.utils.add_week_result(results,rank=1,projected_rank=1,player_name='Joan',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.utils.add_week_result(results,rank=1,projected_rank=1,player_name='Bill',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.utils.add_week_result(results,rank=1,projected_rank=1,player_name='David',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.utils.add_week_result(results,rank=1,projected_rank=1,player_name='Amy',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.utils.add_week_result(results,rank=1,projected_rank=1,player_name='Annie',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.utils.add_week_result(results,rank=9,projected_rank=9,player_name='Kevin',wins=0,losses=10,win_pct=0.000,projected_wins=0,possible_wins=0)
        self.utils.add_week_result(results,rank=9,projected_rank=9,player_name='John',wins=0,losses=10,win_pct=0.000,projected_wins=0,possible_wins=0)
        return results
