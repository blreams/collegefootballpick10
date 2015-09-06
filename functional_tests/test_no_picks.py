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

    def test_week_results_week1_not_started(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_with_no_pick_defaulters(1978,1)
        self.__login_player('Brent',1978)

        player_with_picks = self.utils.get_player_from_public_name(1978,'Brent')
        player_no_picks = self.utils.get_player_from_public_name(1978,'John')

        import pdb; pdb.set_trace()
        self.utils.week_results_page(1978,1)
        self.utils.overall_results_page(1978)
        self.utils.player_results_page(1978,1,player_with_picks.id)
        self.utils.player_results_page(1978,1,player_no_picks.id)
        self.utils.enter_picks_page(1978,1,player_with_picks.id)
        self.utils.update_games_page(1978,1)

        test_db.delete_database()

    @unittest.skip('not yet')
    def test_week_results_week2_not_started(self):
        self.fail('not implemented yet')

    @unittest.skip('not yet')
    def test_week_results_week1_not_started_player2(self):
        # login player with no picks
        self.fail('not implemented yet')

    @unittest.skip('not yet')
    def test_week_results_week2_not_started_player2(self):
        # login player with no picks
        self.fail('not implemented yet')

    def __login_player(self,name,year):
        player = self.utils.get_player_from_public_name(year,name)
        self.utils.login_assigned_user(name=name,player=player)
