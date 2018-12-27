from .base import FunctionalTest
from django.urls import reverse
from pick10.tests.unit_test_database import *
import unittest
from django.core.cache import cache
from .utils import *

class TiebreakTest(FunctionalTest):

    def setUp(self):
        cache.clear()
        super(TiebreakTest, self).setUp()
        self.utils = Utils(self.browser,self.server_url)
        self.utils.login_unassigned_user()

    def test_page_up(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)

        self.__open_tiebreak_page(year=2013,week=1)
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Week 1 Tiebreaker',title)

        test_db.delete_database()

    def test_featured_game_not_started(self):
        pass

    def test_no_tiebreak_necessary(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)

        self.__open_tiebreak_page(year=2013,week=1)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('No tiebreaker is required.',body)

        test_db.delete_database()

    def test_tiebreak0(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_year(2013)

        self.__open_tiebreak_page(year=2013,week=5)

        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Week 5 Tiebreaker',title)

        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Tiebreaker 0 Details',body)
        self.assertNotIn('Tiebreaker 1 Details',body)
        self.assertNotIn('Tiebreaker 2 Details',body)
        self.assertNotIn('Tiebreaker 3 Details',body)

        test_db.delete_database()

    def test_tiebreak1(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_year(2013)

        self.__open_tiebreak_page(year=2013,week=7)

        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Week 7 Tiebreaker',title)

        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Tiebreaker 0 Details',body)
        self.assertIn('Tiebreaker 1 Details',body)
        self.assertNotIn('Tiebreaker 2 Details',body)
        self.assertNotIn('Tiebreaker 3 Details',body)

        test_db.delete_database()

    def test_tiebreak2(self):
        pass

    def test_tiebreak3(self):
        pass

    def test_week_no_games(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1978,1)
        test_db.setup_week_with_no_games(1978,2)

        # make sure week 1 page is up
        self.__open_tiebreak_page(year=1978,week=1)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Week 1 Tiebreaker',body)
        self.assertIn('Summary',body)

        # check for error message on week 2
        self.__open_tiebreak_page(year=1978,week=2)

        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('The week is currently being setup.',body)

        test_db.delete_database()

    def __open_tiebreak_page(self,year,week):
        address = self.server_url + reverse('tiebreak',args=(year,week))
        self.browser.get(address)
