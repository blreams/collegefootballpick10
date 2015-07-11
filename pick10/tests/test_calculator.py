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

    # t13 tests are broken up into multiple functions
    # to allow setUp() to run again and restore data
    def test_t13_player_did_not_pick(self):
        self.__t13_game_none()
        self.__t13_game_invalid()
        self.__t13_invalid_player()

    def test_t13_1_player_did_not_pick(self):
        self.__t13_player_missing_all_week_picks()

    def test_t13_2_player_did_not_pick(self):
        self.__t13_player_missing_pick_for_game()

    def test_t13_3_player_did_not_pick(self):
        self.__t13_player_missing_pick_winner()

    def test_t13_4_player_did_not_pick(self):
        self.__t13_player_made_pick()

    def test_t14_did_player_win_game(self):
        self.__t14_game_none()
        self.__t14_invalid_player()
        self.__t14_player_won_game()
        self.__t14_player_lost_game()

    def test_t14_1_did_player_win_game(self):
        self.__t14_player_missing_pick()

    def test_t14_2_did_player_win_game(self):
        self.__t14_game_in_progress()

    def test_t14_3_did_player_win_game(self):
        self.__t14_game_not_started()

    def test_t15_did_player_lose_game(self):
        self.__t15_game_none()
        self.__t15_invalid_player()
        self.__t15_player_won_game()
        self.__t15_player_lost_game()

    def test_t15_1_did_player_lose_game(self):
        self.__t15_player_missing_pick()

    def test_t15_2_did_player_lose_game(self):
        self.__t15_game_in_progress()

    def test_t15_3_did_player_lose_game(self):
        self.__t15_game_not_started()

    def test_t16_get_number_of_wins(self):
        self.__t16_invalid_player()

    def test_t16_1_get_number_of_wins(self):
        self.__t16_no_games_started()

    def test_t16_2_get_number_of_wins(self):
        self.__t16_some_games_in_progress()

    def test_t16_3_get_number_of_wins(self):
        self.__t16_mixed_game_states()

    def test_t16_4_get_number_of_wins(self):
        self.__t16_all_games_final()

    def test_t16_5_get_number_of_wins(self):
        self.__t16_player_with_no_picks()

    def test_t16_6_get_number_of_wins(self):
        self.__t16_player_0_wins()

    def test_t16_7_get_number_of_wins(self):
        self.__t16_player_10_wins()

    def test_t17_get_number_of_losses(self):
        self.__t17_invalid_player()

    def test_t17_1_get_number_of_losses(self):
        self.__t17_no_games_started()

    def test_t17_2_get_number_of_losses(self):
        self.__t17_some_games_in_progress()

    def test_t17_3_get_number_of_losses(self):
        self.__t17_mixed_game_states()

    def test_t17_4_get_number_of_losses(self):
        self.__t17_all_games_final()

    def test_t17_5_get_number_of_losses(self):
        self.__t17_player_with_no_picks()

    def test_t17_6_get_number_of_losses(self):
        self.__t17_player_0_losses()

    def test_t17_7_get_number_of_losses(self):
        self.__t17_player_10_losses()

    def test_t18_is_player_winning_game(self):
        self.__t18_game_none()
        self.__t18_invalid_player()

    def test_t18_1_is_player_winning_game(self):
        self.__t18_player_pick_missing_game_not_started()

    def test_t18_2_is_player_winning_game(self):
        self.__t18_player_pick_missing_game_in_progress()

    def test_t18_3_is_player_winning_game(self):
        self.__t18_player_pick_missing_game_final()

    def test_t18_4_is_player_winning_game(self):
        self.__t18_game_not_started()

    def test_t18_5_is_player_winning_game(self):
        self.__t18_game_final()

    def test_t18_6_is_player_winning_game(self):
        self.__t18_player_ahead_in_game_and_pool()

    def test_t18_7_is_player_winning_game(self):
        self.__t18_player_behind_in_game_and_pool()

    def test_t18_8_is_player_winning_game(self):
        self.__t18_player_ahead_in_game_and_behind_in_pool()

    def test_t18_8_is_player_winning_game(self):
        self.__t18_player_behind_in_game_and_ahead_in_pool()

    def test_t19_is_player_losing_game(self):
        #self.__t19_game_none()
        #self.__t19_invalid_player()
        #self.__t19_player_pick_missing_game_not_started()
        #self.__t19_player_pick_missing_game_in_progress()
        #self.__t19_player_pick_missing_game_final()
        #self.__t19_game_not_started()
        #self.__t19_game_final()
        #self.__t19_player_ahead_in_game_and_pool()
        #self.__t19_player_behind_in_game_and_pool()
        #self.__t19_player_ahead_in_game_and_behind_in_pool()
        #self.__t19_player_behind_in_game_and_ahead_in_pool()
        pass

    def test_t20_is_player_projected_to_win_game(self):
        #self.__t20_game_none()
        #self.__t20_invalid_player()
        #self.__t20_player_pick_missing()
        #self.__t20_game_final_player_ahead_in_game_and_pool()
        #self.__t20_game_final_player_behind_in_game_and_pool()
        #self.__t20_game_final_player_ahead_in_game_and_behind_in_pool()
        #self.__t20_game_final_player_behind_in_game_and_ahead_in_pool()
        #self.__t20_game_in_progress_player_ahead_in_game_and_pool()
        #self.__t20_game_in_progress_player_behind_in_game_and_pool()
        #self.__t20_game_in_progress_player_ahead_in_game_and_behind_in_pool()
        #self.__t20_game_in_progress_player_behind_in_game_and_ahead_in_pool()
        #self.__t20_game_not_started_player_ahead_in_game_and_pool()
        #self.__t20_game_not_started_player_behind_in_game_and_pool()
        #self.__t20_game_not_started_player_ahead_in_game_and_behind_in_pool()
        #self.__t20_game_not_started_player_behind_in_game_and_ahead_in_pool()
        pass


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

    def __t13_player_missing_all_week_picks(self):
        player = self.week1.get_player("holden_brent")
        game = self.__get_a_valid_game()
        self.__make_all_picks_missing(player)
        self.assertTrue(self.calc.player_did_not_pick(player,game))

    def __t13_player_missing_pick_for_game(self):
        player = self.week1.get_player("holden_brent")
        game = self.__get_a_valid_game()
        self.__remove_game_from_picks(player,game)
        self.assertTrue(self.calc.player_did_not_pick(player,game))

    def __t13_player_missing_pick_winner(self):
        player = self.week1.get_player("holden_brent")
        game = self.__get_a_valid_game()
        self.__make_winner_missing(player,game)
        self.assertTrue(self.calc.player_did_not_pick(player,game))

    def __t13_player_made_pick(self):
        player = self.week1.get_player("holden_brent")
        game = self.__get_a_valid_game()
        self.assertFalse(self.calc.player_did_not_pick(player,game))

    def __t14_game_none(self):
        player = self.week1.get_player("holden_brent")
        with self.assertRaises(Exception):
            self.calc.did_player_win_game(player,None)

    def __t14_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        game = self.__get_a_valid_game()
        with self.assertRaises(Exception):
            self.calc.did_player_win_game(bad_player,game)

    def __t14_player_missing_pick(self):
        player = self.week1.get_player("holden_brent")
        game = self.__get_a_valid_game()

        self.__remove_game_from_picks(player,game)
        self.assertFalse(self.calc.did_player_win_game(player,game))

    def __t14_game_in_progress(self):
        player = self.week1.get_player("holden_brent")
        game = self.__get_a_valid_game()
        game.game_state = IN_PROGRESS
        self.assertFalse(self.calc.did_player_win_game(player,game))

    def __t14_game_not_started(self):
        player = self.week1.get_player("holden_brent")
        game = self.__get_a_valid_game()
        game.game_state = NOT_STARTED
        self.assertFalse(self.calc.did_player_win_game(player,game))

    def __t14_player_won_game(self):
        player = self.week1.get_player("holden_brent")
        game = self.__find_game("North Carolina","South Carolina")
        self.assertTrue(self.calc.did_player_win_game(player,game))

    def __t14_player_lost_game(self):
        player = self.week1.get_player("holden_brent")
        game = self.__find_game("Penn State","Syracuse")
        self.assertFalse(self.calc.did_player_win_game(player,game))

    def __t15_game_none(self):
        player = self.week1.get_player("holden_brent")
        with self.assertRaises(Exception):
            self.calc.did_player_lose_game(player,None)

    def __t15_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        game = self.__get_a_valid_game()
        with self.assertRaises(Exception):
            self.calc.did_player_lose_game(bad_player,game)

    def __t15_player_missing_pick(self):
        player = self.week1.get_player("holden_brent")
        game = self.__get_a_valid_game()
        self.__remove_game_from_picks(player,game)
        self.assertTrue(self.calc.did_player_lose_game(player,game))

    def __t15_game_in_progress(self):
        player = self.week1.get_player("holden_brent")
        game = self.__get_a_valid_game()
        game.game_state = IN_PROGRESS
        self.assertFalse(self.calc.did_player_lose_game(player,game))

    def __t15_game_not_started(self):
        player = self.week1.get_player("holden_brent")
        game = self.__get_a_valid_game()
        game.game_state = NOT_STARTED
        self.assertFalse(self.calc.did_player_lose_game(player,game))

    def __t15_player_won_game(self):
        player = self.week1.get_player("holden_brent")
        game = self.__find_game("North Carolina","South Carolina")
        self.assertFalse(self.calc.did_player_lose_game(player,game))

    def __t15_player_lost_game(self):
        player = self.week1.get_player("holden_brent")
        game = self.__find_game("Penn State","Syracuse")
        self.assertTrue(self.calc.did_player_lose_game(player,game))

    def __t16_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        with self.assertRaises(Exception):
            self.calc.get_number_of_wins(bad_player)

    def __t16_no_games_started(self):
        player = self.week1.get_player("holden_brent")
        self.__modify_game_states([NOT_STARTED]*10)
        self.assertEqual(self.calc.get_number_of_wins(player),0)

    def __t16_some_games_in_progress(self):
        player = self.week1.get_player("holden_brent")
        states = [NOT_STARTED]*3 + [IN_PROGRESS]*7
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_wins(player),0)

    def __t16_mixed_game_states(self):
        player = self.week1.get_player("holden_brent")
        num_wins_in_first_3_games_2013_week_1 = 2

        states = [FINAL]*3 + [NOT_STARTED]*3 + [IN_PROGRESS]*4
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_wins(player),num_wins_in_first_3_games_2013_week_1)

    def __t16_all_games_final(self):
        player = self.week1.get_player("holden_brent")
        num_wins_2013_week_1 = 5
        self.assertEqual(self.calc.get_number_of_wins(player),num_wins_2013_week_1)

    def __t16_player_with_no_picks(self):
        player = self.week1.get_player("holden_brent")
        self.__make_all_player_picks_not_entered(player)
        self.assertEqual(self.calc.get_number_of_wins(player),0)

    def __t16_player_0_wins(self):
        player = self.week1.get_player("robbins_dale")
        self.__make_dale_0_wins()
        self.assertEqual(self.calc.get_number_of_wins(player),0)

    def __t16_player_10_wins(self):
        player = self.week1.get_player("murphy_william")
        self.__make_william_10_wins()
        self.assertEqual(self.calc.get_number_of_wins(player),10)

    def __t17_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        with self.assertRaises(Exception):
            self.calc.get_number_of_losses(bad_player)

    def __t17_no_games_started(self):
        player = self.week1.get_player("holden_brent")
        self.__modify_game_states([NOT_STARTED]*10)
        self.assertEqual(self.calc.get_number_of_losses(player),0)

    def __t17_some_games_in_progress(self):
        player = self.week1.get_player("holden_brent")
        states = [NOT_STARTED]*3 + [IN_PROGRESS]*7
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_losses(player),0)

    def __t17_mixed_game_states(self):
        player = self.week1.get_player("holden_brent")
        num_losses_in_first_3_games_2013_week_1 = 1

        states = [FINAL]*3 + [NOT_STARTED]*3 + [IN_PROGRESS]*4
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_losses(player),num_losses_in_first_3_games_2013_week_1)

    def __t17_all_games_final(self):
        player = self.week1.get_player("reams_byron")
        num_losses_2013_week_1 = 4
        self.assertEqual(self.calc.get_number_of_losses(player),num_losses_2013_week_1)

    def __t17_player_with_no_picks(self):
        player = self.week1.get_player("holden_brent")
        self.__make_all_player_picks_not_entered(player)
        self.assertEqual(self.calc.get_number_of_losses(player),10)

    def __t17_player_0_losses(self):
        player = self.week1.get_player("murphy_william")
        self.__make_william_10_wins()
        self.assertEqual(self.calc.get_number_of_losses(player),0)

    def __t17_player_10_losses(self):
        player = self.week1.get_player("robbins_dale")
        self.__make_dale_0_wins()
        self.assertEqual(self.calc.get_number_of_losses(player),10)

    def __t18_game_none(self):
        valid_player = self.week1.get_player("holden_brent")
        with self.assertRaises(Exception):
            self.calc.is_player_winning_game(valid_player,None)

    def __t18_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        game = self.__get_a_valid_game()
        with self.assertRaises(Exception):
            self.calc.is_player_winning_game(bad_player,game)

    def __t18_player_pick_missing_game_not_started(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = NOT_STARTED

        self.__make_winner_missing(player,game)
        self.assertFalse(self.calc.is_player_winning_game(player,game))


    def __t18_player_pick_missing_game_in_progress(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = IN_PROGRESS

        self.__make_winner_missing(player,game)
        self.assertFalse(self.calc.is_player_winning_game(player,game))

    def __t18_player_pick_missing_game_final(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = FINAL

        self.__make_winner_missing(player,game)
        self.assertFalse(self.calc.is_player_winning_game(player,game))

    def __t18_player_ahead_in_game_and_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_winning_game(player,game))

    def __t18_player_behind_in_game_and_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 30
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM1)
        self.assertFalse(self.calc.is_player_winning_game(player,game))

    def __t18_player_ahead_in_game_and_behind_in_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 5.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 25
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM2)
        self.assertFalse(self.calc.is_player_winning_game(player,game))

    def __t18_player_behind_in_game_and_ahead_in_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_winning_game(player,game))

    def __t18_game_not_started(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = NOT_STARTED

        self.__change_player_pick(player,game,TEAM1)
        self.assertFalse(self.calc.is_player_winning_game(player,game))

    def __t18_game_final(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = FINAL

        self.__change_player_pick(player,game,TEAM1)
        self.assertFalse(self.calc.is_player_winning_game(player,game))

    def __t19_game_none(self):
        player_key = self.__get_a_valid_player_key()
        with self.assertRaises(Exception):
            self.calc.is_player_losing_game(player_key,None)

    def __t19_invalid_player(self):
        game_key = self.__get_a_valid_game_key()
        with self.assertRaises(Exception):
            self.calc.is_player_losing_game("bad key",game_key)

    def __t19_game_not_started(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = NOT_STARTED

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM1)

        self.assertFalse(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_game_final(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = FINAL

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM1)

        self.assertFalse(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_player_pick_missing_game_not_started(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = NOT_STARTED

        game_key = self.__edit_existing_game(game)
        self.__make_winner_missing(player_key,game_key)

        self.assertTrue(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_player_pick_missing_game_in_progress(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = IN_PROGRESS

        game_key = self.__edit_existing_game(game)
        self.__make_winner_missing(player_key,game_key)

        self.assertTrue(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_player_pick_missing_game_final(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 25
        game.game_state = FINAL

        game_key = self.__edit_existing_game(game)
        self.__make_winner_missing(player_key,game_key)

        self.assertFalse(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_player_ahead_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = IN_PROGRESS

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM1)

        self.assertFalse(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_player_behind_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 30
        game.game_state = IN_PROGRESS

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM1)

        self.assertTrue(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_player_ahead_in_game_and_behind_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM2
        game.spread = 5.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 25
        game.game_state = IN_PROGRESS
        
        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM2)

        self.assertTrue(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_player_behind_in_game_and_ahead_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = IN_PROGRESS

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM1)

        self.assertFalse(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t20_game_none(self):
        player_key = self.__get_a_valid_player_key()
        with self.assertRaises(Exception):
            self.calc.is_player_projected_to_win_game(player_key,None)

    def __t20_invalid_player(self):
        game_key = self.__get_a_valid_game_key()
        with self.assertRaises(Exception):
            self.calc.is_player_projected_to_win_game("bad key",game_key)

    def __t20_player_pick_missing(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 25
        game.game_state = IN_PROGRESS

        game_key = self.__edit_existing_game(game)
        self.__make_winner_missing(player_key,game_key)

        self.assertFalse(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t20_game_final_player_ahead_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = FINAL

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM1)

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t20_game_final_player_behind_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 30
        game.game_state = FINAL

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM1)

        self.assertFalse(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t20_game_final_player_ahead_in_game_and_behind_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM2
        game.spread = 5.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 25
        game.game_state = FINAL

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM2)

        self.assertFalse(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)



    def __t20_game_final_player_behind_in_game_and_ahead_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = FINAL

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM1)

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t20_game_in_progress_player_ahead_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = IN_PROGRESS

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM1)

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)



    def __t20_game_in_progress_player_behind_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 30
        game.game_state = IN_PROGRESS

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM1)

        self.assertFalse(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t20_game_in_progress_player_ahead_in_game_and_behind_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM2
        game.spread = 5.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 25
        game.game_state = IN_PROGRESS

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM2)

        self.assertFalse(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t20_game_in_progress_player_behind_in_game_and_ahead_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = IN_PROGRESS

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM1)

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t20_game_not_started_player_ahead_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = NOT_STARTED

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM1)

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t20_game_not_started_player_behind_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 30
        game.game_state = NOT_STARTED

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM1)

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t20_game_not_started_player_ahead_in_game_and_behind_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM2
        game.spread = 5.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 25
        game.game_state = NOT_STARTED

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM2)

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t20_game_not_started_player_behind_in_game_and_ahead_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        player = self.week1.get_player("holden_brent")

        game = Game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = NOT_STARTED

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,TEAM1)

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


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

    def __make_all_picks_missing(self,player):
        self.week1.player_picks[player.id] = []

    def __remove_game_from_picks(self,player,game):
        new_picks = []
        for pick in self.week1.player_picks[player.id]:
            if pick.game != game:
                new_picks.append(pick)
        self.week1.player_picks[player.id] = new_picks

    def __modify_game_states(self,states):
        assert len(states) == 10
        assert len(self.week1.games) == 10

        for game_key in self.week1.games:
            game = self.week1.games[game_key]
            state_index = game.gamenum - 1
            self.week1.games[game_key].game_state = states[state_index]

    def __make_all_player_picks_not_entered(self,player):
        for i in range(len(self.week1.player_picks[player.id])):
            self.week1.player_picks[player.id][i].winner = 0

    def __make_dale_0_wins(self):
        player = self.week1.get_player("robbins_dale")
        game1 = self.__find_game("North Carolina","South Carolina")
        game2 = self.__find_game("Utah State","Utah")
        game3 = self.__find_game("Georgia","Clemson")
        self.__change_player_pick(player,game1)
        self.__change_player_pick(player,game2)
        self.__change_player_pick(player,game3)

    def __make_william_10_wins(self):
        player = self.week1.get_player("murphy_william")
        game1 = self.__find_game("Colorado","Colorado State")
        self.__change_player_pick(player,game1)

    def __change_player_pick(self,player,game,new_value=0):
        player_picks = self.week1.player_picks[player.id]
        for i,pick in enumerate(player_picks):
            if pick.game == game:
                if new_value != 0:
                    self.week1.player_picks[player.id][i].winner = new_value
                elif pick.winner == TEAM1:
                    self.week1.player_picks[player.id][i].winner = TEAM2
                elif pick.winner == TEAM2:
                    self.week1.player_picks[player.id][i].winner = TEAM1
