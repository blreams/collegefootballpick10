from .base import FunctionalTest
from django.urls import reverse
from pick10.tests.unit_test_database import *
from pick10.database import *
import unittest
from django.core.cache import cache
from django.utils import timezone as tz
from datetime import timedelta
from .utils import *

class PlayerResultsTest(FunctionalTest):

    def setUp(self):
        cache.clear()
        super(PlayerResultsTest, self).setUp()
        self.utils = Utils(self.browser,self.server_url)
        self.utils.login_unassigned_user()

    def test_page_up(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)
        player = self.__get_valid_player(year=2013)

        self.__open_week_results_page(year=2013,week_number=1,player_id=player.id)
        body = self.browser.find_element_by_tag_name('body').text
        expected = "%s Week 1 Results" % (player.public_name)
        self.assertIn(expected,body)

        test_db.delete_database()

    def test_week_final(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)
        player = self.__get_valid_player(year=2013)

        self.__open_week_results_page(year=2013,week_number=1,player_id=player.id)
        summary = self.browser.find_elements_by_class_name('summary-label')
        self.assertEqual(len(summary),3)
        self.assertEqual(summary[0].text,'Wins')
        self.assertEqual(summary[1].text,'Losses')
        self.assertEqual(summary[2].text,'Win Pct')

        test_db.delete_database()

    def test_week_not_started(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,6, pick_deadline=tz.now()-timedelta(hours=1))
        player = self.__get_valid_player(year=1978)

        self.__open_week_results_page(year=1978,week_number=6,player_id=player.id)
        summary = self.browser.find_element_by_class_name('summary-content').text
        expected = 'Wins 0 Losses 0 Win Pct 0.000 Projected Wins 10 Possible Wins 10'
        self.assertEqual(expected,summary)

        # check that at no games have started (i.e. all show Favored)
        spread_labels = self.browser.find_elements_by_class_name('spread-label')
        for label in spread_labels:
            self.assertEquals(label.text,'Favored')

        test_db.delete_database()

    def test_week_in_progress(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_in_progress(1978,8)
        player = self.__get_valid_player(year=1978)

        self.__open_week_results_page(year=1978,week_number=8,player_id=player.id)
        summary = self.browser.find_elements_by_class_name('summary-label')
        self.assertEqual(len(summary),5)
        self.assertEqual(summary[0].text,'Wins')
        self.assertEqual(summary[1].text,'Losses')
        self.assertEqual(summary[2].text,'Win Pct')
        self.assertEqual(summary[3].text,'Projected Wins')
        self.assertEqual(summary[4].text,'Possible Wins')

        # check that at least one game has 'Result'
        spread_labels = self.browser.find_elements_by_class_name('spread-label')
        labels = [ label.text for label in spread_labels ]
        self.assertIn('Result',labels)

        test_db.delete_database()

    def test_week_in_progress_games_in_progress(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_in_progress_games_in_progress(1978,9)
        player = self.__get_player(year=1978,ss_name='Brent')

        self.__open_week_results_page(year=1978,week_number=9,player_id=player.id)
        summary = self.browser.find_elements_by_class_name('summary-label')
        self.assertEqual(len(summary),5)
        self.assertEqual(summary[0].text,'Wins')
        self.assertEqual(summary[1].text,'Losses')
        self.assertEqual(summary[2].text,'Win Pct')
        self.assertEqual(summary[3].text,'Projected Wins')
        self.assertEqual(summary[4].text,'Possible Wins')

        # check that at least one game has 'Ahead' and 'Behind' results
        ahead = self.browser.find_elements_by_class_name('ahead-result-content')
        behind = self.browser.find_elements_by_class_name('behind-result-content')
        self.assertGreater(len(ahead),0)
        self.assertGreater(len(behind),0)

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
        expected = "Player (id=%d) is not participating in the 2013 pool." % (player_2012.id)
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

    def test_week_no_games(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1978,1)
        test_db.setup_week_with_no_games(1978,2)

        player = self.__get_player(year=1978,ss_name='Brent')

        # make sure week 1 page is up
        self.__open_week_results_page(year=1978,week_number=1,player_id=player.id)
        self.__is_page_up('Brent Week 1 Results')

        # check for error message on week 2
        self.__open_week_results_page(year=1978,week_number=2,player_id=player.id)

        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('The week is currently being setup.',body)

        test_db.delete_database()

    def __open_week_results_page(self,year,week_number,player_id):
        address = self.server_url + reverse('player_results',args=(year,week_number,player_id))
        self.browser.get(address)

    def __get_valid_player(self,year):
        d = Database()
        players = d.load_players(year)
        return list(players.values())[0]

    def __get_player(self,year,ss_name):
        d = Database()
        players = d.load_players(year)
        for player in players.values():
            if player.ss_name == ss_name:
                return player
        raise AssertionError('Could not find %s' % (ss_name))

    def __is_page_up(self,title):
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn(title,body)

        summary = self.browser.find_elements_by_class_name('summary-label')
        self.assertEqual(len(summary),3)
        self.assertEqual(summary[0].text,'Wins')
        self.assertEqual(summary[1].text,'Losses')
        self.assertEqual(summary[2].text,'Win Pct')


