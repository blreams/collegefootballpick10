from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

from django.test import TestCase
from ..database import Database
from .unit_test_database import UnitTestDatabase

# This class tests the database.py file load_week_data function
class LoadWeekDataTest(TestCase):

    @classmethod
    def setUpClass(cls):
        test_db = UnitTestDatabase()
        test_db.setup_simple_week(2014,1)
        test_db.load_historical_data_for_year(2013)
        super(LoadWeekDataTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        test_db = UnitTestDatabase()
        test_db.delete_database()
        super(LoadWeekDataTest, cls).tearDownClass()

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
        self.assertEqual(week.year.yearnum,2014)
        self.assertEqual(week.weeknum,1)

    # load the games indexed by game number information
    def test_week_games_data_present(self):
        data = self.db.load_week_data(2014,1)
        self.assertEqual(len(data.games),10)
        self.assertEqual(set(data.games.keys()),set([1,2,3,4,5,6,7,8,9,10]))
        for game in data.games.values():
            self.assertEqual(game.week,data.week)

    # load the games indexed by id information
    def test_week_games_id_data_present(self):
        data = self.db.load_week_data(2014,1)
        self.assertEqual(len(data.games_id),10)
        for game_id in data.games_id:
            game = data.games_id[game_id]
            self.assertEqual(game.week,data.week)
            self.assertEqual(game_id,game.id)

    # load the games indexed by id information
    def test_week_games_are_same(self):
        data = self.db.load_week_data(2014,1)
        for game in data.games.values():
            self.assertIn(game.id,data.games_id)

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
        data = self.db.load_week_data(2014,1)
        self.assertGreater(len(data.players),0)
        player_names = [ p.public_name for p in data.players.values() ]
        self.assertIn('Brent',player_names)
        self.assertIn('John',player_names)

    # load the picks
    def test_picks_data_present(self):
        data = self.db.load_week_data(2014,1)
        self.assertGreater(len(data.picks),0)

        for pick in data.picks.values():
            self.assertEqual(pick.game.week.weeknum,1)
            self.assertEqual(pick.game.week.year.yearnum,2014)

    # load the player_picks information
    def test_player_picks_data_present(self):
        data = self.db.load_week_data(2014,1)
        self.assertGreater(len(data.player_picks),0)

        for player_id in data.player_picks:
            player_picks = data.player_picks[player_id]
            self.assertEqual(len(player_picks),10)
            for pick in player_picks:
                self.assertEqual(pick.player.id,player_id)
                self.assertEqual(pick.game.week,data.week)

    def test_get_week_numbers(self):
        self.__get_weeks_test(2013,[1,2,3,4,5,6,7,8,9,10,11,12,13])

    def test_get_week_numbers_bad_year(self):
        self.__get_weeks_invalid_year_test()

    def __get_weeks_test(self,year,expected_weeks):
        d = Database()
        weeks = d.get_week_numbers(year)
        self.assertIsNotNone(weeks)
        self.assertEqual(weeks,expected_weeks)

    def __get_weeks_invalid_year_test(self):
        d = Database()
        with self.assertRaises(Exception):
            weeks = d.get_week_numbers(1900)

