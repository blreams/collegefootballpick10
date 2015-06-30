from django.test import TestCase
from pick10.database import Database
from pick10.models import *

# This class tests the database.py file load_week_data function
class LoadWeekDataTest(TestCase):

    # invalid year parameter
    # invalid week parameter
    # load the games information
    # load the player_picks information
    # load the players
    # load the teams

    def setUp(self):
        add_week(2014,1)
        self.db = Database()

    # call the load_week_data function
    def test_function_call(self):
        data = self.db.load_week_data(2014,1)
        self.assertIsNotNone(data)

    # load the week information
    def test_week_data_present(self):
        week = self.db.load_week_data(2014,1).week
        self.assertEqual(week.week_year,2014)
        self.assertEqual(week.week_num,1)
