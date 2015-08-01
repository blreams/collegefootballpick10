from .base import FunctionalTest
from django.core.urlresolvers import reverse
from pick10.tests.unit_test_database import *
import unittest

class TiebreakTest(FunctionalTest):

    def test_page_up(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_year(2013)

        self.__open_results_page(year=2013)
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('2013 Leaderboard',title)

        test_db.delete_database()

    def __open_tiebreak_page(self,year,week):
        address = self.server_url + reverse('tiebreak',args=(year,week_number))
        self.browser.get(address)
