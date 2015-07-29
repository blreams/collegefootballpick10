from django.test import TestCase
from unit_test_database import *

class CalculateOverallResultsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        test_db = UnitTestDatabase()
        super(CalculateOverallResultsTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        test_db = UnitTestDatabase()
        test_db.delete_database()
        super(CalculateOverallResultsTests, cls).tearDownClass()

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
