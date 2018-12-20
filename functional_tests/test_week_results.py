from .base import FunctionalTest
from django.urls import reverse
from pick10.tests.unit_test_database import *
import unittest
from django.core.cache import cache
from .utils import *

class WeekResultsTest(FunctionalTest):

    # Could not get loading the database 1 time per
    # test run of the class to work, so doing it within
    # each test for now

    #@classmethod
    #def setUpClass(cls):
        #super(WeekResultsTest, cls).setUpClass()
        #test_db = UnitTestDatabase()
        #test_db.load_historical_data_for_week(2013,1)

    #@classmethod
    #def tearDownClass(cls):
        #test_db = UnitTestDatabase()
        #test_db.delete_database()
        #super(WeekResultsTest, cls).tearDownClass()

    def setUp(self):
        cache.clear()
        super(WeekResultsTest, self).setUp()
        self.utils = Utils(self.browser,self.server_url)
        self.utils.login_unassigned_user()

    def test_page_up(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)

        self.__open_week_results_page(year=2013,week_number=1)
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Week 1 Leaderboard',title)

        test_db.delete_database()

    def test_week_not_started(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,6)

        self.__open_week_results_page(year=1978,week_number=6)
        week_state = self.browser.find_element_by_id('not-started-week-state').text
        self.assertIn('week has not started',week_state)

        table_header = self.browser.find_element_by_class_name('results-header').text
        self.assertEqual('Rank Player Wins Losses Win Pct. Possible',table_header)

        test_db.delete_database()

    def test_week_in_progress(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_in_progress(1978,8)

        self.__open_week_results_page(year=1978,week_number=8)
        week_state = self.browser.find_element_by_id('in-progress-week-state').text
        self.assertIn('week is in progress',week_state)

        table_header = self.browser.find_element_by_class_name('results-header').text
        self.assertEqual('Rank Player Wins Losses Win Pct. Projected Possible Winner',table_header)

        test_db.delete_database()


    def test_invalid_year(self):
        self.__open_week_results_page(year=1980,week_number=1)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Cannot find 1980 week 1 in the database.',body)

    def test_invalid_week(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)

        self.__open_week_results_page(year=2013,week_number=15)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Cannot find 2013 week 15 in the database.',body)

        test_db.delete_database()

    def test_week_no_games(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1978,1)
        test_db.setup_week_with_no_games(1978,2)

        # make sure week 1 page is up
        self.__open_week_results_page(year=1978,week_number=1)
        self.__is_page_up('Week 1 Leaderboard')

        # check for error message on week 2
        self.__open_week_results_page(year=1978,week_number=2)

        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('The week is currently being setup.',body)

        test_db.delete_database()

    def __open_week_results_page(self,year,week_number):
        address = self.server_url + reverse('week_results',args=(year,week_number))
        self.browser.get(address)

    def __is_page_up(self,title):
        page_title = self.browser.find_element_by_id('page-title').text
        self.assertEqual(title,page_title)

        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Rank',body)
        self.assertIn('Player',body)
        self.assertIn('Wins',body)

