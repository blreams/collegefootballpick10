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
        #test_db.load_historical_data_for_week(2013,1)
        #test_db.load_historical_data_for_week(2013,2)

    def setUp(self):
        self.calc = CalculateResults(data=None)

    # test is_team1_winning_pool
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

