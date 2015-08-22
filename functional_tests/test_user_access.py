from .base import FunctionalTest
from django.core.urlresolvers import reverse
from pick10.tests.unit_test_database import *
from pick10.models import *
from pick10.calculator import *
import unittest
from django.contrib.auth.models import User
from django.test.client import Client
from utils import *

class UserAccessTest(FunctionalTest):

    def setUp(self):
        super(UserAccessTest, self).setUp()
        self.utils = Utils(self.browser,self.server_url)

    def test_issue_40_user_stays_logged_in(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)

        # load and submit the update games page
        player = self.utils.get_player_from_ss_name(2013,'Holden, Brent')
        self.utils.login_assigned_user(name="Brent",password="1234",player=player)
        self.utils.update_games_page(year=2013,week_number=1)
        self.assertEqual(self.browser.title,'Week 1 Update Games')
        self.__verify_user_logged_in("Brent")
        self.utils.click_input_button('submit_form')

        # ensure update page has logged in user
        self.assertEqual(self.browser.title,'Week 1 Page Update')
        self.__verify_user_logged_in("Brent")

        # wait for page to redirect to week results within 3 minutes
        # verify still logged in
        self.utils.wait_for_page('Week 1 Leaderboard',timeout=60*3)
        self.__verify_user_logged_in("Brent")

        test_db.delete_database()

    def __verify_user_logged_in(self,name):
        logged_in_text = self.browser.find_element_by_id('ident_id').text
        expected = 'Logged in as: %s' % (name)
        self.assertEquals(expected,logged_in_text)

    # TODO
    # login regular user, test name shows up on expected pages
    # login user + player, test access to pages
    # login superuser, test access to pages
    # superuser separate login?  or link to player?
