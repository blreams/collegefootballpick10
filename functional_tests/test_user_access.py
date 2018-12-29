from .base import FunctionalTest
from django.urls import reverse
from pick10.tests.unit_test_database import UnitTestDatabase
import unittest
from django.contrib.auth.models import User
from django.test.client import Client
from .utils import Utils
from django.utils import timezone as tz
from datetime import timedelta

class UserAccessTest(FunctionalTest):

    def setUp(self):
        super(UserAccessTest, self).setUp()
        self.utils = Utils(self.browser,self.server_url)

    def test_issue_40_user_stays_logged_in(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)

        self.utils.unlock_game_scores(2013,1)

        # load and submit the update games page
        player = self.utils.get_player_from_ss_name(2013,'Holden, Brent')
        self.utils.login_assigned_user(name="Brent",password="1234",player=player)
        self.utils.update_games_page(year=2013,week_number=1)
        self.assertEqual(self.browser.title,'Week 1 Update Games')
        self.__verify_user_logged_in("Brent")
        self.utils.click_input_button('submit_form')

        # ensure update page has logged in user
        # Looks like this behaves differently in a cygwin environment.
        # I believe what happened is that the webdriver did not return
        # control until after the cache update was completed, which means
        # it went straight to the Week 1 Leaderboard page.
        if self.browser.title != 'Week 1 Leaderboard':
            self.assertEqual(self.browser.title,'Week 1 Page Update')
            self.__verify_user_logged_in("Brent")

        # wait for page to redirect to week results within 3 minutes
        # verify still logged in
        self.utils.wait_for_page('Week 1 Leaderboard',timeout=60*3)
        self.__verify_user_logged_in("Brent")

        test_db.delete_database()

    def test_no_user(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,1)

        self.__overall_results('Please log in')
        self.__week_results('Please log in')
        self.__player_results('Please log in')
        self.__tiebreak('Please log in')
        self.__update_games('Please log in')
        self.__enter_picks('Please log in')
        self.__update_pages('Please log in')

        test_db.delete_database()

    def test_public_user(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,1, pick_deadline=tz.now()-timedelta(hours=1))

        self.utils.login_unassigned_user('Brent')

        self.__overall_results()
        self.__week_results()
        self.__player_results()
        self.__tiebreak()
        self.__update_games('User Brent is not a participant in the pool')
        self.__enter_picks('User Brent is not a participant in the pool')
        self.__update_pages('Page not found')

        test_db.delete_database()

    def test_private_user(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,1)

        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        self.__overall_results()
        self.__week_results()
        self.__player_results()
        self.__tiebreak()
        self.__update_games()
        self.__enter_picks()
        self.__update_pages(alttitle='Week 1 Leaderboard')

        test_db.delete_database()

    def test_superuser(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,1, pick_deadline=tz.now()-timedelta(hours=1))

        self.utils.login_superuser(name='Brent')

        self.__overall_results()
        self.__week_results()
        self.__player_results()
        self.__tiebreak()
        self.__update_games()
        self.__enter_picks('User Brent is not a participant in the pool')
        self.__update_pages(alttitle='Week 1 Leaderboard')

        test_db.delete_database()

    def __overall_results(self,error_message=None):
        self.utils.overall_results_page(year=1978)

        body = self.browser.find_element_by_tag_name('body').text

        if error_message == None:
            self.assertIn('1978 Leaderboard',body)
        else:
            self.assertIn(error_message,body)

    def __week_results(self,error_message=None):
        self.utils.week_results_page(year=1978,week_number=1)

        body = self.browser.find_element_by_tag_name('body').text

        if error_message == None:
            self.assertIn('Week 1 Leaderboard',body)
        else:
            self.assertIn(error_message,body)

    def __player_results(self,error_message=None):
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.player_results_page(year=1978,week_number=1,player_id=player.id)

        body = self.browser.find_element_by_tag_name('body').text

        if error_message == None:
            self.assertIn('Brent Week 1 Results',body)
        else:
            self.assertIn(error_message,body)

    def __tiebreak(self,error_message=None):
        self.utils.tiebreak_page(year=1978,week=1)

        body = self.browser.find_element_by_tag_name('body').text

        if error_message == None:
            self.assertIn('Week 1 Tiebreaker',body)
        else:
            self.assertIn(error_message,body)

    def __update_games(self,error_message=None):
        self.utils.update_games_page(year=1978,week_number=1)

        body = self.browser.find_element_by_tag_name('body').text

        if error_message == None:
            self.assertIn('Week 1 Games',body)
        else:
            self.assertIn(error_message,body)

    def __enter_picks(self,error_message=None):
        player = self.utils.get_player_from_public_name(1978,'Brent')

        self.utils.enter_picks_page(year=1978,week=1,player_id=player.id)

        body = self.browser.find_element_by_tag_name('body').text

        if error_message == None:
            self.assertIn('Brent Week 1 Picks',body)
        else:
            self.assertIn(error_message,body)

    def __update_pages(self,error_message=None,alttitle=None):
        self.utils.update_page(year=1978,week=1)

        body = self.browser.find_element_by_tag_name('body').text

        if error_message == None:
            if not alttitle or self.browser.title != alttitle:
                # In cygwin environment, webdriver does not return control
                # until after redirect when update is finished.
                self.assertIn('pages are being updated',body)
        else:
            self.assertIn(error_message,body)

    def __verify_user_logged_in(self,name):
        logged_in_text = self.browser.find_element_by_id('ident_id').text
        expected = 'Logged in as: %s' % (name)
        self.assertEquals(expected,logged_in_text)
