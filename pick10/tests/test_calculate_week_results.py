from django.test import TestCase
from pick10.tests.data.week_results_2013 import *
from pick10.database import *
from pick10.calculate_week_results import *
from unit_test_database import *

class CalculateWeekResultsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        print "Loading database with data from 2013...(may take a few minutes)"
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_year(2013)
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
        return
        self.__t1_week_not_started()
        self.__t1_week_not_started_with_defaulters()

    def test_t2_assign_rank(self):
        return
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
        return
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
        return
        self.__t4_week_in_progress()
        self.__t4_week_in_progress_with_games_in_progress()

    def test_t5_get_week_state(self):
        return
        self.__t5_week_not_started()
        self.__t5_week_in_progress()
        self.__t5_week_final()

    def __t1_week_not_started(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,6)
        expected_results = None
        self.__test_week_results(1978,6,expected_results)

    def __t1_week_not_started_with_defaulters(self):
        self.fail('not implemented yet')
        testdata = WeekNotStartedWithDefaulters(leave_objects_in_datastore=False)
        testdata.setup()
        self.__test_get_week_results(testdata.year,testdata.week_number,testdata.get_expected_results())
        testdata.cleanup()

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
            # TODO self.assertEqual(results.winner,expected.winner)

    def __find_expected_result(self,result,expected_results):
        for expected in expected_results:
            if expected.player_name == result.player_name:
                return expected
        raise AssertionError,"could not find expected result"
