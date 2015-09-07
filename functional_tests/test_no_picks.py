from .base import FunctionalTest
from django.core.urlresolvers import reverse
from pick10.tests.unit_test_database import *
import unittest
from django.core.cache import *
from utils import *
from django.conf import settings

class NoPicksTest(FunctionalTest):

    def setUp(self):
        settings.DEBUG = True
        cache = get_cache('default')
        cache.clear()
        super(NoPicksTest, self).setUp()
        self.utils = Utils(self.browser,self.server_url)

    @unittest.skip('tested')
    def test_week_results_week1_not_started(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_with_no_pick_defaulters(1978,1)
        self.__login_player('Brent',1978)

        player_with_picks = self.utils.get_player_from_public_name(1978,'Brent')
        player_no_picks = self.utils.get_player_from_public_name(1978,'John')

        self.utils.week_results_page(1978,1)
        self.__is_page_up('Week 1 Leaderboard')

        self.utils.overall_results_page(1978)
        self.__is_page_up('1978 Leaderboard')

        self.utils.player_results_page(1978,1,player_with_picks.id)
        self.__is_page_up('Brent Week 1 Results')

        self.utils.player_results_page(1978,1,player_no_picks.id)
        self.__is_page_up('John Week 1 Results')

        self.utils.enter_picks_page(1978,1,player_with_picks.id)
        self.__is_page_up('Brent Week 1 Picks')

        self.utils.update_games_page(1978,1)
        self.__is_page_up('Week 1 Games')

        test_db.delete_database()

    @unittest.skip('tested')
    def test_week_results_week2_not_started(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1978,1)
        test_db.setup_week_not_started_with_no_pick_defaulters(1978,2)
        self.__login_player('Brent',1978)

        player_with_picks = self.utils.get_player_from_public_name(1978,'Brent')
        player_no_picks = self.utils.get_player_from_public_name(1978,'John')

        self.utils.week_results_page(1978,1)
        self.__is_page_up('Week 1 Leaderboard')

        self.utils.week_results_page(1978,2)
        self.__is_page_up('Week 2 Leaderboard')

        self.utils.overall_results_page(1978)
        self.__is_page_up('1978 Leaderboard')

        self.utils.player_results_page(1978,1,player_with_picks.id)
        self.__is_page_up('Brent Week 1 Results')

        self.utils.player_results_page(1978,2,player_with_picks.id)
        self.__is_page_up('Brent Week 2 Results')

        self.utils.player_results_page(1978,1,player_no_picks.id)
        self.__is_page_up('John Week 1 Results')

        self.utils.player_results_page(1978,2,player_no_picks.id)
        self.__is_page_up('John Week 2 Results')

        self.utils.enter_picks_page(1978,1,player_with_picks.id)
        self.__is_page_up('The week is final')

        self.utils.enter_picks_page(1978,2,player_with_picks.id)
        self.__is_page_up('Brent Week 2 Picks')

        self.utils.update_games_page(1978,1)
        self.__is_page_up('Week 1 Games')

        self.utils.update_games_page(1978,2)
        self.__is_page_up('Week 2 Games')

        test_db.delete_database()

    @unittest.skip('tested')
    def test_week_results_week1_not_started_player2(self):
        # login player with no picks
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_with_no_pick_defaulters(1978,1)
        self.__login_player('John',1978)

        player_with_picks = self.utils.get_player_from_public_name(1978,'Brent')
        player_no_picks = self.utils.get_player_from_public_name(1978,'John')

        self.utils.week_results_page(1978,1)
        self.__is_page_up('Week 1 Leaderboard')

        self.utils.overall_results_page(1978)
        self.__is_page_up('1978 Leaderboard')

        self.utils.player_results_page(1978,1,player_with_picks.id)
        self.__is_page_up('Brent Week 1 Results')

        self.utils.player_results_page(1978,1,player_no_picks.id)
        self.__is_page_up('John Week 1 Results')

        self.utils.enter_picks_page(1978,1,player_no_picks.id)
        self.__is_page_up('John Week 1 Picks')

        self.utils.update_games_page(1978,1)
        self.__is_page_up('Week 1 Games')

        test_db.delete_database()


    def test_week_results_week2_not_started_player2(self):
        # login player with no picks
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1978,1)
        test_db.setup_week_not_started_with_no_pick_defaulters(1978,2)
        self.__login_player('John',1978)

        player_with_picks = self.utils.get_player_from_public_name(1978,'Brent')
        player_no_picks = self.utils.get_player_from_public_name(1978,'John')

        self.utils.week_results_page(1978,1)
        self.__is_page_up('Week 1 Leaderboard')

        self.utils.week_results_page(1978,2)
        self.__is_page_up('Week 2 Leaderboard')

        self.utils.overall_results_page(1978)
        self.__is_page_up('1978 Leaderboard')

        self.utils.player_results_page(1978,1,player_with_picks.id)
        self.__is_page_up('Brent Week 1 Results')

        self.utils.player_results_page(1978,2,player_with_picks.id)
        self.__is_page_up('Brent Week 2 Results')

        self.utils.player_results_page(1978,1,player_no_picks.id)
        self.__is_page_up('John Week 1 Results')

        self.utils.player_results_page(1978,2,player_no_picks.id)
        self.__is_page_up('John Week 2 Results')

        self.utils.enter_picks_page(1978,1,player_no_picks.id)
        self.__is_page_up('The week is final')

        self.utils.enter_picks_page(1978,2,player_no_picks.id)
        self.__is_page_up('John Week 2 Picks')

        self.utils.update_games_page(1978,1)
        self.__is_page_up('Week 1 Games')

        self.utils.update_games_page(1978,2)
        self.__is_page_up('Week 2 Games')

        test_db.delete_database()

    def __login_player(self,name,year):
        player = self.utils.get_player_from_public_name(year,name)
        self.utils.login_assigned_user(name=name,player=player)

    def __is_page_up(self,text):
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn(text,body)
