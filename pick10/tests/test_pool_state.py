from django.test import TestCase
from pick10.database import Database
from pick10.models import *
from unit_test_database import *
import unittest
import datetime as dt
import pytz

class PoolStateTest(TestCase):

    @classmethod
    def setUpClass(cls):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_year(2013)
        test_db.setup_pool_not_started(1975)
        test_db.setup_week_not_started(1978,1)
        test_db.setup_week_in_progress(1979,1)
        test_db.setup_simple_week(1980,1)   # final week

        # data for the enter_picks tests, make deadline 1 day after current time
        test_db.setup_week_not_started(1981,1)
        week = get_week(1981,1)
        naive_dt_now = dt.datetime.now()
        naive_dt_deadline = dt.datetime(naive_dt_now.year, naive_dt_now.month, naive_dt_now.day, 16, 0, 0) + timedelta(days=1)
        deadline = pytz.timezone('US/Eastern').localize(naive_dt_deadline)
        week.pick_deadline = deadline
        week.lock_picks = False
        week.save()

        # setup week with locked_picks and before deadline
        test_db.setup_week_final(1982,1)
        test_db.setup_week_not_started(1982,2)
        week = get_week(1982,2)
        naive_dt_now = dt.datetime.now()
        naive_dt_deadline = dt.datetime(naive_dt_now.year, naive_dt_now.month, naive_dt_now.day, 16, 0, 0) + timedelta(days=1)
        deadline = pytz.timezone('US/Eastern').localize(naive_dt_deadline)
        week.pick_deadline = deadline
        week.lock_picks = True
        week.save()

        test_db.setup_week_final(1983,1)
        test_db.setup_week_with_no_games(1983,2)

        super(PoolStateTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        test_db = UnitTestDatabase()
        test_db.delete_database()
        super(PoolStateTest, cls).tearDownClass()

    def test_end_of_year(self):
        self.assertEqual(self.__get_pool_state(year=2013),"end_of_year")

    def test_invalid_year(self):
        self.assertEqual(self.__get_pool_state(year=1900),"invalid")
        self.assertEqual(self.__get_pool_state(year=1950),"invalid")

    def test_pool_not_started(self):
        self.assertEqual(self.__get_pool_state(year=1975),"not_started")

    def test_enter_picks(self):
        self.assertEqual(self.__get_pool_state(year=1981),"enter_picks")

    def test_week_not_started(self):
        self.assertEqual(self.__get_pool_state(year=1978),"week_not_started")

    def test_week_in_progress(self):
        self.assertEqual(self.__get_pool_state(year=1979),"week_in_progress")

    def test_week_final(self):
        self.assertEqual(self.__get_pool_state(year=1980),"week_final")

    def test_week_locked(self):
        self.assertEqual(self.__get_pool_state(year=1982),"week_setup")

    def test_week_no_games(self):
        self.assertEqual(self.__get_pool_state(year=1983),"week_setup")

    def __get_pool_state(self,year):
        d = Database()
        pool_state = d.get_pool_state(year)
        return pool_state
