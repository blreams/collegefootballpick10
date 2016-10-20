from django.test import TestCase
from unit_test_database import UnitTestDatabase
from pick10.calculate_overall_results import CalculateOverallResults
from pick10.models import calc_completed_games

class CalculateOverallResultsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_year(2013)
        super(CalculateOverallResultsTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        test_db = UnitTestDatabase()
        test_db.delete_database()
        super(CalculateOverallResultsTests, cls).tearDownClass()

    def test_get_results(self):
        cgs = calc_completed_games(2013)
        c = CalculateOverallResults(2013, cgs)
        results = c.get_results()
        self.assertIsNotNone(results)

    def test_t10_assign_overall_rank(self):
        return
        self.__t10_overall_all_different()
        self.__t10_overall_all_tied()
        self.__t10_overall_mixed_values()

    def test_t11_assign_overall_projected_rank(self):
        return
        self.__t11_projected_rank_all_different()
        self.__t11_projected_rank_all_tied()
        self.__t11_projected_rank_mixed_values()
