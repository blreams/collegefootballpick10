from .base import FunctionalTest
from django.core.urlresolvers import reverse
from pick10.tests.unit_test_database import *
import unittest

class TiebreakTest(FunctionalTest):

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

    def __open_tiebreak_page(self,year,week):
        address = self.server_url + reverse('tiebreak',args=(year,week))
        self.browser.get(address)
