from django.test import TestCase
from pick10.database import Database
from pick10.models import *
from unit_test_database import *

# This class tests the database.py file load_week_data function
class LoadWeekDataTest(TestCase):

    @classmethod
    def setUpClass(cls):
        test_db = UnitTestDatabase()
        test_db.setup_simple_week(2014,1)

    def setUp(self):
        self.db = Database()

    # call the load_week_data function
    def test_function_call(self):
        data = self.db.load_week_data(2014,1)
        self.assertIsNotNone(data)

    # invalid year parameter
    def test_bad_year_parameter(self):
        with self.assertRaises(Exception):
            data = self.db.load_week_data(1978,1)

    # invalid week parameter
    def test_bad_week_parameter(self):
        with self.assertRaises(Exception):
            data = self.db.load_week_data(2014,15)

    # load the week information
    def test_week_data_present(self):
        week = self.db.load_week_data(2014,1).week
        self.assertEqual(week.week_year,2014)
        self.assertEqual(week.week_num,1)

    # load the games information
    def test_week_games_data_present(self):
        data = self.db.load_week_data(2014,1)
        self.assertEqual(len(data.games),10)
        self.assertEqual(set(data.games.keys()),set([1,2,3,4,5,6,7,8,9,10]))
        for game in data.games.values():
            self.assertEqual(game.week,data.week)

    # load the teams
    def test_teams_data_present(self):
        data = self.db.load_week_data(2014,1)
        self.assertGreater(len(data.teams),0)
        self.assertIn('Georgia Tech',data.teams)
        self.assertIn('South Carolina',data.teams)
        self.assertIn('Clemson',data.teams)
        self.assertIn(data.teams['Georgia Tech'].team_name,'Georgia Tech')
        self.assertIn(data.teams['South Carolina'].team_name,'South Carolina')
        self.assertIn(data.teams['Clemson'].team_name,'Clemson')

    # load the players
    def test_players_data_present(self):
        self.fail('Users/Players implementation not final yet')

    # load the player_picks information
    def test_player_picks_data_present(self):
        self.fail('Users/Players implementation not final yet')
