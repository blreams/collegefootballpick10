from .base import FunctionalTest
from django.core.urlresolvers import reverse
from pick10.tests.unit_test_database import *
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

    @unittest.skip('not implemented yet')
    def test_not_started_view(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,1)

        self.__open_page(year=1978,week_number=1)

        self.assertTrue(self.__page_loaded(week_number=1))
        self.assertFalse(self.__lock_button_present())

        for game_number in range(1,11):
            self.__verify_game(game_number,"not_started")

        test_db.delete_database()

    @unittest.skip('not implemented yet')
    def test_edit_scores(self):
        return

    @unittest.skip('not implemented yet')
    def test_edit_quarter_and_time(self):
        return

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

