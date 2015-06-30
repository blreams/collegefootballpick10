from django.test import TestCase
from pick10.database import Database

# This class tests the database.py file load_week_data function
class LoadWeekDataTest(TestCase):

    # check year parameter valid
    # check week_number parameter valid
    # load the week information
    # load the games information
    # load the player_picks information
    # load the players
    # load the teams

    # call the load_week_data function
    def test_load_week_data_function_call(self):
        db = Database()
        data = db.load_week_data(2014,1)
        self.assertIsNotNone(data)
