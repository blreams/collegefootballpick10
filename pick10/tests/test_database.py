from django.test import TestCase
from pick10.database import Database
from pick10.models import *

# This class tests the database.py file load_week_data function
class LoadWeekDataTest(TestCase):

    # invalid year parameter
    # invalid week parameter
    # load the player_picks information
    # load the players
    # load the teams

    def setUp(self):
        week = add_week(2014,1)
        conf = add_conference('ACC')
        team1 = add_team('Georgia Tech','Buzz',conf)
        team2 = add_team('Clemson','Tigers',conf)
        add_game(week,team1,team2,game_num=1,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=2,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=3,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=4,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=5,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=6,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=7,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=8,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=9,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=10,favored=1,spread=0.5)
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

    # load the games information
    def test_week_games_data_present(self):
        data = self.db.load_week_data(2014,1)
        self.assertEqual(len(data.games),10)
        self.assertEqual(set(data.games.keys()),set([1,2,3,4,5,6,7,8,9,10]))
        for game in data.games.values():
            self.assertEqual(game.week,data.week)
