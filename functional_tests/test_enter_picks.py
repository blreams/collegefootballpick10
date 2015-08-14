from .base import FunctionalTest
from django.core.urlresolvers import reverse
from pick10.tests.unit_test_database import *
from pick10.models import *
from pick10.calculator import *
import unittest
from django.contrib.auth.models import User
from django.test.client import Client
from utils import *

class EnterPicksTest(FunctionalTest):

    def setUp(self):
        super(EnterPicksTest, self).setUp()
        self.utils = Utils(self.browser,self.server_url)

    def test_page_up(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # login a user and open the picks page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)
        self.utils.enter_picks_page(year=1978,week=1,player_id=player.id)

        # check for title
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Brent Week 1 Picks',title)

        test_db.delete_database()

    @unittest.skip('not implemented yet')
    def test_wrong_player(self):
        pass

    @unittest.skip('not implemented yet')
    def test_pick_team1(self):
        pass

    @unittest.skip('not implemented yet')
    def test_pick_team2(self):
        pass

    @unittest.skip('not implemented yet')
    def test_pick_score(self):
        pass

    @unittest.skip('not implemented yet')
    def test_no_picks(self):
        pass

    @unittest.skip('not implemented yet')
    def test_no_score(self):
        pass

    @unittest.skip('not implemented yet')
    def test_bad_score(self):
        pass

    @unittest.skip('not implemented yet')
    def test_cancel_button(self):
        pass

    @unittest.skip('not implemented yet')
    def test_no_picks_yet(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,1)
        #self.__open_page(year=1978,week_number=1)

    @unittest.skip('not implemented yet')
    def test_picks_already_made(self):
        pass

    @unittest.skip('not implemented yet')
    def test_no_change_to_picks(self):
        pass

    @unittest.skip('not implemented yet')
    def test_after_pick_deadline(self):
        pass

    @unittest.skip('not implemented yet')
    def test_week_in_progress(self):
        pass

    @unittest.skip('not implemented yet')
    def test_week_final(self):
        pass

    @unittest.skip('not implemented yet')
    def test_GET_invalid_user(self):
        pass

    @unittest.skip('not implemented yet')
    def test_GET_user_not_logged_in(self):
        pass

    @unittest.skip('not implemented yet')
    def test_GET_invalid_year(self):
        pass

    @unittest.skip('not implemented yet')
    def test_GET_invalid_week(self):
        pass

    @unittest.skip('not implemented yet')
    def test_GET_invalid_player(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_invalid_user(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_user_not_logged_in(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_invalid_year(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_invalid_week(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_invalid_player(self):
        pass
