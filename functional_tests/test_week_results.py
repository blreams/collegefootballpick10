from .base import FunctionalTest
from django.core.urlresolvers import reverse
from pick10.tests.unit_test_database import *

class WeekResultsTest(FunctionalTest):

    # Could not get loading the database 1 time per
    # test run of the class to work, so doing it within
    # each test for now
    #@classmethod
    #def setUpClass(cls):
        #super(WeekResultsTest, cls).setUpClass()
        #test_db = UnitTestDatabase()
        #test_db.load_historical_data_for_week(2013,1)

    #@classmethod
    #def tearDownClass(cls):
        #test_db = UnitTestDatabase()
        #test_db.delete_database()
        #super(WeekResultsTest, cls).tearDownClass()

    def test_page_up(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)

        self.__open_week_results_page(year=2013,week_number=1)
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Week 1 Leaderboard',title)

        test_db.delete_database()

    def test_duplicate(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)

        self.__open_week_results_page(year=2013,week_number=1)
        title = self.browser.find_element_by_id('page-title').text
        self.assertIn('Week 1 Leaderboard',title)

        test_db.delete_database()

    def test_invalid_year(self):
        self.__open_week_results_page(year=1980,week_number=1)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Cannot find 1980 week 1 in the database.',body)

    def test_invalid_week(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)

        self.__open_week_results_page(year=2013,week_number=15)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Cannot find 2013 week 15 in the database.',body)

        test_db.delete_database()

    def __open_week_results_page(self,year,week_number):
        address = self.server_url + reverse('week_results',args=(year,week_number))
        self.browser.get(address)
