from .base import FunctionalTest
from django.core.urlresolvers import reverse
from pick10.tests.unit_test_database import *
import unittest

class OverallResultsTest(FunctionalTest):

    @unittest.skip('debug')
    def test_page_up(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_year(2013)

        self.__open_results_page(year=2013)
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('2013 Leaderboard',title)

        test_db.delete_database()

    @unittest.skip('debug')
    def test_bad_year(self):
        self.__open_results_page(year=1980)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Cannot find a pool for the year 1980',body)

    @unittest.skip('debug')
    def test_final_results(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_year(2013)

        self.__open_results_page(year=2013)

        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('2013 Leaderboard',title)

        header = self.browser.find_element_by_class_name('results-header').text
        expected = 'Rank Player Overall Win Pct. Wk1 Wk2 Wk3 Wk4 Wk5 Wk6 Wk7 Wk8 Wk9 Wk10 Wk11 Wk12 Wk13'
        self.assertEqual(expected,header)

        test_db.delete_database()

    @unittest.skip('debug')
    def test_pool_not_started(self):
        test_db = UnitTestDatabase()
        test_db.setup_pool_not_started(1975)

        self.__open_results_page(year=1975)

        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('1975 Leaderboard',title)

        message = self.browser.find_element_by_id('year-not-started').text
        self.assertEqual('The pool has not started.',message)

        test_db.delete_database()

    @unittest.skip('debug')
    def test_enter_picks(self):
        pass

    def test_week_not_started(self):
        test_db = UnitTestDatabase()

        test_db.setup_week_final(1978,1)
        test_db.setup_week_final(1978,2)
        test_db.setup_week_final(1978,3)
        test_db.setup_week_not_started(1978,4)

        self.__open_results_page(year=1978)
        import pdb; pdb.set_trace()

        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('1978 Leaderboard',title)

        header = self.browser.find_element_by_class_name('results-header').text
        expected = 'Rank Player Overall Possible Win Pct. Wk1 Wk2 Wk3 Wk4'
        self.assertEqual(expected,header)

        test_db.delete_database()

    @unittest.skip('debug')
    def test_week_in_progress(self):
        pass

    @unittest.skip('debug')
    def test_week_final(self):
        pass

    def __open_results_page(self,year):
        address = self.server_url + reverse('overall_results',args=(year,))
        self.browser.get(address)
