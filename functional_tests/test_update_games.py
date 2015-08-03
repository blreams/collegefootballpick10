from .base import FunctionalTest
from django.core.urlresolvers import reverse
from pick10.tests.unit_test_database import *
from pick10.models import *
import unittest

class UpdateGamesTest(FunctionalTest):

    @unittest.skip('debugging other function')
    def test_page_up(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)

        self.__open_page(year=2013,week_number=1)
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Week 1 Games',title)

        test_db.delete_database()

    @unittest.skip('debugging other function')
    def test_not_started_view(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,1)

        self.__open_page(year=1978,week_number=1)

        self.assertTrue(self.__page_loaded(week_number=1))
        self.assertFalse(self.__lock_button_present())

        for game_number in range(1,11):
            self.__verify_game(game_number,"not_started")

        test_db.delete_database()

    def test_edit_scores(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,1)

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
        import pdb; pdb.set_trace()

    @unittest.skip('not implemented yet')
    def test_edit_quarter_and_time(self):
        return

    @unittest.skip('debugging other function')
    def test_in_progress_view(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_in_progress_games_in_progress(1981,1)

        self.__set_game_attr(1981,1,number=7,quarter='2nd',time_left='7:30')
        self.__set_game_attr(1981,1,number=8,quarter='1st',time_left='11:20')
        self.__set_game_attr(1981,1,number=9,quarter='Half',time_left='')

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
        self.__verify_game(9,"in_progress",team1_score=25,team2_score=20,quarter='Half',time='')
        self.__verify_game(10,"not_started")

        test_db.delete_database()


    @unittest.skip('debugging other function')
    def test_all_final_view(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_final(1980,1)

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

    @unittest.skip('not implemented yet')
    def test_cancel_button(self):
        return

    @unittest.skip('not implemented yet')
    def test_games_locked(self):
        return

    def __open_page(self,year,week_number):
        address = self.server_url + reverse('update_games',args=(year,week_number,))
        self.browser.get(address)

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

