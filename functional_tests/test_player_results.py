from .base import FunctionalTest
from django.core.urlresolvers import reverse
from pick10.tests.unit_test_database import *
import unittest

class PlayerResultsTest(FunctionalTest):

    @unittest.skip('not ready to test')
    def test_page_up(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)

        self.__open_week_results_page(year=2013,week_number=1)
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Week 1 Leaderboard',title)

        test_db.delete_database()

    def test_bad_player_id(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)

        self.__open_week_results_page(year=2013,week_number=1,player_id=0)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Cannot find player 0 in the database.',body)

        test_db.delete_database()

    def test_bad_player_id_year(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)

        # setup a player in a different year
        week = test_db.setup_week(2012,1)
        player_2012 = test_db.setup_player(2012,'Player2012')

        self.__open_week_results_page(year=2013,week_number=1,player_id=player_2012.id)
        body = self.browser.find_element_by_tag_name('body').text
        expected = "Player %d is not participating in the 2013 pool." % (player_2012.id)
        self.assertIn(expected,body)

        test_db.delete_database()

    def test_invalid_year(self):
        self.__open_week_results_page(year=1980,week_number=1,player_id=1)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Cannot find 1980 week 1 in the database.',body)

    def test_invalid_week(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)

        self.__open_week_results_page(year=2013,week_number=15,player_id=1)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Cannot find 2013 week 15 in the database.',body)

        test_db.delete_database()

    def __open_week_results_page(self,year,week_number,player_id):
        address = self.server_url + reverse('player_results',args=(year,week_number,player_id))
        self.browser.get(address)

