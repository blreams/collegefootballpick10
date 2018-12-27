from .base import FunctionalTest
from django.urls import reverse
from pick10.tests.unit_test_database import *
from pick10.models import *
from pick10.calculator import *
import unittest
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.cache import cache
from .utils import *

class UpdateGamesTest(FunctionalTest):

    def setUp(self):
        cache.clear()
        super(UpdateGamesTest, self).setUp()
        self.utils = Utils(self.browser,self.server_url)

    def test_page_up(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)

        player = self.utils.get_player_from_ss_name(2013,'Holden, Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        self.__open_page(year=2013,week_number=1)
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Week 1 Games',title)

        test_db.delete_database()

    def test_not_started_view(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,1)

        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        self.__open_page(year=1978,week_number=1)

        self.assertTrue(self.__page_loaded(week_number=1))
        self.assertFalse(self.__lock_button_present())

        for game_number in range(1,11):
            self.__verify_game(game_number,"not_started")

        test_db.delete_database()

    def test_edit_scores(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,1)

        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        self.__open_page(year=1978,week_number=1)

        self.assertTrue(self.__page_loaded(week_number=1))
        self.assertFalse(self.__lock_button_present())

        self.__set_game_score(1,team1_score=11,team2_score=12)
        self.__set_game_score(2,team1_score=21,team2_score=22)
        self.__set_game_score(3,team1_score=31,team2_score=32)
        self.__set_game_score(4,team1_score=41,team2_score=42)
        self.__set_game_score(5,team1_score=51,team2_score=52)
        self.__set_game_score(6,team1_score=61,team2_score=62)
        self.__set_game_score(7,team1_score=71,team2_score=72)
        self.__set_game_score(8,team1_score=81,team2_score=82)
        self.__set_game_score(9,team1_score=91,team2_score=92)
        self.__set_game_score(10,team1_score=0,team2_score=2)

        self.__click_button('submit')

        self.__verify_game_in_database(1978,1,1,IN_PROGRESS,11,12,'','')
        self.__verify_game_in_database(1978,1,2,IN_PROGRESS,21,22,'','')
        self.__verify_game_in_database(1978,1,3,IN_PROGRESS,31,32,'','')
        self.__verify_game_in_database(1978,1,4,IN_PROGRESS,41,42,'','')
        self.__verify_game_in_database(1978,1,5,IN_PROGRESS,51,52,'','')
        self.__verify_game_in_database(1978,1,6,IN_PROGRESS,61,62,'','')
        self.__verify_game_in_database(1978,1,7,IN_PROGRESS,71,72,'','')
        self.__verify_game_in_database(1978,1,8,IN_PROGRESS,81,82,'','')
        self.__verify_game_in_database(1978,1,9,IN_PROGRESS,91,92,'','')
        self.__verify_game_in_database(1978,1,10,IN_PROGRESS,0,2,'','')

        test_db.delete_database()

    def test_edit_quarter_and_time(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,1)

        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        self.__open_page(year=1978,week_number=1)

        self.assertTrue(self.__page_loaded(week_number=1))
        self.assertFalse(self.__lock_button_present())

        self.__set_game_score(1,team1_score=11,team2_score=12)
        self.__set_game_score(2,team1_score=21,team2_score=22)
        self.__set_game_score(3,team1_score=31,team2_score=32)
        self.__set_game_score(4,team1_score=41,team2_score=42)
        self.__set_game_score(5,team1_score=51,team2_score=52)
        self.__set_game_score(6,team1_score=61,team2_score=62)
        self.__set_game_score(7,team1_score=71,team2_score=72)
        self.__set_game_score(8,team1_score=81,team2_score=82)
        self.__set_game_score(9,team1_score=91,team2_score=92)
        self.__set_game_score(10,team1_score=0,team2_score=2)

        self.__set_game_quarter_time(1,quarter='1st',time='15:00')
        self.__set_game_quarter_time(2,quarter='2nd',time='8:57')
        self.__set_game_quarter_time(3,quarter='Hal',time='')
        self.__set_game_quarter_time(4,quarter='3rd',time='1:30')
        self.__set_game_quarter_time(5,quarter='4th',time='0:10')
        self.__set_game_quarter_time(6,quarter='OT',time='')
        self.__set_game_quarter_time(7,quarter='2OT',time='')
        self.__set_game_quarter_time(8,quarter='',time='')
        self.__set_game_quarter_time(9,quarter='',time='')
        self.__set_game_quarter_time(10,quarter='',time='')

        self.__click_button('submit')

        self.__verify_game_in_database(1978,1,1,IN_PROGRESS,11,12,'1st','15:00')
        self.__verify_game_in_database(1978,1,2,IN_PROGRESS,21,22,'2nd','8:57')
        self.__verify_game_in_database(1978,1,3,IN_PROGRESS,31,32,'Hal','')
        self.__verify_game_in_database(1978,1,4,IN_PROGRESS,41,42,'3rd','1:30')
        self.__verify_game_in_database(1978,1,5,IN_PROGRESS,51,52,'4th','0:10')
        self.__verify_game_in_database(1978,1,6,IN_PROGRESS,61,62,'OT','')
        self.__verify_game_in_database(1978,1,7,IN_PROGRESS,71,72,'2OT','')
        self.__verify_game_in_database(1978,1,8,IN_PROGRESS,81,82,'','')
        self.__verify_game_in_database(1978,1,9,IN_PROGRESS,91,92,'','')
        self.__verify_game_in_database(1978,1,10,IN_PROGRESS,0,2,'','')

        test_db.delete_database()

    def test_in_progress_view(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_in_progress_games_in_progress(1981,1)

        self.__set_game_attr(1981,1,number=7,quarter='2nd',time_left='7:30')
        self.__set_game_attr(1981,1,number=8,quarter='1st',time_left='11:20')
        self.__set_game_attr(1981,1,number=9,quarter='Hal',time_left='')

        player = self.utils.get_player_from_public_name(1981,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        self.__open_page(year=1981,week_number=1)

        self.assertTrue(self.__page_loaded(week_number=1))
        self.assertFalse(self.__lock_button_present())

        self.__verify_game(1,"final",team1_score=25,team2_score=20)
        self.__verify_game(2,"final",team1_score=25,team2_score=20)
        self.__verify_game(3,"final",team1_score=25,team2_score=20)
        self.__verify_game(4,"final",team1_score=15,team2_score=30)
        self.__verify_game(5,"final",team1_score=15,team2_score=30)
        self.__verify_game(6,"final",team1_score=15,team2_score=30)
        self.__verify_game(7,"in_progress",team1_score=25,team2_score=20,quarter='2nd',time='7:30')
        self.__verify_game(8,"in_progress",team1_score=15,team2_score=30,quarter='1st',time='11:20')
        self.__verify_game(9,"in_progress",team1_score=25,team2_score=20,quarter='Hal',time='')
        self.__verify_game(10,"not_started")

        test_db.delete_database()


    def test_all_final_view(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1980,1)

        player = self.utils.get_player_from_public_name(1980,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        self.__open_page(year=1980,week_number=1)

        self.assertTrue(self.__page_loaded(week_number=1))
        self.assertFalse(self.__lock_button_present())

        self.__verify_game(1,"final",team1_score=25,team2_score=20)
        self.__verify_game(2,"final",team1_score=15,team2_score=30)
        self.__verify_game(3,"final",team1_score=25,team2_score=20)
        self.__verify_game(4,"final",team1_score=15,team2_score=30)
        self.__verify_game(5,"final",team1_score=25,team2_score=20)
        self.__verify_game(6,"final",team1_score=15,team2_score=30)
        self.__verify_game(7,"final",team1_score=25,team2_score=20)
        self.__verify_game(8,"final",team1_score=15,team2_score=30)
        self.__verify_game(9,"final",team1_score=25,team2_score=20)
        self.__verify_game(10,"final",team1_score=15,team2_score=30)

        test_db.delete_database()

    def test_cancel_button(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,1)

        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        self.__open_page(year=1978,week_number=1)

        self.assertTrue(self.__page_loaded(week_number=1))
        self.assertFalse(self.__lock_button_present())

        self.__set_game_score(1,team1_score=11,team2_score=12)
        self.__set_game_score(2,team1_score=21,team2_score=22)
        self.__set_game_score(3,team1_score=31,team2_score=32)
        self.__set_game_score(4,team1_score=41,team2_score=42)
        self.__set_game_score(5,team1_score=51,team2_score=52)
        self.__set_game_score(6,team1_score=61,team2_score=62)
        self.__set_game_score(7,team1_score=71,team2_score=72)
        self.__set_game_score(8,team1_score=81,team2_score=82)
        self.__set_game_score(9,team1_score=91,team2_score=92)
        self.__set_game_score(10,team1_score=0,team2_score=2)

        self.__set_game_quarter_time(1,quarter='1st',time='15:00')
        self.__set_game_quarter_time(2,quarter='2nd',time='8:57')
        self.__set_game_quarter_time(3,quarter='Half',time='')
        self.__set_game_quarter_time(4,quarter='3rd',time='1:30')
        self.__set_game_quarter_time(5,quarter='4th',time='0:10')
        self.__set_game_quarter_time(6,quarter='OT',time='')
        self.__set_game_quarter_time(7,quarter='2OT',time='')
        self.__set_game_quarter_time(8,quarter='',time='')
        self.__set_game_quarter_time(9,quarter='',time='')
        self.__set_game_quarter_time(10,quarter='',time='')

        self.__click_button('cancel')

        self.__verify_game_in_database(1978,1,1,NOT_STARTED,-1,-1,'','')
        self.__verify_game_in_database(1978,1,2,NOT_STARTED,-1,-1,'','')
        self.__verify_game_in_database(1978,1,3,NOT_STARTED,-1,-1,'','')
        self.__verify_game_in_database(1978,1,4,NOT_STARTED,-1,-1,'','')
        self.__verify_game_in_database(1978,1,5,NOT_STARTED,-1,-1,'','')
        self.__verify_game_in_database(1978,1,6,NOT_STARTED,-1,-1,'','')
        self.__verify_game_in_database(1978,1,7,NOT_STARTED,-1,-1,'','')
        self.__verify_game_in_database(1978,1,8,NOT_STARTED,-1,-1,'','')
        self.__verify_game_in_database(1978,1,9,NOT_STARTED,-1,-1,'','')
        self.__verify_game_in_database(1978,1,10,NOT_STARTED,-1,-1,'','')

        test_db.delete_database()

    def test_games_locked(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1980,1)

        w = get_week(1980,1)
        w.lock_scores = True
        w.save()

        player = self.utils.get_player_from_public_name(1980,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        self.__open_page(year=1980,week_number=1)

        self.assertTrue(self.__page_loaded(week_number=1))
        self.assertFalse(self.__lock_button_present())
        self.assertFalse(self.__submit_button_present())

        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('The scores are locked and cannot be edited.',body)

        self.__click_button('cancel')

        test_db.delete_database()

    def test_lock_button_not_admin(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1980,1)

        w = get_week(1980,1)
        w.lock_scores = False
        w.save()

        player = self.utils.get_player_from_public_name(1980,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        self.__open_page(year=1980,week_number=1)

        self.assertTrue(self.__page_loaded(week_number=1))
        self.assertFalse(self.__lock_button_present())
        self.assertTrue(self.__submit_button_present())
        self.assertFalse(self.__unlock_button_present())

        self.__click_button('cancel')

        w = get_week(1980,1)
        self.assertFalse(w.lock_scores)

        test_db.delete_database()

    def test_lock_button_admin(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1980,1)

        w = get_week(1980,1)
        w.lock_scores = False
        w.save()

        self.__login_superuser()
        self.__open_page(year=1980,week_number=1)

        self.assertTrue(self.__page_loaded(week_number=1))
        self.assertTrue(self.__lock_button_present())
        self.assertTrue(self.__submit_button_present())
        self.assertFalse(self.__unlock_button_present())

        self.__click_button('lock')

        w = get_week(1980,1)
        self.assertTrue(w.lock_scores)

        test_db.delete_database()

    def test_unlock_button_not_admin(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1980,1)

        w = get_week(1980,1)
        w.lock_scores = True
        w.save()

        player = self.utils.get_player_from_public_name(1980,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        self.__open_page(year=1980,week_number=1)

        self.assertTrue(self.__page_loaded(week_number=1))
        self.assertFalse(self.__lock_button_present())
        self.assertFalse(self.__submit_button_present())
        self.assertFalse(self.__unlock_button_present())

        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('The scores are locked and cannot be edited.',body)

        self.__click_button('cancel')

        w = get_week(1980,1)
        self.assertTrue(w.lock_scores)

        test_db.delete_database()

    def test_unlock_button_admin(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1980,1)

        w = get_week(1980,1)
        w.lock_scores = True
        w.save()

        self.__login_superuser()
        self.__open_page(year=1980,week_number=1)

        self.assertTrue(self.__page_loaded(week_number=1))
        self.assertFalse(self.__lock_button_present())
        self.assertFalse(self.__submit_button_present())
        self.assertTrue(self.__unlock_button_present())

        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('The scores are locked and cannot be edited.',body)

        self.__click_button('unlock')

        w = get_week(1980,1)
        self.assertFalse(w.lock_scores)

        test_db.delete_database()

    def test_week_no_games(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1978,1)
        test_db.setup_week_with_no_games(1978,2)

        player = self.utils.get_player_from_public_name(1978,'Brent')
        self.utils.login_assigned_user(name='Brent',player=player)

        self.__open_page(year=1978,week_number=1)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertTrue(self.__page_loaded(week_number=1))
        self.assertIn('Teams',body)

        self.__open_page(year=1978,week_number=2)

        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('The week is currently being setup.',body)

        test_db.delete_database()

    # TODO:  test a blank form
    def test_blank_form_submit(self):
        pass

    def __open_page(self,year,week_number):
        address = self.server_url + reverse('update_games',args=(year,week_number,))
        self.browser.get(address)

    def __login_user(self):
        user = User.objects.create_user('user1','myemail@test.com','1234')
        self.__login(user.username,'1234')

    def __login_superuser(self):
        # create user
        user = User.objects.create_superuser('myuser','myemail@test.com','1234')
        self.__login(user.username,'1234')

    def __login(self,name,password):

        # go to login page
        address = self.server_url + reverse('auth_login')
        self.browser.get(address)

        # fill in user/password
        self.browser.find_element_by_id('id_username').send_keys(name)
        self.browser.find_element_by_id('id_password').send_keys(password)

        # click sign in button
        buttons = self.browser.find_elements_by_tag_name('button')
        for button in buttons:
            if button.text == 'Sign in':
                button.click()
                break

    def __get_input_value(self,tag,game_number):
        name = "%s_%d" % (tag,game_number)
        value = self.browser.find_element_by_name(name).get_attribute('value')
        return value

    def __set_input_value(self,tag,game_number,value):
        name = "%s_%d" % (tag,game_number)
        self.browser.find_element_by_name(name).send_keys(value)

    def __click_button(self,button):
        name = '%s_form' % (button)
        self.browser.find_element_by_name(name).click()

    def __is_checked(self,tag,game_number):
        name = "%s_%d" % (tag,game_number)
        checked = self.browser.find_element_by_name(name).get_attribute('checked')
        return checked != None

    def __lock_button_present(self):
        try:
            lock_button = self.browser.find_element_by_name('lock_form')
        except:
            return False
        return True

    def __unlock_button_present(self):
        try:
            unlock_button = self.browser.find_element_by_name('unlock_form')
        except:
            return False
        return True

    def __submit_button_present(self):
        try:
            submit_button = self.browser.find_element_by_name('submit_form')
        except:
            return False
        return True

    def __set_game_attr(self,year,week,number,quarter=None,time_left=None):
        g = get_game(year,week,number)

        if quarter != None:
            g.quarter = quarter
        if time_left != None:
            g.time_left = time_left

        g.save()

    def __set_game_score(self,game_number,team1_score,team2_score):
        self.__set_input_value('team1_score',game_number,str(team1_score))
        self.__set_input_value('team2_score',game_number,str(team2_score))

    def __set_game_quarter_time(self,game_number,quarter,time):
        self.__set_input_value('quarter',game_number,str(quarter))
        self.__set_input_value('time',game_number,str(time))

    def __page_loaded(self,week_number):
        title = self.browser.find_element_by_id('page-title').text
        expected = 'Week %d Games' % (week_number)
        return expected == title

    def __verify_game(self,game_number,state,team1_score=None,team2_score=None,quarter=None,time=None):

        team1_score_input = self.__get_input_value('team1_score',game_number)
        team2_score_input = self.__get_input_value('team2_score',game_number)
        time_input = self.__get_input_value('time',game_number)
        quarter_input = self.__get_input_value('quarter',game_number)
        final = self.__is_checked('final',game_number)

        if state == "not_started":
            self.assertEqual(team1_score_input,'')
            self.assertEqual(team2_score_input,'')
            self.assertEqual(quarter_input,'')
            self.assertEqual(time_input,'')
            self.assertEqual(final,False)
        elif state == "in_progress":
            self.assertEqual(int(team1_score_input),team1_score)
            self.assertEqual(int(team2_score_input),team2_score)
            self.assertEqual(final,False)

            if quarter != None:
                self.assertEqual(quarter_input,quarter)
            if time != None:
                self.assertEqual(time_input,time)
        elif state == "final":
            self.assertEqual(int(team1_score_input),team1_score)
            self.assertEqual(int(team2_score_input),team2_score)
            self.assertEqual(quarter_input,'')
            self.assertEqual(time_input,'')
            self.assertEqual(final,True)
        else:
            self.fail('Unexpected state value %s' % (state))

    def __verify_game_in_database(self,year,week,game_number,state,team1_score=None,team2_score=None,quarter=None,time=None):
        g = get_game(year,week,game_number)
        self.assertEqual(state,g.game_state)

        if team1_score != None:
            self.assertEqual(team1_score,g.team1_actual_points)
        if team2_score != None:
            self.assertEqual(team2_score,g.team2_actual_points)
        if quarter != None:
            self.assertEqual(quarter,g.quarter)
        if time != None:
            self.assertEqual(time,g.time_left)


