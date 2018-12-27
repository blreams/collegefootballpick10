from .base import FunctionalTest
from django.urls import reverse
from pick10.tests.unit_test_database import *
from pick10.models import *
from pick10.calculator import *
from pick10.database import *
import unittest
from .utils import *

class RaceConditionTest(FunctionalTest):

    def setUp(self):
        super(RaceConditionTest, self).setUp()
        self.utils = Utils(self.browser,self.server_url)

    def test_enter_picks_game_change(self):
        # setup data
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # login user linked to a player
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        for game_number in range(1,11):
            self.__test_enter_picks_change_spread(game_number,player)

        test_db.delete_database()

    def __test_enter_picks_change_spread(self,game_number,player):

        # get the page
        self.utils.enter_picks_page(year=1978,week=1,player_id=player.id)

        # change the spread
        game = get_game(1978,1,game_number)
        game.spread = game.spread + 5
        game.save()

        # submit the picks
        self.utils.click_button('Submit Picks')

        # verify error message
        body = self.browser.find_element_by_tag_name('body').text
        expected = "The games have changed. Please re-enter your picks"
        self.assertIn(expected,body)
