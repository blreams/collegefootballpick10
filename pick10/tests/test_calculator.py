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

    def test_t2_get_team_name_player_picked_to_win(self):
        self.__t2_invalid_player()
        self.__t2_invalid_game()
        self.__t2_game_none()
        self.__t2_team1_winner()
        self.__t2_team2_winner()
        self.__t2_winner_missing()

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

    def test_t4_is_team2_winning_pool(self):
        self.__t4_bad_game_favored_value()
        self.__t4_team2_ahead()
        self.__t4_team2_behind()
        self.__t4_team2_ahead_in_pool_behind_in_game()
        self.__t4_team2_behind_in_pool_ahead_in_game()
        self.__t4_team2_boundary_case1()
        self.__t4_team2_boundary_case2()
        self.__t4_team2_boundary_case3()
        self.__t4_team2_boundary_case4()

    def test_t5_get_pool_game_winner(self):
        self.__t5_game_none()
        self.__t5_game_in_progress()
        self.__t5_game_not_started()
        self.__t5_team1_won()
        self.__t5_team2_won()

    def test_t6_get_pool_game_winner_team_name(self):
        self.__t6_game_none()
        self.__t6_game_in_progress()
        self.__t6_game_not_started()
        self.__t6_team1_won()
        self.__t6_team2_won()

    def test_t7_get_game_winner(self):
        self.__t7_game_none()
        self.__t7_game_in_progress()
        self.__t7_game_not_started()
        self.__t7_same_score()
        self.__t7_team1_won()
        self.__t7_team2_won()
        self.__t7_team1_won_but_not_favored()
        self.__t7_team2_won_but_not_favored()

    def test_t8_get_game_winner_team_name(self):
        self.__t8_game_none()
        self.__t8_game_in_progress()
        self.__t8_game_not_started()
        self.__t8_same_score()
        self.__t8_team1_won()
        self.__t8_team2_won()

    def test_t9_get_team_winning_pool_game(self):
        self.__t9_game_none()
        self.__t9_game_final()
        self.__t9_game_not_started()
        self.__t9_same_score()
        self.__t9_team1_ahead()
        self.__t9_team2_ahead()

    def test_t10_get_team_name_winning_pool_game(self):
        self.__t10_game_none()
        self.__t10_game_final()
        self.__t10_game_not_started()
        self.__t10_same_score()
        self.__t10_team1_ahead()
        self.__t10_team2_ahead()

    def test_t11_get_team_winning_game(self):
        self.__t11_game_none()
        self.__t11_game_final()
        self.__t11_game_not_started()
        self.__t11_same_score()
        self.__t11_team1_ahead()
        self.__t11_team2_ahead()

    def test_t12_get_team_name_winning_game(self):
        self.__t12_game_none()
        self.__t12_game_final()
        self.__t12_game_not_started()
        self.__t12_same_score()
        self.__t12_team1_ahead()
        self.__t12_team2_ahead()

    def test_t13_player_did_not_pick(self):
        pass
        #self.__t13_game_none()
        #self.__t13_game_invalid()
        #self.__t13_invalid_player()
        #self.__t13_player_missing_all_week_picks()
        #self.__t13_player_missing_pick_for_game()
        #self.__t13_player_missing_pick_winner()
        #self.__t13_player_made_pick()

    def test_t14_did_player_win_game(self):
        pass
        #self.__t14_game_none()
        #self.__t14_invalid_player()
        #self.__t14_player_missing_pick()
        #self.__t14_game_in_progress()
        #self.__t14_game_not_started()
        #self.__t14_player_won_game()
        #self.__t14_player_lost_game()

    def test_t15_did_player_lose_game(self):
        pass
        #self.__t15_game_none()
        #self.__t15_invalid_player()
        #self.__t15_player_missing_pick()
        #self.__t15_game_in_progress()
        #self.__t15_game_not_started()
        #self.__t15_player_won_game()
        #self.__t15_player_lost_game()

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

    def __t2_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        game = self.__get_a_valid_game()
        with self.assertRaises(KeyError):
            self.calc.get_team_name_player_picked_to_win(bad_player,game)

    def __t2_invalid_game(self):
        invalid_game = self.__get_a_valid_game2()
        valid_player = self.week1.get_player("holden_brent")
        with self.assertRaises(AssertionError):
            self.calc.get_team_name_player_picked_to_win(valid_player,invalid_game)

    def __t2_game_none(self):
        valid_player = self.week1.get_player("holden_brent")
        with self.assertRaises(AssertionError):
            self.calc.get_team_name_player_picked_to_win(valid_player,None)

    def __t2_team2_winner(self):
        game = self.__find_game("North Carolina","South Carolina")
        brent = self.week1.get_player("holden_brent")
        team = self.calc.get_team_name_player_picked_to_win(brent,game)
        self.assertEqual(team,"South Carolina")

    def __t2_team1_winner(self):
        game = self.__find_game("LSU","TCU")
        brent = self.week1.get_player("holden_brent")
        team = self.calc.get_team_name_player_picked_to_win(brent,game)
        self.assertEqual(team,"LSU")

    def __t2_winner_missing(self):
        player = self.week1.get_player("holden_brent")
        game = self.__get_a_valid_game()

        self.__make_winner_missing(player,game)
        team = self.calc.get_team_name_player_picked_to_win(player,game)
        self.assertEqual(team,"")

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

    def __t4_bad_game_favored_value(self):
        g = Game()
        g.team1_actual_points = 0
        g.team2_actual_points = 0
        g.favored = 0
        g.spread = 0.5
        with self.assertRaises(AssertionError):
            self.calc.is_team2_winning_pool(g)

    def __t4_team2_ahead(self):
        g = Game()
        g.team1_actual_points = 10 
        g.team2_actual_points = 20 
        g.favored = TEAM2
        g.spread = 5.5 
        self.assertTrue(self.calc.is_team2_winning_pool(g))

    def __t4_team2_behind(self):
        g = Game()
        g.team1_actual_points = 20 
        g.team2_actual_points = 10 
        g.favored = TEAM2
        g.spread = 5.5 
        self.assertFalse(self.calc.is_team2_winning_pool(g))

    def __t4_team2_ahead_in_pool_behind_in_game(self):
        g = Game()
        g.team1_actual_points = 17 
        g.team2_actual_points = 14 
        g.favored = TEAM1
        g.spread = 3.5 
        self.assertTrue(self.calc.is_team2_winning_pool(g))

    def __t4_team2_behind_in_pool_ahead_in_game(self):
        g = Game()
        g.team1_actual_points = 17
        g.team2_actual_points = 21
        g.favored = TEAM2
        g.spread = 4.5 
        self.assertFalse(self.calc.is_team2_winning_pool(g))

    def __t4_team2_boundary_case1(self):
        g = Game()
        g.team1_actual_points = 16 
        g.team2_actual_points = 17 
        g.favored = TEAM2
        g.spread = 0.5 
        self.assertTrue(self.calc.is_team2_winning_pool(g))

    def __t4_team2_boundary_case2(self):
        g = Game()
        g.team1_actual_points = 17 
        g.team2_actual_points = 16 
        g.favored = TEAM2
        g.spread = 0.5 
        self.assertFalse(self.calc.is_team2_winning_pool(g))

    def __t4_team2_boundary_case3(self):
        g = Game()
        g.team1_actual_points = 16 
        g.team2_actual_points = 17 
        g.favored = TEAM1
        g.spread = 0.5 
        self.assertTrue(self.calc.is_team2_winning_pool(g))

    def __t4_team2_boundary_case4(self):
        g = Game()
        g.team1_actual_points = 17 
        g.team2_actual_points = 16 
        g.favored = TEAM1
        g.spread = 0.5 
        self.assertFalse(self.calc.is_team2_winning_pool(g))

    def __t5_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_pool_game_winner(None)

    def __t5_game_in_progress(self):
        g = Game()
        g.game_state = IN_PROGRESS
        self.assertIsNone(self.calc.get_pool_game_winner(g))

    def __t5_game_not_started(self):
        g = Game()
        g.game_state = NOT_STARTED
        self.assertIsNone(self.calc.get_pool_game_winner(g))

    def __t5_team1_won(self):
        g = Game()
        g.team1_actual_points = 30 
        g.team2_actual_points = 10 
        g.favored = TEAM1
        g.spread = 10.5
        g.game_state = FINAL
        self.assertEqual(self.calc.get_pool_game_winner(g),TEAM1)

    def __t5_team2_won(self):
        g = Game()
        g.team1_actual_points = 30 
        g.team2_actual_points = 25 
        g.favored = TEAM1
        g.spread = 10.5
        g.game_state = FINAL
        self.assertEqual(self.calc.get_pool_game_winner(g),TEAM2)

    def __t6_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_pool_game_winner_team_name(None)

    def __t6_game_in_progress(self):
        g = Game()
        g.game_state = IN_PROGRESS
        self.assertIsNone(self.calc.get_pool_game_winner_team_name(g))

    def __t6_game_not_started(self):
        g = Game()
        g.game_state = NOT_STARTED
        self.assertIsNone(self.calc.get_pool_game_winner_team_name(g))

    def __t6_team1_won(self):
        game = self.__find_game("LSU","TCU")
        self.assertEqual(self.calc.get_pool_game_winner_team_name(game),"LSU")

    def __t6_team2_won(self):
        game = self.__find_game("Boise State","Washington")
        self.assertEqual(self.calc.get_pool_game_winner_team_name(game),"Washington")

    def __t7_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_game_winner(None)

    def __t7_game_in_progress(self):
        g = Game()
        g.game_state = IN_PROGRESS
        self.assertIsNone(self.calc.get_game_winner(g))

    def __t7_game_not_started(self):
        g = Game()
        g.game_state = NOT_STARTED
        self.assertIsNone(self.calc.get_game_winner(g))

    def __t7_same_score(self):
        g = Game()
        g.team1_actual_points = 21
        g.team2_actual_points = 21
        g.favored = TEAM1
        g.spread = 10.5
        g.game_state = FINAL
        with self.assertRaises(AssertionError):
            self.calc.get_game_winner(g)

    def __t7_team1_won(self):
        g = Game()
        g.team1_actual_points = 31
        g.team2_actual_points = 21
        g.favored = TEAM1
        g.spread = 10.5
        g.game_state = FINAL
        self.assertEqual(self.calc.get_game_winner(g),TEAM1)

    def __t7_team2_won(self):
        g = Game()
        g.team1_actual_points = 10 
        g.team2_actual_points = 24 
        g.favored = TEAM2
        g.spread = 14.5
        g.game_state = FINAL
        self.assertEqual(self.calc.get_game_winner(g),TEAM2)

    def __t7_team1_won_but_not_favored(self):
        g = Game()
        g.team1_actual_points = 24
        g.team2_actual_points = 21
        g.favored = TEAM2
        g.spread = 5.5
        g.game_state = FINAL
        self.assertEqual(self.calc.get_game_winner(g),TEAM1)

    def __t7_team2_won_but_not_favored(self):
        g = Game()
        g.team1_actual_points = 41
        g.team2_actual_points = 48
        g.favored = TEAM1
        g.spread = 7.5
        g.game_state = FINAL
        self.assertEqual(self.calc.get_game_winner(g),TEAM2)

    def __t8_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_game_winner_team_name(None)

    def __t8_game_in_progress(self):
        g = Game()
        g.game_state = IN_PROGRESS
        self.assertIsNone(self.calc.get_game_winner_team_name(g))

    def __t8_game_not_started(self):
        g = Game()
        g.game_state = NOT_STARTED
        self.assertIsNone(self.calc.get_game_winner_team_name(g))

    def __t8_same_score(self):
        g = Game()
        g.team1_actual_points = 21
        g.team2_actual_points = 21
        g.favored = TEAM1
        g.spread = 10.5
        g.game_state = FINAL
        with self.assertRaises(AssertionError):
            self.calc.get_game_winner_team_name(g)

    def __t8_team1_won(self):
        game = self.__find_game("Penn State","Syracuse")
        self.assertEqual(self.calc.get_game_winner_team_name(game),"Penn State")

    def __t8_team2_won(self):
        game = self.__find_game("Georgia","Clemson")
        self.assertEqual(self.calc.get_game_winner_team_name(game),"Clemson")

    def __t9_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_team_winning_pool_game(None)

    def __t9_game_final(self):
        g = Game()
        g.game_state = FINAL
        self.assertIsNone(self.calc.get_team_winning_pool_game(g))

    def __t9_game_not_started(self):
        g = Game()
        g.game_state = NOT_STARTED
        self.assertIsNone(self.calc.get_team_winning_pool_game(g))

    def __t9_same_score(self):
        g = Game()
        g.team1_actual_points = 35
        g.team2_actual_points = 35
        g.favored = TEAM1
        g.spread = 0.5
        g.game_state = IN_PROGRESS
        self.assertEqual(self.calc.get_team_winning_pool_game(g),TEAM2)

    def __t9_team1_ahead(self):
        g = Game()
        g.team1_actual_points = 44
        g.team2_actual_points = 48
        g.favored = TEAM2
        g.spread = 4.5
        g.game_state = IN_PROGRESS
        self.assertEqual(self.calc.get_team_winning_pool_game(g),TEAM1)

    def __t9_team2_ahead(self):
        g = Game()
        g.team1_actual_points = 21
        g.team2_actual_points = 18
        g.favored = TEAM1
        g.spread = 3.5
        g.game_state = IN_PROGRESS
        self.assertEqual(self.calc.get_team_winning_pool_game(g),TEAM2)

    def __t10_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_team_name_winning_pool_game(None)

    def __t10_game_final(self):
        g = Game()
        g.game_state = FINAL
        self.assertIsNone(self.calc.get_team_name_winning_pool_game(g))

    def __t10_game_not_started(self):
        g = Game()
        g.game_state = NOT_STARTED
        self.assertIsNone(self.calc.get_team_name_winning_pool_game(g))

    def __t10_same_score(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_actual_points = 35
        g.team2_actual_points = 35
        g.favored = TEAM1
        g.spread = 0.5
        g.game_state = IN_PROGRESS
        self.assertEqual(self.calc.get_team_name_winning_pool_game(g),"Clemson")

    def __t10_team1_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_actual_points = 44
        g.team2_actual_points = 48
        g.favored = TEAM2
        g.spread = 4.5
        g.game_state = IN_PROGRESS
        self.assertEqual(self.calc.get_team_name_winning_pool_game(g),"Georgia Tech")

    def __t10_team2_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_actual_points = 21
        g.team2_actual_points = 18
        g.favored = TEAM1
        g.spread = 3.5
        g.game_state = IN_PROGRESS
        self.assertEqual(self.calc.get_team_name_winning_pool_game(g),"Clemson")

    def __t11_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_team_winning_game(None)

    def __t11_game_final(self):
        g = Game()
        g.game_state = FINAL
        self.assertIsNone(self.calc.get_team_winning_game(g))

    def __t11_game_not_started(self):
        g = Game()
        g.game_state = NOT_STARTED
        self.assertIsNone(self.calc.get_team_winning_game(g))

    def __t11_same_score(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_actual_points = 35
        g.team2_actual_points = 35
        g.favored = TEAM1
        g.spread = 0.5
        g.game_state = IN_PROGRESS
        self.assertEqual(self.calc.get_team_winning_game(g),TIED)

    def __t11_team1_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_actual_points = 31
        g.team2_actual_points = 24
        g.favored = TEAM2
        g.spread = 4.5
        g.game_state = IN_PROGRESS
        self.assertEqual(self.calc.get_team_winning_game(g),TEAM1)

    def __t11_team2_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_actual_points = 17
        g.team2_actual_points = 31
        g.favored = TEAM1
        g.spread = 3.5
        g.game_state = IN_PROGRESS
        self.assertEqual(self.calc.get_team_winning_game(g),TEAM2)

    def __t12_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_team_name_winning_game(None)

    def __t12_game_final(self):
        g = Game()
        g.game_state = FINAL
        self.assertIsNone(self.calc.get_team_name_winning_game(g))

    def __t12_game_not_started(self):
        g = Game()
        g.game_state = NOT_STARTED
        self.assertIsNone(self.calc.get_team_name_winning_game(g))

    def __t12_same_score(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_actual_points = 35
        g.team2_actual_points = 35
        g.favored = TEAM1
        g.spread = 0.5
        g.game_state = IN_PROGRESS
        self.assertEqual(self.calc.get_team_name_winning_game(g),"tied")

    def __t12_team1_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_actual_points = 31
        g.team2_actual_points = 24
        g.favored = TEAM2
        g.spread = 4.5
        g.game_state = IN_PROGRESS
        self.assertEqual(self.calc.get_team_name_winning_game(g),"Georgia Tech")

    def __t12_team2_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_actual_points = 17
        g.team2_actual_points = 31
        g.favored = TEAM1
        g.spread = 3.5
        g.game_state = IN_PROGRESS
        self.assertEqual(self.calc.get_team_name_winning_game(g),"Clemson")

    def __t13_game_none(self):
        valid_player = self.week1.get_player("holden_brent")
        with self.assertRaises(Exception):
            self.calc.player_did_not_pick(valid_player,None)

    def __t13_game_invalid(self):
        valid_player = self.week1.get_player("holden_brent")
        invalid_game = self.__get_a_valid_game2()
        with self.assertRaises(Exception):
            self.calc.player_did_not_pick(valid_player,invalid_game)

    def __t13_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        game = self.__get_a_valid_game()
        with self.assertRaises(Exception):
            self.calc.player_did_not_pick(bad_player,game)

    # TODO
    def __t13_player_missing_all_week_picks(self):
        valid_player = self.week1.get_player("holden_brent")
        player_key = self.__get_a_valid_player_key()
        game_key = self.__get_a_valid_game_key()
        self.__make_all_picks_missing(player_key)
        self.assertTrue(self.calc.player_did_not_pick(player_key,game_key))
        self.__restore_picks(player_key)

    def __t13_player_missing_pick_for_game(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__get_a_valid_game_key()

        self.__remove_game_from_picks(player_key,game_key)
        self.assertTrue(self.calc.player_did_not_pick(player_key,game_key))
        self.__restore_picks(player_key)


    def __t13_player_missing_pick_winner(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__get_a_valid_game_key()

        self.__make_winner_missing(player_key,game_key)
        self.assertTrue(self.calc.player_did_not_pick(player_key,game_key))
        self.__restore_picks(player_key)

    def __t13_player_made_pick(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__get_a_valid_game_key()
        self.assertFalse(self.calc.player_did_not_pick(player_key,game_key))

    def __t14_game_none(self):
        player_key = self.__get_a_valid_player_key()
        with self.assertRaises(Exception):
            self.calc.did_player_win_game(player_key,None)

    def __t14_invalid_player(self):
        game_key = self.__get_a_valid_game_key()
        with self.assertRaises(Exception):
            self.calc.did_player_win_game("bad key",game_key)

    def __t14_player_missing_pick(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__get_a_valid_game_key()

        self.__remove_game_from_picks(player_key,game_key)
        self.assertFalse(self.calc.did_player_win_game(player_key,game_key))
        self.__restore_picks(player_key)

    def __t14_game_in_progress(self):
        player_key = self.week1.get_player_key("Brent H.")
        g = Game()
        g.game_state = IN_PROGRESS
        game_key = self.__edit_existing_game(g)
        self.assertFalse(self.calc.did_player_win_game(player_key,game_key))
        self.__restore_game(game_key)

    def __t14_game_not_started(self):
        player_key = self.week1.get_player_key("Brent H.")
        g = Game()
        g.game_state = NOT_STARTED
        game_key = self.__edit_existing_game(g)
        self.assertFalse(self.calc.did_player_win_game(player_key,game_key))
        self.__restore_game(game_key)

    def __t14_player_won_game(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__find_game_key("North Carolina","South Carolina")
        self.assertTrue(self.calc.did_player_win_game(player_key,game_key))

    def __t14_player_lost_game(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__find_game_key("Penn State","Syracuse")
        self.assertFalse(self.calc.did_player_win_game(player_key,game_key))

    def __t15_game_none(self):
        player_key = self.__get_a_valid_player_key()
        with self.assertRaises(Exception):
            self.calc.did_player_lose_game(player_key,None)

    def __t15_invalid_player(self):
        game_key = self.__get_a_valid_game_key()
        with self.assertRaises(Exception):
            self.calc.did_player_lose_game("bad key",game_key)

    def __t15_player_missing_pick(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__get_a_valid_game_key()

        self.__remove_game_from_picks(player_key,game_key)
        self.assertTrue(self.calc.did_player_lose_game(player_key,game_key))
        self.__restore_picks(player_key)

    def __t15_game_in_progress(self):
        player_key = self.week1.get_player_key("Brent H.")
        g = Game()
        g.game_state = IN_PROGRESS
        game_key = self.__edit_existing_game(g)
        self.assertFalse(self.calc.did_player_lose_game(player_key,game_key))
        self.__restore_game(game_key)

    def __t15_game_not_started(self):
        player_key = self.week1.get_player_key("Brent H.")
        g = Game()
        g.game_state = NOT_STARTED
        game_key = self.__edit_existing_game(g)
        self.assertFalse(self.calc.did_player_lose_game(player_key,game_key))
        self.__restore_game(game_key)

    def __t15_player_won_game(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__find_game_key("North Carolina","South Carolina")
        self.assertFalse(self.calc.did_player_lose_game(player_key,game_key))

    def __t15_player_lost_game(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__find_game_key("Penn State","Syracuse")
        self.assertTrue(self.calc.did_player_lose_game(player_key,game_key))

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

    def __find_team(self,name):
        if name not in self.week1.teams:
            raise AssertionError,"Could not find team %s" % (name)
        return self.week1.teams[name]

    def __make_winner_missing(self,player,game):
        for i,pick in enumerate(self.week1.player_picks[player.id]):
            if pick.game == game:
                self.week1.player_picks[player.id][i].winner = 0
                return
        raise AssertionError,"could not find game in picks"
