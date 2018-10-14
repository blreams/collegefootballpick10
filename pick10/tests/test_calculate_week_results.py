from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

import random
from django.test import TestCase
from .data.week_results_2013 import WeekResults2013
from .data.week_not_started_results import WeekNotStartedResults
from .data.week_not_started_with_defaulters_results import WeekNotStartedWithDefaultersResults
from .data.week_in_progress_results import WeekInProgressResults
from .data.week_in_progress_games_in_progress_results import WeekInProgressGamesInProgressResults
from .data.utils import TestDataUtils
from ..models import Player
from ..database import Database
from ..calculator import NOT_STARTED, IN_PROGRESS, FINAL
from ..calculate_week_results import CalculateWeekResults
from .unit_test_database import UnitTestDatabase

class CalculateWeekResultsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        print("Loading database with data from 2013...(may take a few minutes)")
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_year(2013)
        test_db.setup_week_not_started(1978,6)
        test_db.setup_week_not_started_with_defaulters(1978,7)
        test_db.setup_week_in_progress(1978,8)
        test_db.setup_week_in_progress_games_in_progress(1978,9)
        super(CalculateWeekResultsTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        test_db = UnitTestDatabase()
        test_db.delete_database()
        super(CalculateWeekResultsTests, cls).tearDownClass()

    def test_week_results_against_expected_data_with_public_names(self):
        players = self.__get_players(2013)

        data_2013 = WeekResults2013(players,use_private_names=False)
        self.__test_week_results(2013,1,data_2013.week1())
        self.__test_week_results(2013,2,data_2013.week2())
        self.__test_week_results(2013,3,data_2013.week3())
        self.__test_week_results(2013,4,data_2013.week4())
        self.__test_week_results(2013,5,data_2013.week5())
        self.__test_week_results(2013,6,data_2013.week6())
        self.__test_week_results(2013,7,data_2013.week7())
        self.__test_week_results(2013,8,data_2013.week8())
        self.__test_week_results(2013,9,data_2013.week9())
        self.__test_week_results(2013,10,data_2013.week10())
        self.__test_week_results(2013,11,data_2013.week11())
        self.__test_week_results(2013,12,data_2013.week12())
        self.__test_week_results(2013,13,data_2013.week13())

    def test_week_results_against_expected_data_with_private_names(self):
        players = self.__get_players(2013)

        data_2013 = WeekResults2013(players,use_private_names=True)
        self.__test_week_results(2013,1,data_2013.week1(),private_names=True)
        self.__test_week_results(2013,2,data_2013.week2(),private_names=True)
        self.__test_week_results(2013,3,data_2013.week3(),private_names=True)
        self.__test_week_results(2013,4,data_2013.week4(),private_names=True)
        self.__test_week_results(2013,5,data_2013.week5(),private_names=True)
        self.__test_week_results(2013,6,data_2013.week6(),private_names=True)
        self.__test_week_results(2013,7,data_2013.week7(),private_names=True)
        self.__test_week_results(2013,8,data_2013.week8(),private_names=True)
        self.__test_week_results(2013,9,data_2013.week9(),private_names=True)
        self.__test_week_results(2013,10,data_2013.week10(),private_names=True)
        self.__test_week_results(2013,11,data_2013.week11(),private_names=True)
        self.__test_week_results(2013,12,data_2013.week12(),private_names=True)
        self.__test_week_results(2013,13,data_2013.week13(),private_names=True)

    def test_t1_week_not_started(self):
        self.__t1_week_not_started()
        self.__t1_week_not_started_with_defaulters()

    def test_t2_assign_rank(self):
        self.utils = TestDataUtils(None)
        self.__t2_win_loss_all_different()
        self.__t2_week_not_started()
        self.__t2_week_not_started_with_defaulters()
        self.__t2_week_not_started_with_some_missing_picks()
        self.__t2_win_loss_with_ties()
        self.__t2_win_loss_with_ties_less_than_10_games_complete()
        self.__t2_win_loss_with_first_place_ties()
        self.__t2_win_loss_with_first_place_ties_and_winner_specified()
        self.__t2_winner_missing()
        self.__t2_winner_insane()

    def test_t3_assign_projected_rank(self):
        self.utils = TestDataUtils(None)
        self.__t3_wins_all_different()
        self.__t3_week_not_started()
        self.__t3_week_not_started_with_defaulters()
        self.__t3_week_not_started_with_some_missing_picks()
        self.__t3_wins_with_ties()
        self.__t3_less_than_10_wins()
        self.__t3_all_wins_0()
        self.__t3_first_place_ties()
        self.__t3_winner_specified()
        self.__t3_first_place_tie_with_winner_specified()
        self.__t3_winner_missing()
        self.__t3_winner_insane()

    def test_t4_get_week_results_week_in_progress(self):
        self.__t4_week_in_progress()
        self.__t4_week_in_progress_with_games_in_progress()

    def test_t5_get_week_state(self):
        self.__t5_week_not_started()
        self.__t5_week_in_progress()
        self.__t5_week_final()

    def __t1_week_not_started(self):
        players = self.__get_players(1978)
        wns = WeekNotStartedResults(players)
        self.__test_week_results(1978,6,wns.week_results())

    def __t1_week_not_started_with_defaulters(self):
        players = self.__get_players(1978)
        wnsd = WeekNotStartedWithDefaultersResults(players)
        self.__test_week_results(1978,7,wnsd.week_results())

    def __t2_win_loss_all_different(self):
        week_results = []
        self.utils.add_week_result(week_results,rank=None,expected_rank=11,wins=0,losses=10)
        self.utils.add_week_result(week_results,rank=None,expected_rank=10,wins=1,losses=9)
        self.utils.add_week_result(week_results,rank=None,expected_rank=9,wins=2,losses=8)
        self.utils.add_week_result(week_results,rank=None,expected_rank=8,wins=3,losses=7)
        self.utils.add_week_result(week_results,rank=None,expected_rank=7,wins=4,losses=6)
        self.utils.add_week_result(week_results,rank=None,expected_rank=6,wins=5,losses=5)
        self.utils.add_week_result(week_results,rank=None,expected_rank=5,wins=6,losses=4)
        self.utils.add_week_result(week_results,rank=None,expected_rank=4,wins=7,losses=3)
        self.utils.add_week_result(week_results,rank=None,expected_rank=3,wins=8,losses=2)
        self.utils.add_week_result(week_results,rank=None,expected_rank=2,wins=9,losses=1)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=10,losses=0)

        self.__run_assign_rank_test(week_results)

    def __t2_week_not_started(self): 
        # in the week not started case, all records are 0-0
        # all should be tied for first place
        week_results = []
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)

        self.__run_assign_rank_test(week_results)

    def __t2_week_not_started_with_defaulters(self): 
        # in the week not started case, players with picks have record 0-0
        # defaulters have a record of 0-10
        # defaulters tied for last place, all others tied for first place
        week_results = []
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=9,wins=0,losses=10)
        self.utils.add_week_result(week_results,rank=None,expected_rank=9,wins=0,losses=10)
        self.utils.add_week_result(week_results,rank=None,expected_rank=9,wins=0,losses=10)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)

        self.__run_assign_rank_test(week_results)

    def __t2_week_not_started_with_some_missing_picks(self): 
        # not started player with picks have record 0-0
        # not started player with missing picks have losses 0-#losses
        week_results = []
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=0,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=7,wins=0,losses=1)
        self.utils.add_week_result(week_results,rank=None,expected_rank=7,wins=0,losses=1)
        self.utils.add_week_result(week_results,rank=None,expected_rank=9,wins=0,losses=2)
        self.utils.add_week_result(week_results,rank=None,expected_rank=10,wins=0,losses=10)
        self.utils.add_week_result(week_results,rank=None,expected_rank=10,wins=0,losses=10)

        self.__run_assign_rank_test(week_results)

    def __t2_win_loss_with_ties(self):
        week_results = []
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=10,losses=0)
        self.utils.add_week_result(week_results,rank=None,expected_rank=2,wins=9,losses=1)
        self.utils.add_week_result(week_results,rank=None,expected_rank=2,wins=9,losses=1)
        self.utils.add_week_result(week_results,rank=None,expected_rank=4,wins=8,losses=2)
        self.utils.add_week_result(week_results,rank=None,expected_rank=4,wins=8,losses=2)
        self.utils.add_week_result(week_results,rank=None,expected_rank=6,wins=7,losses=3)
        self.utils.add_week_result(week_results,rank=None,expected_rank=6,wins=7,losses=3)
        self.utils.add_week_result(week_results,rank=None,expected_rank=8,wins=6,losses=4)
        self.utils.add_week_result(week_results,rank=None,expected_rank=8,wins=6,losses=4)
        self.utils.add_week_result(week_results,rank=None,expected_rank=10,wins=5,losses=5)
        self.utils.add_week_result(week_results,rank=None,expected_rank=10,wins=5,losses=5)
        self.utils.add_week_result(week_results,rank=None,expected_rank=12,wins=4,losses=6)
        self.utils.add_week_result(week_results,rank=None,expected_rank=12,wins=4,losses=6)
        self.utils.add_week_result(week_results,rank=None,expected_rank=14,wins=3,losses=7)
        self.utils.add_week_result(week_results,rank=None,expected_rank=14,wins=3,losses=7)
        self.utils.add_week_result(week_results,rank=None,expected_rank=16,wins=2,losses=8)
        self.utils.add_week_result(week_results,rank=None,expected_rank=16,wins=2,losses=8)
        self.utils.add_week_result(week_results,rank=None,expected_rank=18,wins=1,losses=9)
        self.utils.add_week_result(week_results,rank=None,expected_rank=18,wins=1,losses=9)
        self.utils.add_week_result(week_results,rank=None,expected_rank=20,wins=0,losses=10)
        self.utils.add_week_result(week_results,rank=None,expected_rank=20,wins=0,losses=10)

        self.__run_assign_rank_test(week_results)

    def __t2_win_loss_with_ties_less_than_10_games_complete(self):
        week_results = []
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=5,losses=1)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=5,losses=1)
        self.utils.add_week_result(week_results,rank=None,expected_rank=3,wins=4,losses=2)
        self.utils.add_week_result(week_results,rank=None,expected_rank=3,wins=4,losses=2)
        self.utils.add_week_result(week_results,rank=None,expected_rank=3,wins=4,losses=2)
        self.utils.add_week_result(week_results,rank=None,expected_rank=6,wins=3,losses=3)
        self.utils.add_week_result(week_results,rank=None,expected_rank=6,wins=3,losses=3)
        self.utils.add_week_result(week_results,rank=None,expected_rank=6,wins=3,losses=3)
        self.utils.add_week_result(week_results,rank=None,expected_rank=9,wins=2,losses=4)
        self.utils.add_week_result(week_results,rank=None,expected_rank=9,wins=2,losses=4)
        self.utils.add_week_result(week_results,rank=None,expected_rank=11,wins=1,losses=5)

        self.__run_assign_rank_test(week_results)

    def __t2_win_loss_with_first_place_ties(self):
        week_results = []
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=8,losses=2)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=8,losses=2)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=8,losses=2)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=8,losses=2)
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=8,losses=2)
        self.utils.add_week_result(week_results,rank=None,expected_rank=6,wins=7,losses=3)
        self.utils.add_week_result(week_results,rank=None,expected_rank=7,wins=6,losses=4)
        self.utils.add_week_result(week_results,rank=None,expected_rank=7,wins=6,losses=4)
        self.utils.add_week_result(week_results,rank=None,expected_rank=9,wins=5,losses=5)
        self.utils.add_week_result(week_results,rank=None,expected_rank=10,wins=4,losses=6)
        self.utils.add_week_result(week_results,rank=None,expected_rank=11,wins=3,losses=7)
        self.utils.add_week_result(week_results,rank=None,expected_rank=12,wins=2,losses=8)
        self.utils.add_week_result(week_results,rank=None,expected_rank=13,wins=1,losses=9)
        self.utils.add_week_result(week_results,rank=None,expected_rank=14,wins=0,losses=10)
        self.utils.add_week_result(week_results,rank=None,expected_rank=14,wins=0,losses=10)

        self.__run_assign_rank_test(week_results)

    def __t2_win_loss_with_first_place_ties_and_winner_specified(self): 
        week_results = []
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=8,losses=2,player_id=15)
        self.utils.add_week_result(week_results,rank=None,expected_rank=2,wins=8,losses=2,player_id=14)
        self.utils.add_week_result(week_results,rank=None,expected_rank=2,wins=8,losses=2,player_id=13)
        self.utils.add_week_result(week_results,rank=None,expected_rank=2,wins=8,losses=2,player_id=12)
        self.utils.add_week_result(week_results,rank=None,expected_rank=2,wins=8,losses=2,player_id=11)
        self.utils.add_week_result(week_results,rank=None,expected_rank=6,wins=7,losses=3,player_id=10)
        self.utils.add_week_result(week_results,rank=None,expected_rank=7,wins=6,losses=4,player_id=9)
        self.utils.add_week_result(week_results,rank=None,expected_rank=7,wins=6,losses=4,player_id=8)
        self.utils.add_week_result(week_results,rank=None,expected_rank=9,wins=5,losses=5,player_id=7)
        self.utils.add_week_result(week_results,rank=None,expected_rank=10,wins=4,losses=6,player_id=6)
        self.utils.add_week_result(week_results,rank=None,expected_rank=11,wins=3,losses=7,player_id=5)
        self.utils.add_week_result(week_results,rank=None,expected_rank=12,wins=2,losses=8,player_id=4)
        self.utils.add_week_result(week_results,rank=None,expected_rank=13,wins=1,losses=9,player_id=3)
        self.utils.add_week_result(week_results,rank=None,expected_rank=14,wins=0,losses=10,player_id=2)
        self.utils.add_week_result(week_results,rank=None,expected_rank=14,wins=0,losses=10,player_id=1)

        self.__run_assign_rank_test(week_results,winner=15)

    def __t2_winner_missing(self):
        week_results = []
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=8,losses=2,player_id=15)
        self.utils.add_week_result(week_results,rank=None,expected_rank=2,wins=8,losses=2,player_id=14)
        self.utils.add_week_result(week_results,rank=None,expected_rank=2,wins=8,losses=2,player_id=13)
        self.utils.add_week_result(week_results,rank=None,expected_rank=4,wins=8,losses=2,player_id=12)
        self.utils.add_week_result(week_results,rank=None,expected_rank=4,wins=8,losses=2,player_id=11)
        self.utils.add_week_result(week_results,rank=None,expected_rank=6,wins=7,losses=3,player_id=10)
        self.utils.add_week_result(week_results,rank=None,expected_rank=8,wins=6,losses=4,player_id=9)
        self.utils.add_week_result(week_results,rank=None,expected_rank=8,wins=6,losses=4,player_id=8)
        self.utils.add_week_result(week_results,rank=None,expected_rank=10,wins=5,losses=5,player_id=7)
        self.utils.add_week_result(week_results,rank=None,expected_rank=12,wins=4,losses=6,player_id=6)
        self.utils.add_week_result(week_results,rank=None,expected_rank=14,wins=3,losses=7,player_id=5)
        self.utils.add_week_result(week_results,rank=None,expected_rank=16,wins=2,losses=8,player_id=4)
        self.utils.add_week_result(week_results,rank=None,expected_rank=18,wins=1,losses=9,player_id=3)
        self.utils.add_week_result(week_results,rank=None,expected_rank=20,wins=0,losses=10,player_id=2)
        self.utils.add_week_result(week_results,rank=None,expected_rank=20,wins=0,losses=10,player_id=1)

        with self.assertRaises(Exception):
            self.__run_assign_rank_test(winner=255,num_tests=1)

    def __t2_winner_insane(self):
        week_results = []
        self.utils.add_week_result(week_results,rank=None,expected_rank=1,wins=8,losses=2,player_id=15)
        self.utils.add_week_result(week_results,rank=None,expected_rank=2,wins=8,losses=2,player_id=14)
        self.utils.add_week_result(week_results,rank=None,expected_rank=2,wins=8,losses=2,player_id=13)
        self.utils.add_week_result(week_results,rank=None,expected_rank=4,wins=8,losses=2,player_id=12)
        self.utils.add_week_result(week_results,rank=None,expected_rank=4,wins=8,losses=2,player_id=11)
        self.utils.add_week_result(week_results,rank=None,expected_rank=6,wins=7,losses=3,player_id=10)
        self.utils.add_week_result(week_results,rank=None,expected_rank=8,wins=6,losses=4,player_id=9)
        self.utils.add_week_result(week_results,rank=None,expected_rank=8,wins=6,losses=4,player_id=8)
        self.utils.add_week_result(week_results,rank=None,expected_rank=10,wins=5,losses=5,player_id=7)
        self.utils.add_week_result(week_results,rank=None,expected_rank=12,wins=4,losses=6,player_id=6)
        self.utils.add_week_result(week_results,rank=None,expected_rank=14,wins=3,losses=7,player_id=5)
        self.utils.add_week_result(week_results,rank=None,expected_rank=16,wins=2,losses=8,player_id=4)
        self.utils.add_week_result(week_results,rank=None,expected_rank=18,wins=1,losses=9,player_id=3)
        self.utils.add_week_result(week_results,rank=None,expected_rank=20,wins=0,losses=10,player_id=2)
        self.utils.add_week_result(week_results,rank=None,expected_rank=20,wins=0,losses=10,player_id=1)

        with self.assertRaises(Exception):
            self.__run_assign_rank_test(winner=8,num_tests=1)

    def __t3_wins_all_different(self):
        week_results = []
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=11,projected_wins=0)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=10,projected_wins=1)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=9,projected_wins=2)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=8,projected_wins=3)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=7,projected_wins=4)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=6,projected_wins=5)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=5,projected_wins=6)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=4,projected_wins=7)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=3,projected_wins=8)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=2,projected_wins=9)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)

        self.__run_assign_projected_rank_test(week_results)

    def __t3_week_not_started(self): 
        # in the week not started case, player projected to win all games
        # all should be tied for first place
        week_results = []
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)

        self.__run_assign_projected_rank_test(week_results)

    def __t3_week_not_started_with_defaulters(self): 
        # in the week not started case, players with picks projected to win all games
        # defaulters should be projected to win 0 games
        # players with picks tied for 1st, defaulters tied for last place
        week_results = []
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=8,projected_wins=0)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=8,projected_wins=0)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=8,projected_wins=0)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=8,projected_wins=0)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)

        self.__run_assign_projected_rank_test(week_results)

    def __t3_week_not_started_with_some_missing_picks(self): 
        # players with all picks expect to win all games
        # players missing picks expect to lost those games
        week_results = []
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=5,projected_wins=9)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=5,projected_wins=9)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=7,projected_wins=5)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=8,projected_wins=4)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=9,projected_wins=0)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=9,projected_wins=0)

        self.__run_assign_projected_rank_test(week_results)

    def __t3_wins_with_ties(self): 
        week_results = []
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=3,projected_wins=9)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=3,projected_wins=9)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=5,projected_wins=8)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=5,projected_wins=8)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=7,projected_wins=7)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=7,projected_wins=7)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=9,projected_wins=6)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=9,projected_wins=6)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=11,projected_wins=5)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=11,projected_wins=5)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=13,projected_wins=4)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=13,projected_wins=4)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=15,projected_wins=3)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=15,projected_wins=3)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=17,projected_wins=2)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=17,projected_wins=2)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=19,projected_wins=1)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=19,projected_wins=1)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=21,projected_wins=0)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=21,projected_wins=0)

        self.__run_assign_projected_rank_test(week_results)

    def __t3_less_than_10_wins(self): 
        week_results = []
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=7)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=7)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=3,projected_wins=6)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=4,projected_wins=5)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=5,projected_wins=4)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=6,projected_wins=3)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=6,projected_wins=3)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=8,projected_wins=0)

        self.__run_assign_projected_rank_test(week_results)

    def __t3_all_wins_0(self): 
        week_results = []
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=0)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=0)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=0)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=0)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=0)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=0)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=0)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=0)

        self.__run_assign_projected_rank_test(week_results)

    def __t3_first_place_ties(self): 
        week_results = []
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=8)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=8)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=8)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=8)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=8)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=6,projected_wins=5)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=7,projected_wins=4)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=8,projected_wins=3)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=9,projected_wins=2)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=10,projected_wins=1)

        self.__run_assign_projected_rank_test(week_results)

    def __t3_winner_specified(self): 
        week_results = []
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=8,player_id=8)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=2,projected_wins=7,player_id=7)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=3,projected_wins=6,player_id=6)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=4,projected_wins=5,player_id=5)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=5,projected_wins=4,player_id=4)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=6,projected_wins=3,player_id=3)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=7,projected_wins=2,player_id=2)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=8,projected_wins=1,player_id=1)

        self.__run_assign_projected_rank_test(week_results,projected_winner=8)

    def __t3_first_place_tie_with_winner_specified(self): 
        week_results = []
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=2,projected_wins=7,player_id=1)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=2,projected_wins=7,player_id=2)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=7,player_id=3)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=2,projected_wins=7,player_id=4)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=2,projected_wins=7,player_id=5)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=6,projected_wins=6,player_id=6)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=7,projected_wins=5,player_id=7)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=8,projected_wins=4,player_id=8)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=9,projected_wins=3,player_id=9)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=10,projected_wins=2,player_id=10)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=11,projected_wins=1,player_id=11)

        self.__run_assign_projected_rank_test(week_results,projected_winner=3)

    def __t3_winner_missing(self): 
        week_results = []
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=7,player_id=1)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=7,player_id=2)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=7,player_id=3)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=7,player_id=4)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=7,player_id=5)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=6,projected_wins=6,player_id=6)

        with self.assertRaises(Exception):
            self.__run_assign_projected_rank_test(week_results,projected_winner=255,num_tests=1)

    def __t3_winner_insane(self): 
        week_results = []
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=7,player_id=1)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=7,player_id=2)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=7,player_id=3)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=7,player_id=4)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=1,projected_wins=7,player_id=5)
        self.utils.add_week_result(week_results,projected_rank=None,expected_rank=6,projected_wins=6,player_id=6)

        with self.assertRaises(Exception):
            self.__run_assign_projected_rank_test(week_results,projected_winner=6,num_tests=1)

    def __t4_week_in_progress(self):
        players = self.__get_players(1978)
        wip = WeekInProgressResults(players)
        self.__test_week_results(1978,8,wip.week_results())

    def __t4_week_in_progress_with_games_in_progress(self):
        players = self.__get_players(1978)
        wip = WeekInProgressGamesInProgressResults(players)
        self.__test_week_results(1978,9,wip.week_results())

    def __t5_week_not_started(self):
        state = CalculateWeekResults(1978,6).get_week_state()
        self.assertEqual(state,NOT_STARTED)

    def __t5_week_in_progress(self):
        state = CalculateWeekResults(1978,8).get_week_state()
        self.assertEqual(state,IN_PROGRESS)

    def __t5_week_final(self):
        state = CalculateWeekResults(2013,1).get_week_state()
        self.assertEqual(state,FINAL)

    def __test_week_results(self,year,week_number,expected_results,private_names=False):
        results = CalculateWeekResults(year,week_number,private_names).get_results()
        self.__verify_results_ignore_tied_order(results,expected_results)

    def __get_players(self,year):
        return Database().load_players(year)

    def __verify_results_ignore_tied_order(self,results,expected_results):
        self.assertEqual(len(results),len(expected_results))

        first_place_wins = results[0].wins
        first_place_losses = results[0].losses
        first_place_projected_wins = results[0].projected_wins

        for i in range(len(results)):
            result = results[i]
            expected = self.__find_expected_result(result,expected_results)

            self.assertEqual(result.rank,expected.rank)
            self.assertEqual(result.projected_rank,expected.projected_rank)

            self.assertEqual(result.player_id,expected.player_id)
            self.assertEqual(result.player_name,expected.player_name)
            self.assertEqual(result.wins,expected.wins)
            self.assertEqual(result.losses,expected.losses)
            self.assertEqual(result.win_pct,expected.win_pct)
            self.assertEqual(result.projected_wins,expected.projected_wins)
            self.assertEqual(result.possible_wins,expected.possible_wins)
            self.assertEqual(result.winner,expected.winner)

    def __find_expected_result(self,result,expected_results):
        for expected in expected_results:
            if expected.player_name == result.player_name:
                return expected
        raise AssertionError("could not find expected result")

    def __run_assign_rank_test(self,week_results,num_tests=10,winner=None):
        cwr = CalculateWeekResults(year=2013,week_number=1)
        random.seed(777)
        for i in range(num_tests):
            test_results = self.__randomize_results_order(week_results)
            if not(winner):
                assigned_results = cwr.assign_rank(test_results)
            else:
                winner_model = Player()
                winner_model.id = winner
                assigned_results = cwr.assign_rank(test_results,winner=winner_model)
            self.__verify_ranks(assigned_results)

    def __run_assign_projected_rank_test(self,week_results,num_tests=10,projected_winner=None):
        cwr = CalculateWeekResults(year=2013,week_number=1)
        random.seed(888)
        for i in range(num_tests):
            test_results = self.__randomize_results_order(week_results)
            if not(projected_winner):
                assigned_results = cwr.assign_projected_rank(week_results)
            else:
                winner_model = Player()
                winner_model.id = projected_winner
                assigned_results = cwr.assign_projected_rank(week_results,projected_winner=winner_model)
            self.__verify_projected_ranks(assigned_results)

    def __randomize_results_order(self,week_results):
        indexes = list(range(len(week_results)))
        random.shuffle(indexes)

        random_results = []
        for i in indexes:
            random_results.append(week_results[i])

        return random_results

    def __verify_ranks(self,results):
        for result in results:
            self.assertEqual(result.rank,result.expected_rank)

    def __verify_projected_ranks(self,results):
        for result in results:
            self.assertEqual(result.projected_rank,result.expected_rank)
