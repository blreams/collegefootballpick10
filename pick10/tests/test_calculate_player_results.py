from django.test import TestCase
from unit_test_database import UnitTestDatabase

class CalculatePlayerResultsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        test_db = UnitTestDatabase()
        super(CalculatePlayerResultsTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        test_db = UnitTestDatabase()
        test_db.delete_database()
        super(CalculatePlayerResultsTests, cls).tearDownClass()

    def test_t6_get_player_results_summary(self):
        return
        self.__t6_test_summary()
        self.__t6_test_summary_week_not_started()
        self.__t6_test_summary_week_not_started_with_defaulters()
        self.__t6_test_summary_week_in_progress()
        self.__t6_test_summary_week_in_progress_with_games_in_progress()
        # TODO tests
        # test player results
        # test bad arguments

    def test_t7_get_player_results_empty_cache(self):
        return
        self.__test_get_player_results_empty_cache(2013,1,PlayerTestData.player_results_2013_week1())
        self.__test_get_player_results_empty_cache(2013,2,PlayerTestData.player_results_2013_week2())
        self.__test_get_player_results_empty_cache(2013,3,PlayerTestData.player_results_2013_week3())
        self.__test_get_player_results_empty_cache(2013,4,PlayerTestData.player_results_2013_week4())
        self.__test_get_player_results_empty_cache(2013,5,PlayerTestData.player_results_2013_week5())
        self.__test_get_player_results_empty_cache(2013,6,PlayerTestData.player_results_2013_week6())
        self.__test_get_player_results_empty_cache(2013,7,PlayerTestData.player_results_2013_week7())
        self.__test_get_player_results_empty_cache(2013,8,PlayerTestData.player_results_2013_week8())
        self.__test_get_player_results_empty_cache(2013,9,PlayerTestData.player_results_2013_week9())
        self.__test_get_player_results_empty_cache(2013,10,PlayerTestData.player_results_2013_week10())
        self.__test_get_player_results_empty_cache(2013,11,PlayerTestData.player_results_2013_week11())
        self.__test_get_player_results_empty_cache(2013,12,PlayerTestData.player_results_2013_week12())
        self.__test_get_player_results_empty_cache(2013,13,PlayerTestData.player_results_2013_week13())

    def test_t8_get_player_results_populated_cache(self):
        return
        self.__test_get_player_results_populated_cache(2013,1,PlayerTestData.player_results_2013_week1())
        self.__test_get_player_results_populated_cache(2013,2,PlayerTestData.player_results_2013_week2())
        self.__test_get_player_results_populated_cache(2013,3,PlayerTestData.player_results_2013_week3())
        self.__test_get_player_results_populated_cache(2013,4,PlayerTestData.player_results_2013_week4())
        self.__test_get_player_results_populated_cache(2013,5,PlayerTestData.player_results_2013_week5())
        self.__test_get_player_results_populated_cache(2013,6,PlayerTestData.player_results_2013_week6())
        self.__test_get_player_results_populated_cache(2013,7,PlayerTestData.player_results_2013_week7())
        self.__test_get_player_results_populated_cache(2013,8,PlayerTestData.player_results_2013_week8())
        self.__test_get_player_results_populated_cache(2013,9,PlayerTestData.player_results_2013_week9())
        self.__test_get_player_results_populated_cache(2013,10,PlayerTestData.player_results_2013_week10())
        self.__test_get_player_results_populated_cache(2013,11,PlayerTestData.player_results_2013_week11())
        self.__test_get_player_results_populated_cache(2013,12,PlayerTestData.player_results_2013_week12())
        self.__test_get_player_results_populated_cache(2013,13,PlayerTestData.player_results_2013_week13())

    def test_t9_get_player_results(self):
        return
        self.__t9_week_not_started()
        self.__t9_week_not_started_defaulter()
        self.__t9_week_in_progress()
