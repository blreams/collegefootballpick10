from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

import unittest
from bs4 import BeautifulSoup
from collections import Counter
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import Client
from .base import FunctionalTest
from .tests.unit_test_database import UnitTestDatabase
from .database import Database
from .calculate_week_results import CalculateWeekResults
from .calculator import NOT_STARTED, IN_PROGRESS, FINAL
from .utils import Utils

class TestHtmlAnalysis(FunctionalTest):

    def setUp(self):
        super(TestHtmlAnalysis, self).setUp()
        print("Initializing Test Fixture...")
        self.test_db = UnitTestDatabase()
        self.test_db.load_historical_data_for_week(2013, 1)
        self.test_db.load_historical_data_for_week(2013, 2)
        self.utils = Utils(self.browser,self.server_url)
        self.utils.unlock_game_scores(2013, 1)
        self.utils.unlock_game_scores(2013, 2)

        # load and submit the update games page
        self.player = self.utils.get_player_from_ss_name(2013, 'Reams, Byron L')
        self.utils.login_assigned_user(name='Byron', password='1234', player=self.player)
        self.utils.update_games_page(year=2013, week_number=1)
        self.assertEqual(self.browser.title, 'Week 1 Update Games')
        self.__verify_user_logged_in("Byron")
        self.utils.click_input_button('submit_form')
        # ensure update page has logged in user
        # Looks like this behaves differently in a cygwin environment.
        # I believe what happened is that the webdriver did not return
        # control until after the cache update was completed, which means
        # it went straight to the Week 1 Leaderboard page.
        if self.browser.title != 'Week 1 Leaderboard':
            self.assertEqual(self.browser.title,'Week 1 Page Update')
            self.__verify_user_logged_in("Byron")

        # wait for page to redirect to week results within 3 minutes
        # verify still logged in
        self.utils.wait_for_page('Week 1 Leaderboard',timeout=60*3)
        self.__verify_user_logged_in("Byron")

        self.utils.landing_page()

    def test_check_overall_results_weeknotstarted_page(self):
        self.test_db.setup_week_not_started(2013, 3)
        self.utils.set_pick_deadline_to_expired(2013, 3)
        self.utils.overall_results_page(2013)
        db = Database()
        self.assertEqual(db.get_pool_state(2013), 'week_not_started')
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        tags = soup.find_all(id='weeknotstarted-pool-state')
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0].text, 'week 3 pick entry deadline has passed, no games have started')
        all_ids_counter = Counter([elem.get('id') for elem in soup.find_all(id=True)])
        duplicate_ids = [id for id in all_ids_counter if all_ids_counter[id] > 1]
        self.longMessage = True
        self.assertEqual(duplicate_ids, [], 'The following id attributes are duplicate: \n%s' % '\n'.join(['%s: %d' % (id, all_ids_counter[id]) for id in duplicate_ids]))
        self.test_db.delete_database()

    def test_check_overall_results_enterpicks_page(self):
        self.test_db.setup_week_not_started(2013, 3)
        self.utils.set_pick_deadline_not_expired(2013, 3)
        self.utils.unlock_picks(2013, 3)
        self.utils.overall_results_page(2013)
        db = Database()
        self.assertEqual(db.get_pool_state(2013), 'enter_picks')
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        tags = soup.find_all(id='enterpicks-pool-state')
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0].text, 'currently entering picks for week 3')
        all_ids_counter = Counter([elem.get('id') for elem in soup.find_all(id=True)])
        duplicate_ids = [id for id in all_ids_counter if all_ids_counter[id] > 1]
        self.longMessage = True
        self.assertEqual(duplicate_ids, [], 'The following id attributes are duplicate: \n%s' % '\n'.join(['%s: %d' % (id, all_ids_counter[id]) for id in duplicate_ids]))
        self.test_db.delete_database()

    def test_check_overall_results_weekinprogress_page(self):
        self.test_db.setup_week_in_progress(2013, 3)
        self.utils.set_pick_deadline_to_expired(2013, 3)
        self.utils.overall_results_page(2013)
        db = Database()
        self.assertEqual(db.get_pool_state(2013), 'week_in_progress')
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        tags = soup.find_all(id='weekinprogress-pool-state')
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0].text, 'week 3 in progress')
        all_ids_counter = Counter([elem.get('id') for elem in soup.find_all(id=True)])
        duplicate_ids = [id for id in all_ids_counter if all_ids_counter[id] > 1]
        self.longMessage = True
        self.assertEqual(duplicate_ids, [], 'The following id attributes are duplicate: \n%s' % '\n'.join(['%s: %d' % (id, all_ids_counter[id]) for id in duplicate_ids]))
        self.test_db.delete_database()

    def test_check_overall_results_weekfinal_page(self):
        self.utils.overall_results_page(2013)
        db = Database()
        self.assertEqual(db.get_pool_state(2013), 'week_final')
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        tags = soup.find_all(id='weekfinal-pool-state')
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0].text, 'week 2 final')
        all_ids_counter = Counter([elem.get('id') for elem in soup.find_all(id=True)])
        duplicate_ids = [id for id in all_ids_counter if all_ids_counter[id] > 1]
        self.longMessage = True
        self.assertEqual(duplicate_ids, [], 'The following id attributes are duplicate: \n%s' % '\n'.join(['%s: %d' % (id, all_ids_counter[id]) for id in duplicate_ids]))
        self.test_db.delete_database()

    def test_check_overall_results_final_page(self):
        self.test_db.setup_week_final(2013, 13)
        self.utils.overall_results_page(2013)
        db = Database()
        self.assertEqual(db.get_pool_state(2013), 'end_of_year')
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        tags = soup.find_all(id='final-pool-state')
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0].text, 'final results')
        all_ids_counter = Counter([elem.get('id') for elem in soup.find_all(id=True)])
        duplicate_ids = [id for id in all_ids_counter if all_ids_counter[id] > 1]
        self.longMessage = True
        self.assertEqual(duplicate_ids, [], 'The following id attributes are duplicate: \n%s' % '\n'.join(['%s: %d' % (id, all_ids_counter[id]) for id in duplicate_ids]))
        self.test_db.delete_database()

    def test_check_week_results_weeknotstarted_page(self):
        self.test_db.setup_week_not_started(2013, 3)
        self.utils.set_pick_deadline_to_expired(2013, 3)
        self.utils.week_results_page(2013, 3)
        cwr = CalculateWeekResults(2013, 3, True)
        self.assertEqual(cwr.get_week_state(), NOT_STARTED)
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        all_ids_counter = Counter([elem.get('id') for elem in soup.find_all(id=True)])
        duplicate_ids = [id for id in all_ids_counter if all_ids_counter[id] > 1]
        self.longMessage = True
        self.assertEqual(duplicate_ids, [], 'The following id attributes are duplicate: \n%s' % '\n'.join(['%s: %d' % (id, all_ids_counter[id]) for id in duplicate_ids]))
        self.test_db.delete_database()

    def test_check_week_results_weekinprogress_page(self):
        self.test_db.setup_week_in_progress(2013, 3)
        self.utils.set_pick_deadline_to_expired(2013, 3)
        self.utils.week_results_page(2013, 3)
        cwr = CalculateWeekResults(2013, 3, True)
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        self.assertEqual(cwr.get_week_state(), IN_PROGRESS)
        all_ids_counter = Counter([elem.get('id') for elem in soup.find_all(id=True)])
        duplicate_ids = [id for id in all_ids_counter if all_ids_counter[id] > 1]
        self.longMessage = True
        self.assertEqual(duplicate_ids, [], 'The following id attributes are duplicate: \n%s' % '\n'.join(['%s: %d' % (id, all_ids_counter[id]) for id in duplicate_ids]))
        self.test_db.delete_database()

    def test_check_week_results_weekfinal_page(self):
        self.utils.week_results_page(2013, 2)
        cwr = CalculateWeekResults(2013, 2, True)
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        self.assertEqual(cwr.get_week_state(), FINAL)
        all_ids_counter = Counter([elem.get('id') for elem in soup.find_all(id=True)])
        duplicate_ids = [id for id in all_ids_counter if all_ids_counter[id] > 1]
        self.longMessage = True
        self.assertEqual(duplicate_ids, [], 'The following id attributes are duplicate: \n%s' % '\n'.join(['%s: %d' % (id, all_ids_counter[id]) for id in duplicate_ids]))
        self.test_db.delete_database()

    def test_check_player_results_page(self):
        self.utils.player_results_page(2013, 2, self.player.id)
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        all_ids_counter = Counter([elem.get('id') for elem in soup.find_all(id=True)])
        duplicate_ids = [id for id in all_ids_counter if all_ids_counter[id] > 1]
        self.longMessage = True
        self.assertEqual(duplicate_ids, [], 'The following id attributes are duplicate: \n%s' % '\n'.join(['%s: %d' % (id, all_ids_counter[id]) for id in duplicate_ids]))
        self.test_db.delete_database()

    def __verify_user_logged_in(self,name):
        logged_in_text = self.browser.find_element_by_id('ident_id').text
        expected = 'Logged in as: %s' % (name)
        self.assertEquals(expected,logged_in_text)

