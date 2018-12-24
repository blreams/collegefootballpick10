from .base import FunctionalTest
from django.urls import reverse
from pick10.tests.unit_test_database import *
from pick10.models import *
from pick10.calculator import *
from pick10.database import *
import unittest
from django.contrib.auth.models import User
from django.test.client import Client
from .utils import *
from pick10.utils import get_timestamp
from django.conf import settings
import pytz
import django.utils.timezone as tz

class EnterPicksTest(FunctionalTest):

    def setUp(self):
        settings.DEBUG = True
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

    def test_submit_picks(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # login a user and open the picks page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)
        self.utils.enter_picks_page(year=1978,week=1,player_id=player.id)

        # check for title
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Brent Week 1 Picks',title)

        # make picks
        self.utils.click_radio_button('pick_1','team1')
        self.utils.click_radio_button('pick_2','team2')
        self.utils.click_radio_button('pick_3','team1')
        self.utils.click_radio_button('pick_4','team2')
        self.utils.click_radio_button('pick_5','team1')
        self.utils.click_radio_button('pick_6','team2')
        self.utils.click_radio_button('pick_7','team1')
        self.utils.click_radio_button('pick_8','team2')
        self.utils.click_radio_button('pick_9','team1')

        # set pick score
        self.browser.find_element_by_name("team1-score").send_keys("10")
        self.browser.find_element_by_name("team2-score").send_keys("20")

        self.utils.click_button('Submit Picks')

        # verify picks in database
        expected = [ TEAM1, TEAM2, TEAM1, TEAM2, TEAM1, TEAM2, TEAM1, TEAM2, TEAM1, TEAM2 ]
        self.__verify_picks(player,1978,1,expected,team1_score=10,team2_score=20)

        test_db.delete_database()

    def test_team_set_correctly_for_each_pick(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # login a user and open the picks page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        # verify can choose team1 for each game
        for game_number in range(1,11):

            # set 1 game to TEAM1 and the rest to TEAM2
            # this ensures game with TEAM1 only changes the pick for that game
            picks = [TEAM2] * 10
            picks[game_number-1] = TEAM1

            self.__run_test(1978,1,player,picks,auto_score=True)

        # verify can choose team2 for each game
        for game_number in range(1,11):

            # set 1 game to TEAM2 and the rest to TEAM1
            # this ensures game with TEAM2 only changes the pick for that game
            picks = [TEAM1] * 10
            picks[game_number-1] = TEAM2

            self.__run_test(1978,1,player,picks,auto_score=True)

        test_db.delete_database()

    def test_team_score(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # login a user and open the picks page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        # try different scores
        picks = [TEAM1]*10

        picks[-1] = TEAM2
        self.__run_test(1978,1,player,picks,team1_score=0,team2_score=10,auto_score=False)

        picks[-1] = TEAM1
        self.__run_test(1978,1,player,picks,team1_score=10,team2_score=0,auto_score=False)

        picks[-1] = TEAM1
        self.__run_test(1978,1,player,picks,team1_score=5,team2_score=5,auto_score=False)

        picks[-1] = TEAM1
        self.__run_test(1978,1,player,picks,team1_score=45,team2_score=12,auto_score=False)

        picks[-1] = TEAM2
        self.__run_test(1978,1,player,picks,team1_score=12,team2_score=45,auto_score=False)

        test_db.delete_database()

    def test_no_change_to_picks(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # login a user and open the picks page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        picks = [TEAM1]*10

        # verify submit time hasn't changed when inputing same data
        self.__run_test(1978,1,player,picks,auto_score=True)
        submit1_time = self.__get_pick_submit_time(1978,1,player)
        self.__run_test(1978,1,player,picks,auto_score=True)
        submit2_time = self.__get_pick_submit_time(1978,1,player)

        # verify submit time changes if make a change
        picks[-1] = TEAM2
        self.__run_test(1978,1,player,picks,auto_score=True)
        submit3_time = self.__get_pick_submit_time(1978,1,player)

        self.assertIsNotNone(submit1_time)
        self.assertIsNotNone(submit2_time)
        self.assertIsNotNone(submit3_time)
        self.assertEqual(submit1_time,submit2_time)
        self.assertNotEqual(submit1_time,submit3_time)

        test_db.delete_database()

    def test_pick_submit_time(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # login a user and open the picks page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        picks = [TEAM1]*10

        # verify submit time is close to current time
        self.__run_test(1978,1,player,picks,auto_score=True)
        submit_time = self.__get_pick_submit_time(1978,1,player)
        current_time = tz.now()

        # note that this assumes test is run in eastern time zone

        # verify times are within a minute
        self.assertIsNotNone(submit_time)
        diff = get_timestamp(current_time) - get_timestamp(submit_time) 
        self.assertGreaterEqual(diff,0)
        self.assertLess(diff,60)

        test_db.delete_database()

    def test_no_picks(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # login a user and open the picks page and submit a blank page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)
        self.utils.enter_picks_page(year=1978,week=1,player_id=player.id)

        self.utils.click_button('Submit Picks')

        # check for title
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Brent Week 1 Picks',title)

        # each pick should have an error message
        for game_number in range(1,11):
            error_text = self.browser.find_element_by_id('pick_%d_error' % (game_number)).text
            if game_number == 10:
                self.assertEqual(error_text,'ERROR!  Team score is invalid')
            else:
                self.assertEqual(error_text,'ERROR!  Please pick a team')

        test_db.delete_database()

    def test_missing_one_pick(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # login a user and open the picks page and submit a blank page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        # fill in all picks except one and verify error message
        # do this for each pick
        for game_number in range(1,11):

            # set 1 game to 0 which will prevent pick from being made
            picks = [TEAM1] * 10
            picks[game_number-1] = 0

            self.__run_test(1978,1,player,picks,verify=False,auto_score=True)

            # check for title
            title = self.browser.find_element_by_id('page-title').text
            self.assertIn('Brent Week 1 Picks',title)

            # only one pick should have an error message
            for pick_number in range(1,10):

                if game_number == pick_number:
                    error_text = self.browser.find_element_by_id('pick_%d_error' % (game_number)).text
                    self.assertEqual(error_text,'ERROR!  Please pick a team')
                else:  # error message element should be missing
                    try:
                        element = self.browser.find_element_by_id('pick_%d_error' % (pick_number))
                        self.fail('Should not have found element')
                    except:
                        pass

        test_db.delete_database()

    def test_missing_score(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # login a user and open the picks page and submit a blank page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        picks = [TEAM1] * 10

        # test both scores missing
        self.__run_test(1978,1,player,picks,team1_score=None,team2_score=None,verify=False,auto_score=False)

        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Brent Week 1 Picks',title)

        error_text = self.browser.find_element_by_id('pick_10_error').text
        self.assertEqual(error_text,'ERROR!  Team score is invalid')

        # test team1 score missing
        self.__run_test(1978,1,player,picks,team1_score=None,team2_score=10,verify=False,auto_score=False)

        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Brent Week 1 Picks',title)

        error_text = self.browser.find_element_by_id('pick_10_error').text
        self.assertEqual(error_text,'ERROR!  Team score is invalid')

        # test team2 score missing
        self.__run_test(1978,1,player,picks,team1_score=10,team2_score=None,verify=False,auto_score=False)

        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Brent Week 1 Picks',title)

        error_text = self.browser.find_element_by_id('pick_10_error').text
        self.assertEqual(error_text,'ERROR!  Team score is invalid')

        test_db.delete_database()

    def test_bad_score(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # login a user and open the picks page and submit a blank page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        picks = [TEAM1] * 10

        # test team1 score not integer
        self.__run_test(1978,1,player,picks,team1_score='AA',team2_score=10,verify=False,auto_score=False)

        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Brent Week 1 Picks',title)

        error_text = self.browser.find_element_by_id('pick_10_error').text
        self.assertEqual(error_text,'ERROR!  Team score is invalid')

        # test team2 score not integer
        self.__run_test(1978,1,player,picks,team1_score=10,team2_score='BB',verify=False,auto_score=False)

        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Brent Week 1 Picks',title)

        error_text = self.browser.find_element_by_id('pick_10_error').text
        self.assertEqual(error_text,'ERROR!  Team score is invalid')

        test_db.delete_database()

    def test_wrong_player_without_user_profile(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # login a user and open the picks page and submit a blank page
        brent = self.utils.get_player_from_public_name(1978,'Brent')
        byron = self.utils.get_player_from_public_name(1978,'Byron')
        self.utils.login_assigned_user(name='Brent',player=brent)

        # access Brent's page
        self.utils.enter_picks_page(year=1978,week=1,player_id=brent.id)
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Brent Week 1 Picks',title)

        # access Bryon's page
        self.utils.enter_picks_page(year=1978,week=1,player_id=byron.id)

        # verify error message
        elements = self.browser.find_elements_by_id('error-msg')

        expected1 = 'Player %d does not match the logged in user.' % (byron.id)
        expected2 = 'A user can only access their own enter picks page.'

        self.assertEqual(len(elements),2)
        self.assertTrue(expected1 in elements[0].text or expected1 in elements[1].text)
        self.assertTrue(expected2 in elements[0].text or expected2 in elements[1].text)

        test_db.delete_database()

    def test_wrong_player_with_user_profile(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # login a user and open the picks page and submit a blank page
        brent = self.utils.get_player_from_public_name(1978,'Brent')
        byron = self.utils.get_player_from_public_name(1978,'Byron')
        self.utils.login_assigned_user(name='Brent',player=brent)
        self.utils.create_user_with_profile(name='Byron',player=byron)

        # access Brent's page
        self.utils.enter_picks_page(year=1978,week=1,player_id=brent.id)
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Brent Week 1 Picks',title)

        # access Bryon's page
        self.utils.enter_picks_page(year=1978,week=1,player_id=byron.id)

        # verify error message
        elements = self.browser.find_elements_by_id('error-msg')

        expected1 = 'Player %d does not match the logged in user.' % (byron.id)
        expected2 = 'A user can only access their own enter picks page.'

        self.assertEqual(len(elements),2)
        self.assertTrue(expected1 in elements[0].text or expected1 in elements[1].text)
        self.assertTrue(expected2 in elements[0].text or expected2 in elements[1].text)

        test_db.delete_database()

    def test_start_with_defaults(self):
        # this test reflects the expected state of the database
        # when picks are made for the first time in a week
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_all_picks_default(1978,1)

        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        picks = [TEAM1] * 10
        self.__run_test(1978,1,player,picks,auto_score=True)

        test_db.delete_database()

    def test_cancel_button(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # login a user and open the picks page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)
        self.utils.enter_picks_page(year=1978,week=1,player_id=player.id)

        self.utils.click_button('Cancel')

        # should have redirected to week results page
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Week 1 Leaderboard',title)

        test_db.delete_database()

    def test_picks_already_made(self):
        # this test reflects the expected state of the database
        # when picks are made for the first time in a week
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,1)

        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        picks = [TEAM1,TEAM2,TEAM1,TEAM2,TEAM1,TEAM2,TEAM1,TEAM2,TEAM1,TEAM2]
        self.__run_test(1978,1,player,picks,auto_score=True)

        test_db.delete_database()

    def test_after_pick_deadline(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        self.utils.set_pick_deadline_to_expired(1978,1)

        # login a user and open the picks page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)
        self.utils.enter_picks_page(year=1978,week=1,player_id=player.id)

        body = self.browser.find_element_by_tag_name('body').text
        expected = "The pick deadline has expired. Picks can no longer be entered."
        self.assertIn(expected,body)

        test_db.delete_database()

    def test_before_pick_deadline(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        self.utils.set_pick_deadline_not_expired(1978,1)

        # login a user and open the picks page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)
        self.utils.enter_picks_page(year=1978,week=1,player_id=player.id)

        # Ensure pick pages shows up
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Brent Week 1 Picks',title)

        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Game 10',body)
        self.assertIn('spread',body)

        test_db.delete_database()

    def test_no_pick_deadline_week_not_started(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # verify week pick deadline is None
        week = get_week(1978,1) 
        #self.assertIsNone(week.pick_deadline)
        self.assertFalse(week.lock_picks)

        # login a user and open the picks page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)
        self.utils.enter_picks_page(year=1978,week=1,player_id=player.id)

        # Ensure pick pages shows up
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Brent Week 1 Picks',title)

        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Game 10',body)
        self.assertIn('spread',body)

        test_db.delete_database()

    def test_no_pick_deadline_week_in_progress(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_in_progress(1978,1)

        # verify week pick deadline is None
        week = get_week(1978,1) 
        #self.assertIsNone(week.pick_deadline)
        self.assertFalse(week.lock_picks)

        # login a user and open the picks page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)
        self.utils.enter_picks_page(year=1978,week=1,player_id=player.id)

        body = self.browser.find_element_by_tag_name('body').text
        expected = "The week is currently in progress. No picks can be made."
        self.assertIn(expected,body)

        test_db.delete_database()

    def test_no_pick_deadline_week_final(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1978,1)

        # verify week pick deadline is None
        week = get_week(1978,1) 
        #self.assertIsNone(week.pick_deadline)
        self.assertFalse(week.lock_picks)

        # login a user and open the picks page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)
        self.utils.enter_picks_page(year=1978,week=1,player_id=player.id)

        body = self.browser.find_element_by_tag_name('body').text
        expected = "The week is final. No picks can be made."
        self.assertIn(expected,body)

        test_db.delete_database()

    def test_after_deadline_week_in_progress(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_in_progress(1978,1)

        self.utils.set_pick_deadline_to_expired(1978,1)

        # login a user and open the picks page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)
        self.utils.enter_picks_page(year=1978,week=1,player_id=player.id)

        body = self.browser.find_element_by_tag_name('body').text
        expected = "The week is currently in progress. No picks can be made."
        self.assertIn(expected,body)

        test_db.delete_database()

    def test_after_deadline_week_final(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1978,1)

        self.utils.set_pick_deadline_to_expired(1978,1)

        # login a user and open the picks page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)
        self.utils.enter_picks_page(year=1978,week=1,player_id=player.id)

        body = self.browser.find_element_by_tag_name('body').text
        expected = "The week is final. No picks can be made."
        self.assertIn(expected,body)

        test_db.delete_database()

    def test_user_without_player(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        self.utils.create_user_with_profile(name='user1',password='1234',player=None)
        self.utils.login('user1','1234')
        brent = self.utils.get_player_from_public_name(1978,'Brent')

        self.utils.enter_picks_page(year=1978,week=1,player_id=brent.id)

        body = self.browser.find_element_by_tag_name('body').text
        expected = 'User user1 is not a participant in the pool.' 
        self.assertIn(expected,body)

        test_db.delete_database()

    def test_user_without_userprofile(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        self.utils.create_user(name='user1',password='1234')
        self.utils.login('user1','1234')
        brent = self.utils.get_player_from_public_name(1978,'Brent')

        self.utils.enter_picks_page(year=1978,week=1,player_id=brent.id)

        body = self.browser.find_element_by_tag_name('body').text
        expected = 'User user1 is not a participant in the pool.' 
        self.assertIn(expected,body)

        test_db.delete_database()

    def test_user_not_logged_in(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        brent = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.enter_picks_page(year=1978,week=1,player_id=brent.id)

        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Please log in',body)

        test_db.delete_database()

    def test_invalid_year(self):
        # login
        test_db = UnitTestDatabase()
        player = test_db.setup_player(1980,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        # access invalid year
        self.utils.enter_picks_page(year=1978,week=1,player_id=1)
        body = self.browser.find_element_by_tag_name('body').text
        expected = 'Cannot find 1978 week 1 in the database.'
        self.assertIn(expected,body)

        test_db.delete_database()

    def test_invalid_week(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # login
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        # access invalid week
        self.utils.enter_picks_page(year=1978,week=2,player_id=1)

        # check error message
        body = self.browser.find_element_by_tag_name('body').text
        expected = 'Cannot find 1978 week 2 in the database.'
        self.assertIn(expected,body)

        test_db.delete_database()

    def test_invalid_player(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # find an invalid player id
        # player ids usually ordered starting at 1
        # so number of players + 1 should be invalid
        # just in case, try the next 100 numbers
        players = Database().load_players(1978)
        num_players = len(players)
        player_id = -1
        for num in range(num_players+1,num_players+100):
            if num not in players:
                player_id = num
                break
        self.assertNotEqual(player_id,-1)  # did not find invalid number

        # login
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        # invalid id
        self.utils.enter_picks_page(year=1978,week=1,player_id=player_id)

        # check error message
        body = self.browser.find_element_by_tag_name('body').text
        expected = 'Cannot find player %d in the database.' % (player_id)
        self.assertIn(expected,body)

        test_db.delete_database()

    def test_player_not_in_year(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        player_other_year = test_db.setup_player(1980,'Player1')
        self.utils.login_assigned_user(name='user1',player=player_other_year)

        self.utils.enter_picks_page(year=1978,week=1,player_id=player_other_year.id)

        body = self.browser.find_element_by_tag_name('body').text
        expected = "Player Player1(id=%d) is not participating in the pool." % (player_other_year.id)
        self.assertIn(expected,body)

        test_db.delete_database()

    def test_picks_locked(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started_no_picks(1978,1)

        # login a user and open the picks page
        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)
        self.utils.lock_picks(1978,1) # Weird things happen if you lock picks before this.
        self.utils.enter_picks_page(year=1978,week=1,player_id=player.id)

        body = self.browser.find_element_by_tag_name('body').text
        expected = "The week is currently being setup."
        self.assertIn(expected,body)

        test_db.delete_database()

    def test_week_no_games(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1978,1)
        test_db.setup_week_with_no_games(1978,2)

        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        # make sure week 1 page is up
        self.utils.enter_picks_page(year=1978,week=1,player_id=player.id)
        body = self.browser.find_element_by_tag_name('body').text
        expected = 'The week is final. No picks can be made.'
        self.assertIn(expected,body)

        # check for error message on week 2
        self.utils.enter_picks_page(year=1978,week=2,player_id=player.id)

        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('The week is currently being setup.',body)

        test_db.delete_database()


    @unittest.skip('not implemented yet')
    def test_POST_invalid_year(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_picks_locked(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_after_pick_deadline(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_before_pick_deadline(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_no_pick_deadline_week_not_started(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_no_pick_deadline_week_in_progress(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_no_pick_deadline_week_final(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_after_deadline_week_in_progress(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_after_deadline_week_final(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_user_without_player(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_user_without_userprofile(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_user_not_logged_in(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_invalid_week(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_invalid_player(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_wrong_player_without_user_profile(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_wrong_player_with_user_profile(self):
        pass

    @unittest.skip('not implemented yet')
    def test_POST_player_not_in_year(self):
        pass

    def __verify_picks(self,player,year,week_number,expected_picks,team1_score,team2_score):
        week_db = get_week(year,week_number) 
        picks_db = Pick.objects.filter(game__week=week_db,player=player)

        assert len(picks_db) == 10
        assert len(expected_picks) == 10

        # verify pick for each game number in db
        picks_by_game = { pick.game.gamenum:pick for pick in picks_db }
        game_numbers = sorted(picks_by_game.keys())
        assert game_numbers == [1,2,3,4,5,6,7,8,9,10]

        # verify picks match expected
        for game_number in range(1,11):
            pick_db = picks_by_game[game_number]
            index = game_number - 1
            self.assertEqual(pick_db.winner,expected_picks[index])

        game10 = picks_by_game[10]
        self.assertEqual(game10.team1_predicted_points,team1_score)
        self.assertEqual(game10.team2_predicted_points,team2_score)

    def __run_test(self,year,week,player,picks,team1_score=None,team2_score=None,verify=True,auto_score=True):

        self.utils.enter_picks_page(year=year,week=week,player_id=player.id)

        # check for title
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('%s Week 1 Picks' % (player.private_name),title)

        # make picks
        for game_number in range(1,11):
            index = game_number - 1
            if picks[index] == TEAM1:
                value = 'team1'
            elif picks[index] == TEAM2:
                value = 'team2'
            elif picks[index] != 0:
                raise AssertionError("Invalid pick value")

            # skip the pick if it is set to 0
            if picks[index] != 0 and game_number != 10:
                name = 'pick_%d' % (game_number)
                self.utils.click_radio_button(name,value)

        if auto_score:
            game10_pick = picks[9]
            team1_score,team2_score = self.__set_game10_winner(game10_pick)

        # set pick score
        if team1_score != None:
            self.utils.set_input_text('team1-score',str(team1_score))
        if team2_score != None:
            self.utils.set_input_text('team2-score',str(team2_score))

        self.utils.click_button('Submit Picks')

        # verify picks in database
        if verify:
            self.__verify_picks(player,year,week,picks,team1_score,team2_score)

    def __get_pick_submit_time(self,year,week,player):
        database = Database()
        week_data = database.load_week_data(year,week)
        calc = CalculateResults(week_data)
        submit_time = calc.get_player_submit_time(player)
        return submit_time

    def __set_game10_winner(self,winner):
        game10 = get_game(1978,1,10)

        if winner == TEAM1:
            team2_score = 0
            team1_score = int(game10.spread) + 1
        elif winner == TEAM2:
            team1_score = 0
            team2_score = int(game10.spread) + 1
        elif winner == 0:
            team1_score = None
            team2_score = None 
        else:
            raise AssertionError("expected TEAM1 or TEAM2")

        return team1_score,team2_score

