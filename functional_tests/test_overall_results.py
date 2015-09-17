from .base import FunctionalTest
from django.core.urlresolvers import reverse
from pick10.tests.unit_test_database import *
import unittest
import datetime as dt
import pytz
from django.core.cache import *
from utils import *

class OverallResultsTest(FunctionalTest):

    def setUp(self):
        cache = get_cache('default')
        cache.clear()
        super(OverallResultsTest, self).setUp()
        self.utils = Utils(self.browser,self.server_url)
        self.utils.login_unassigned_user()

    def test_page_up(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_year(2013)

        self.utils.overall_results_page(year=2013)
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('2013 Leaderboard',title)

        test_db.delete_database()

    def test_bad_year(self):
        self.utils.overall_results_page(year=1980)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Cannot find a pool for the year 1980',body)

    def test_final_results(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_year(2013)

        self.utils.overall_results_page(year=2013)

        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('2013 Leaderboard',title)

        header = self.browser.find_element_by_class_name('results-header').text
        expected = 'Rank Player Overall Win Pct. Wk1 Wk2 Wk3 Wk4 Wk5 Wk6 Wk7 Wk8 Wk9 Wk10 Wk11 Wk12 Wk13'
        self.assertEqual(expected,header)

        test_db.delete_database()

    def test_pool_not_started(self):
        test_db = UnitTestDatabase()
        test_db.setup_pool_not_started(1975)

        self.utils.overall_results_page(year=1975)

        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('1975 Leaderboard',title)

        message = self.browser.find_element_by_id('year-not-started').text
        self.assertEqual('The pool has not started.',message)

        test_db.delete_database()

    def test_enter_picks(self):
        test_db = UnitTestDatabase()

        test_db.setup_week_final(1978,1)
        test_db.setup_week_final(1978,2)
        test_db.setup_week_final(1978,3)
        test_db.setup_week_not_started(1978,4)

        # set pick deadline so it hasn't been expired
        week = get_week(1978,4)
        naive_dt_now = dt.datetime.now()
        naive_dt_deadline = dt.datetime(naive_dt_now.year, naive_dt_now.month, naive_dt_now.day, 16, 0, 0) + timedelta(days=1)
        deadline = pytz.timezone('US/Eastern').localize(naive_dt_deadline)
        week.pick_deadline = deadline
        week.lock_picks = False
        week.save()

        self.utils.overall_results_page(year=1978)

        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('1978 Leaderboard',title)

        message = self.browser.find_element_by_id('enterpicks-pool-state').text
        expected = 'currently entering picks for week 4'
        self.assertEqual(expected,message)

        header = self.browser.find_element_by_class_name('results-header').text
        expected = 'Rank Player Overall Win Pct. Wk1 Wk2 Wk3 Wk4'
        self.assertEqual(expected,header)

        test_db.delete_database()

    def test_week_not_started(self):
        test_db = UnitTestDatabase()

        test_db.setup_week_final(1978,1)
        test_db.setup_week_final(1978,2)
        test_db.setup_week_final(1978,3)
        test_db.setup_week_not_started(1978,4)

        self.utils.overall_results_page(year=1978)

        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('1978 Leaderboard',title)

        header = self.browser.find_element_by_class_name('results-header').text
        expected = 'Rank Player Overall Possible Win Pct. Wk1 Wk2 Wk3 Wk4'
        self.assertEqual(expected,header)

        test_db.delete_database()

    def test_week_in_progress(self):
        test_db = UnitTestDatabase()

        test_db.setup_week_final(1978,1)
        test_db.setup_week_final(1978,2)
        test_db.setup_week_in_progress(1978,3)

        self.utils.overall_results_page(year=1978)

        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('1978 Leaderboard',title)

        header = self.browser.find_element_by_class_name('results-header').text
        expected = 'Rank Player Overall Projected Possible Win Pct. Wk1 Wk2 Wk3 Wk3 Projected Wk3 Possible'
        self.assertEqual(expected,header)

        test_db.delete_database()

    def test_week_final(self):
        test_db = UnitTestDatabase()

        test_db.setup_week_final(1978,1)
        test_db.setup_week_final(1978,2)

        self.utils.overall_results_page(year=1978)

        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('1978 Leaderboard',title)

        header = self.browser.find_element_by_class_name('results-header').text
        expected = 'Rank Player Overall Possible Win Pct. Wk1 Wk2'
        self.assertEqual(expected,header)

        test_db.delete_database()

    def test_week_no_games(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1978,1)
        test_db.setup_week_with_no_games(1978,2)

        self.utils.overall_results_page(year=1978)

        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('1978 Leaderboard',body)
        self.assertIn('week 1 final',body)

        test_db.delete_database()
