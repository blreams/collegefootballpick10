from django.test import TestCase
from pick10.database import Database
from pick10.calculator import *
from pick10.models import *
from unit_test_database import *

# This class tests the calculator.py file load_week_data function
class CalculatorTests(TestCase):

    @classmethod
    def setUpClass(cls):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_week(2013,1)
        test_db.load_historical_data_for_week(2013,2)

    def setUp(self):
        self.db = Database()
        self.week1 = self.db.load_week_data(2013,1)
        self.week2 = self.db.load_week_data(2013,2)
        self.calc = CalculateResults(data=self.week1)

    # function name decode:  
    # test_ : each function to test must start with test_ (unittest requirement)
    # _t<number>_ : unique identifier used to specify this test function
    # _<name> : this is the name of the function in calculator.py that is being tested
    def test_t1_get_team_player_picked_to_win(self):
        self.__t1_invalid_player()
        self.__t1_invalid_game()
        self.__t1_game_none()
        self.__t1_team1_winner()
        self.__t1_team2_winner()

    def test_t3_is_team1_winning_pool(self):
        self.__t3_bad_game_favored_value()
        self.__t3_team1_ahead()
        self.__t3_team1_behind()
        self.__t3_team1_ahead_in_pool_behind_in_game()
        self.__t3_team1_behind_in_pool_ahead_in_game()
        self.__t3_team1_boundary_case1()
        self.__t3_team1_boundary_case2()
        self.__t3_team1_boundary_case3()
        self.__t3_team1_boundary_case4()

    def __t1_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        game = self.__get_a_valid_game()
        with self.assertRaises(KeyError):
            self.calc.get_team_player_picked_to_win(bad_player,game)

    def __t1_invalid_game(self):
        invalid_game = self.__get_a_valid_game2()
        valid_player = self.week1.get_player("holden_brent")
        with self.assertRaises(AssertionError):
            self.calc.get_team_player_picked_to_win(valid_player,invalid_game)

    def __t1_game_none(self):
        valid_player = self.week1.get_player("holden_brent")
        with self.assertRaises(AssertionError):
            self.calc.get_team_player_picked_to_win(valid_player,None)

    def __t1_team2_winner(self):
        game = self.__find_game("North Carolina","South Carolina")
        brent = self.week1.get_player("holden_brent")
        team = self.calc.get_team_player_picked_to_win(brent,game)
        self.assertEqual(team,TEAM2)

    def __t1_team1_winner(self):
        game = self.__find_game("LSU","TCU")
        brent = self.week1.get_player("holden_brent")
        team = self.calc.get_team_player_picked_to_win(brent,game)
        self.assertEqual(team,TEAM1)

    def __t3_bad_game_favored_value(self):
        g = Game()
        g.team1_actual_points = 0
        g.team2_actual_points = 0
        g.favored = 0
        g.spread = 0.5
        with self.assertRaises(AssertionError):
            self.calc.is_team1_winning_pool(g)

    def __t3_team1_ahead(self):
        g = Game()
        g.team1_actual_points = 20 
        g.team2_actual_points = 10 
        g.favored = TEAM1
        g.spread = 5.5 
        self.assertTrue(self.calc.is_team1_winning_pool(g))

    def __t3_team1_behind(self):
        g = Game()
        g.team1_actual_points = 10 
        g.team2_actual_points = 20 
        g.favored = TEAM1
        g.spread = 5.5 
        self.assertFalse(self.calc.is_team1_winning_pool(g))

    def __t3_team1_ahead_in_pool_behind_in_game(self):
        g = Game()
        g.team1_actual_points = 14 
        g.team2_actual_points = 17 
        g.favored = TEAM2
        g.spread = 3.5 
        self.assertTrue(self.calc.is_team1_winning_pool(g))

    def __t3_team1_behind_in_pool_ahead_in_game(self):
        g = Game()
        g.team1_actual_points = 21 
        g.team2_actual_points = 17 
        g.favored = TEAM1
        g.spread = 4.5 
        self.assertFalse(self.calc.is_team1_winning_pool(g))

    def __t3_team1_boundary_case1(self):
        g = Game()
        g.team1_actual_points = 17 
        g.team2_actual_points = 16 
        g.favored = TEAM1
        g.spread = 0.5 
        self.assertTrue(self.calc.is_team1_winning_pool(g))

    def __t3_team1_boundary_case2(self):
        g = Game()
        g.team1_actual_points = 16 
        g.team2_actual_points = 17 
        g.favored = TEAM1
        g.spread = 0.5 
        self.assertFalse(self.calc.is_team1_winning_pool(g))

    def __t3_team1_boundary_case3(self):
        g = Game()
        g.team1_actual_points = 17 
        g.team2_actual_points = 16 
        g.favored = TEAM2
        g.spread = 0.5 
        self.assertTrue(self.calc.is_team1_winning_pool(g))

    def __t3_team1_boundary_case4(self):
        g = Game()
        g.team1_actual_points = 16 
        g.team2_actual_points = 17 
        g.favored = TEAM2
        g.spread = 0.5 
        self.assertFalse(self.calc.is_team1_winning_pool(g))

    def __get_a_valid_game(self):
        return self.week1.games[1]

    def __get_a_valid_game2(self):
        return self.week2.games[1]

    def __find_game(self,team1,team2):
        for game in self.week1.games.values():
            same_teams = team1 == game.team1.team_name and team2 == game.team2.team_name
            if same_teams:
                return game
        raise AssertionError, "Could not find game"
