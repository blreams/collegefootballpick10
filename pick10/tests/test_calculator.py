from django.test import TestCase
from pick10.database import Database
from pick10.calculator import *
from pick10.models import *
from unit_test_database import *
import datetime as dt

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

    def test_t18_9_is_player_winning_game(self):
        self.__t18_player_behind_in_game_and_ahead_in_pool()

    def test_t19_is_player_losing_game(self):
        self.__t19_game_none()
        self.__t19_invalid_player()

    def test_t19_1_is_player_losing_game(self):
        self.__t19_player_pick_missing_game_not_started()

    def test_t19_2_is_player_losing_game(self):
        self.__t19_player_pick_missing_game_in_progress()

    def test_t19_3_is_player_losing_game(self):
        self.__t19_player_pick_missing_game_final()

    def test_t19_4_is_player_losing_game(self):
        self.__t19_game_not_started()

    def test_t19_5_is_player_losing_game(self):
        self.__t19_game_final()

    def test_t19_6_is_player_losing_game(self):
        self.__t19_player_ahead_in_game_and_pool()

    def test_t19_7_is_player_losing_game(self):
        self.__t19_player_behind_in_game_and_pool()

    def test_t19_8_is_player_losing_game(self):
        self.__t19_player_ahead_in_game_and_behind_in_pool()

    def test_t19_9_is_player_losing_game(self):
        self.__t19_player_behind_in_game_and_ahead_in_pool()

    def test_t20_is_player_projected_to_win_game(self):
        self.__t20_game_none()
        self.__t20_invalid_player()

    def test_t20_1_is_player_projected_to_win_game(self):
        self.__t20_player_pick_missing()

    def test_t20_2_is_player_projected_to_win_game(self):
        self.__t20_game_final_player_ahead_in_game_and_pool()

    def test_t20_3_is_player_projected_to_win_game(self):
        self.__t20_game_final_player_behind_in_game_and_pool()

    def test_t20_4_is_player_projected_to_win_game(self):
        self.__t20_game_final_player_ahead_in_game_and_behind_in_pool()

    def test_t20_5_is_player_projected_to_win_game(self):
        self.__t20_game_final_player_behind_in_game_and_ahead_in_pool()

    def test_t20_6_is_player_projected_to_win_game(self):
        self.__t20_game_in_progress_player_ahead_in_game_and_pool()

    def test_t20_7_is_player_projected_to_win_game(self):
        self.__t20_game_in_progress_player_behind_in_game_and_pool()

    def test_t20_8_is_player_projected_to_win_game(self):
        self.__t20_game_in_progress_player_ahead_in_game_and_behind_in_pool()

    def test_t20_9_is_player_projected_to_win_game(self):
        self.__t20_game_in_progress_player_behind_in_game_and_ahead_in_pool()

    def test_t20_10_is_player_projected_to_win_game(self):
        self.__t20_game_not_started_player_ahead_in_game_and_pool()

    def test_t20_11_is_player_projected_to_win_game(self):
        self.__t20_game_not_started_player_behind_in_game_and_pool()

    def test_t20_12_is_player_projected_to_win_game(self):
        self.__t20_game_not_started_player_ahead_in_game_and_behind_in_pool()

    def test_t20_13_is_player_projected_to_win_game(self):
        self.__t20_game_not_started_player_behind_in_game_and_ahead_in_pool()

    def test_t21_is_player_possible_to_win_game(self):
        self.__t21_game_none()
        self.__t21_invalid_player()

    def test_t21_1_is_player_possible_to_win_game(self):
        self.__t21_player_pick_missing()

    def test_t21_2_is_player_possible_to_win_game(self):
        self.__t21_game_final_player_ahead_in_game_and_pool()

    def test_t21_3_is_player_possible_to_win_game(self):
        self.__t21_game_final_player_behind_in_game_and_pool()

    def test_t21_4_is_player_possible_to_win_game(self):
        self.__t21_game_final_player_ahead_in_game_and_behind_in_pool()

    def test_t21_5_is_player_possible_to_win_game(self):
        self.__t21_game_final_player_behind_in_game_and_ahead_in_pool()

    def test_t21_6_is_player_possible_to_win_game(self):
        self.__t21_game_in_progress_player_ahead_in_game_and_pool()

    def test_t21_7_is_player_possible_to_win_game(self):
        self.__t21_game_in_progress_player_behind_in_game_and_pool()

    def test_t21_8_is_player_possible_to_win_game(self):
        self.__t21_game_in_progress_player_ahead_in_game_and_behind_in_pool()

    def test_t21_9_is_player_possible_to_win_game(self):
        self.__t21_game_in_progress_player_behind_in_game_and_ahead_in_pool()

    def test_t21_10_is_player_possible_to_win_game(self):
        self.__t21_game_not_started_player_ahead_in_game_and_pool()

    def test_t21_11_is_player_possible_to_win_game(self):
        self.__t21_game_not_started_player_behind_in_game_and_pool()

    def test_t21_12_is_player_possible_to_win_game(self):
        self.__t21_game_not_started_player_ahead_in_game_and_behind_in_pool()

    def test_t21_13_is_player_possible_to_win_game(self):
        self.__t21_game_not_started_player_behind_in_game_and_ahead_in_pool()

    def test_t22_get_number_of_projected_wins(self):
        self.__t22_invalid_player_name()

    def test_t22_1_get_number_of_projected_wins(self):
        self.__t22_no_games_started()

    def test_t22_2_get_number_of_projected_wins(self):
        self.__t22_some_games_in_progress()

    def test_t22_3_get_number_of_projected_wins(self):
        self.__t22_mixed_game_states()

    def test_t22_4_get_number_of_projected_wins(self):
        self.__t22_all_games_final()

    def test_t22_5_get_number_of_projected_wins(self):
        self.__t22_player_with_no_picks()

    def test_t22_6_get_number_of_projected_wins(self):
        self.__t22_game_not_started_player_0_wins()

    def test_t22_7_get_number_of_projected_wins(self):
        self.__t22_game_not_started_player_10_wins()

    def test_t22_8_get_number_of_projected_wins(self):
        self.__t22_game_in_progress_player_0_wins()

    def test_t22_9_get_number_of_projected_wins(self):
        self.__t22_game_in_progress_player_10_wins()

    def test_t22_10_get_number_of_projected_wins(self):
        self.__t22_game_final_player_0_wins()

    def test_t22_11_get_number_of_projected_wins(self):
        self.__t22_game_final_player_10_wins()

    def test_t23_get_number_of_possible_wins(self):
        self.__t23_invalid_player()

    def test_t23_1_get_number_of_possible_wins(self):
        self.__t23_no_games_started()

    def test_t23_2_get_number_of_possible_wins(self):
        self.__t23_some_games_in_progress()

    def test_t23_3_get_number_of_possible_wins(self):
        self.__t23_mixed_game_states()

    def test_t23_4_get_number_of_possible_wins(self):
        self.__t23_all_games_final()

    def test_t23_5_get_number_of_possible_wins(self):
        self.__t23_player_with_no_picks()

    def test_t23_6_get_number_of_possible_wins(self):
        self.__t23_game_not_started_player_0_wins()

    def test_t23_7_get_number_of_possible_wins(self):
        self.__t23_game_not_started_player_10_wins()

    def test_t23_8_get_number_of_possible_wins(self):
        self.__t23_game_in_progress_player_0_wins()

    def test_t23_9_get_number_of_possible_wins(self):
        self.__t23_game_in_progress_player_10_wins()

    def test_t23_10_get_number_of_possible_wins(self):
        self.__t23_game_final_player_0_wins()

    def test_t23_11_get_number_of_possible_wins(self):
        self.__t23_game_final_player_10_wins()

    def test_t24_1_all_games_final(self):
        self.__t24_no_games_started()

    def test_t24_2_all_games_final(self):
        self.__t24_some_games_in_progress()

    def test_t24_3_all_games_final(self):
        self.__t24_mixed_game_states()

    def test_t24_4_all_games_final(self):
        self.__t24_all_games_final()

    def test_t25_1_no_games_started(self):
        self.__t25_no_games_started()

    def test_t25_2_no_games_started(self):
        self.__t25_some_games_in_progress()

    def test_t25_3_no_games_started(self):
        self.__t25_mixed_game_states()

    def test_t25_4_no_games_started(self):
        self.__t25_all_games_final()

    def test_t26_1_at_least_one_game_in_progress(self):
        self.__t26_no_games_started()

    def test_t26_2_at_least_one_game_in_progress(self):
        self.__t26_one_game_in_progress()

    def test_t26_3_at_least_one_game_in_progress(self):
        self.__t26_some_games_in_progress()

    def test_t26_4_at_least_one_game_in_progress(self):
        self.__t26_mixed_game_states()

    def test_t26_5_at_least_one_game_in_progress(self):
        self.__t26_all_games_final()

    def test_t27_1_get_summary_state_of_all_games(self):
        self.__t27_no_games_started()

    def test_t27_2_get_summary_state_of_all_games(self):
        self.__t27_one_game_in_progress()

    def test_t27_3_get_summary_state_of_all_games(self):
        self.__t27_some_games_in_progress()

    def test_t27_4_get_summary_state_of_all_games(self):
        self.__t27_mixed_game_states()

    def test_t27_5_get_summary_state_of_all_games(self):
        self.__t27_all_games_final()

    def test_t28_get_game_result_string(self):
        self.__t28_game_none()
        self.__t28_invalid_player()

    def test_t28_1_get_game_result_string(self):
        self.__t28_player_pick_missing()

    def test_t28_2_get_game_result_string(self):
        self.__t28_game_win()

    def test_t28_3_get_game_result_string(self):
        self.__t28_game_loss()

    def test_t28_4_get_game_result_string(self):
        self.__t28_game_ahead()

    def test_t28_5_get_game_result_string(self):
        self.__t28_game_behind()

    def test_t28_6_get_game_result_string(self):
        self.__t28_game_not_started()

    def test_t29_get_favored_team_name(self):
        self.__t29_game_none()
        self.__t29_team1_favored()
        self.__t29_team2_favored()

    def test_t29_1_get_favored_team_name(self):
        self.__t29_invalid_favored()

    def test_t30_get_game_score_spread(self):
        self.__t30_game_none()

    def test_t30_1_get_game_score_spread(self):
        self.__t30_game_not_started()

    def test_t30_2_get_game_score_spread(self):
        self.__t30_game_in_progress()

    def test_t30_3_get_game_score_spread(self):
        self.__t30_tied_score()

    def test_t30_4_get_game_score_spread(self):
        self.__t30_team1_ahead()

    def test_t30_5_get_game_score_spread(self):
        self.__t30_team2_ahead()

    def test_t31_get_pick_score_spread(self):
        self.__t31_pick_none()
        self.__t31_pick_team1_score_none()
        self.__t31_pick_team2_score_none()
        self.__t31_pick_team1_score_negative()
        self.__t31_pick_team2_score_negative()
        self.__t31_tied_score()
        self.__t31_team1_ahead()
        self.__t31_team2_ahead()

    def test_t32_0_get_featured_game(self):
        self.__t32_featured_game_missing()

    def test_t32_1_get_featured_game(self):
        self.__t32_featured_game()

    def test_t33_get_win_percent(self):
        self.__t33_invalid_player()

    def test_t33_1_get_win_percent(self):
        self.__t33_games_not_started()

    def test_t33_2_get_win_percent(self):
        self.__t33_games_in_progress()

    def test_t33_3_get_win_percent(self):
        self.__t33_games_mixed()

    def test_t33_4_get_win_percent(self):
        self.__t33_games_final()

    def test_t34_0_get_win_percent_string(self):
        self.__t34_invalid_player()

    def test_t34_1_get_win_percent_string(self):
        self.__t34_games_not_started()

    def test_t34_2_get_win_percent_string(self):
        self.__t34_games_in_progress()

    def test_t34_3_get_win_percent_string(self):
        self.__t34_games_mixed()

    def test_t34_4_get_win_percent_string(self):
        self.__t34_games_final()

    def test_t35_0_get_player_pick_for_game(self):
        self.__t35_game_none()

    def test_t35_1_get_player_pick_for_game(self):
        self.__t35_invalid_player()

    def test_t35_2_get_player_pick_for_game(self):
        self.__t35_game_invalid()

    def test_t35_3_get_player_pick_for_game(self):
        self.__t35_valid_player_pick()

    def test_t36_0_get_player_submit_time(self):
        self.__t36_invalid_player()

    def test_t36_1_get_player_submit_time(self):
        self.__t36_pick_created_entry_time()

    def test_t36_2_get_player_submit_time(self):
        self.__t36_pick_updated_entry_time()

    def test_t36_3_get_player_submit_time(self):
        self.__t36_week_lock_picks_not_specified()

    def test_t36_4_get_player_submit_time(self):
        self.__t36_submit_after_week_lock()

    def test_t36_5_get_player_submit_time(self):
        self.__t36_submit_before_week_lock()

    def test_t36_6_get_player_submit_time(self):
        self.__t36_submit_same_as_week_lock()

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
        valid_player = self.week1.get_player("holden_brent")
        with self.assertRaises(Exception):
            self.calc.is_player_losing_game(valid_player,None)

    def __t19_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        game = self.__get_a_valid_game()
        with self.assertRaises(Exception):
            self.calc.is_player_losing_game(bad_player,game)

    def __t19_game_not_started(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = NOT_STARTED

        self.__change_player_pick(player,game,TEAM1)
        self.assertFalse(self.calc.is_player_losing_game(player,game))

    def __t19_game_final(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = FINAL

        self.__change_player_pick(player,game,TEAM1)
        self.assertFalse(self.calc.is_player_losing_game(player,game))

    def __t19_player_pick_missing_game_not_started(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = NOT_STARTED

        self.__make_winner_missing(player,game)
        self.assertTrue(self.calc.is_player_losing_game(player,game))

    def __t19_player_pick_missing_game_in_progress(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = IN_PROGRESS

        self.__make_winner_missing(player,game)
        self.assertTrue(self.calc.is_player_losing_game(player,game))

    def __t19_player_pick_missing_game_final(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 25
        game.game_state = FINAL

        self.__make_winner_missing(player,game)
        self.assertFalse(self.calc.is_player_losing_game(player,game))

    def __t19_player_ahead_in_game_and_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM1)
        self.assertFalse(self.calc.is_player_losing_game(player,game))

    def __t19_player_behind_in_game_and_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 30
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_losing_game(player,game))

    def __t19_player_ahead_in_game_and_behind_in_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 5.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 25
        game.game_state = IN_PROGRESS
        
        self.__change_player_pick(player,game,TEAM2)
        self.assertTrue(self.calc.is_player_losing_game(player,game))

    def __t19_player_behind_in_game_and_ahead_in_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM1)
        self.assertFalse(self.calc.is_player_losing_game(player,game))

    def __t20_game_none(self):
        valid_player = self.week1.get_player("holden_brent")
        with self.assertRaises(Exception):
            self.calc.is_player_projected_to_win_game(valid_player,None)

    def __t20_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        game = self.__get_a_valid_game()
        with self.assertRaises(Exception):
            self.calc.is_player_projected_to_win_game(bad_player,game)

    def __t20_player_pick_missing(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 25
        game.game_state = IN_PROGRESS

        self.__make_winner_missing(player,game)
        self.assertFalse(self.calc.is_player_projected_to_win_game(player,game))

    def __t20_game_final_player_ahead_in_game_and_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = FINAL

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_projected_to_win_game(player,game))

    def __t20_game_final_player_behind_in_game_and_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 30
        game.game_state = FINAL

        self.__change_player_pick(player,game,TEAM1)
        self.assertFalse(self.calc.is_player_projected_to_win_game(player,game))

    def __t20_game_final_player_ahead_in_game_and_behind_in_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 5.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 25
        game.game_state = FINAL

        self.__change_player_pick(player,game,TEAM2)
        self.assertFalse(self.calc.is_player_projected_to_win_game(player,game))

    def __t20_game_final_player_behind_in_game_and_ahead_in_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = FINAL

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_projected_to_win_game(player,game))

    def __t20_game_in_progress_player_ahead_in_game_and_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_projected_to_win_game(player,game))

    def __t20_game_in_progress_player_behind_in_game_and_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 30
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM1)
        self.assertFalse(self.calc.is_player_projected_to_win_game(player,game))

    def __t20_game_in_progress_player_ahead_in_game_and_behind_in_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 5.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 25
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM2)
        self.assertFalse(self.calc.is_player_projected_to_win_game(player,game))

    def __t20_game_in_progress_player_behind_in_game_and_ahead_in_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_projected_to_win_game(player,game))

    def __t20_game_not_started_player_ahead_in_game_and_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = NOT_STARTED

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_projected_to_win_game(player,game))

    def __t20_game_not_started_player_behind_in_game_and_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 30
        game.game_state = NOT_STARTED

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_projected_to_win_game(player,game))

    def __t20_game_not_started_player_ahead_in_game_and_behind_in_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 5.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 25
        game.game_state = NOT_STARTED

        self.__change_player_pick(player,game,TEAM2)
        self.assertTrue(self.calc.is_player_projected_to_win_game(player,game))

    def __t20_game_not_started_player_behind_in_game_and_ahead_in_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = NOT_STARTED

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_projected_to_win_game(player,game))

    def __t21_game_none(self):
        valid_player = self.week1.get_player("holden_brent")
        with self.assertRaises(Exception):
            self.calc.is_player_possible_to_win_game(player,None)

    def __t21_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        game = self.__get_a_valid_game()
        with self.assertRaises(Exception):
            self.calc.is_player_possible_to_win_game(bad_player,game)

    def __t21_player_pick_missing(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 25
        game.game_state = IN_PROGRESS

        self.__make_winner_missing(player,game)
        self.assertFalse(self.calc.is_player_possible_to_win_game(player,game))

    def __t21_game_final_player_ahead_in_game_and_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = FINAL

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_possible_to_win_game(player,game))

    def __t21_game_final_player_behind_in_game_and_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 30
        game.game_state = FINAL

        self.__change_player_pick(player,game,TEAM1)
        self.assertFalse(self.calc.is_player_possible_to_win_game(player,game))

    def __t21_game_final_player_ahead_in_game_and_behind_in_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 5.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 25
        game.game_state = FINAL

        self.__change_player_pick(player,game,TEAM2)
        self.assertFalse(self.calc.is_player_possible_to_win_game(player,game))

    def __t21_game_final_player_behind_in_game_and_ahead_in_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = FINAL

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_possible_to_win_game(player,game))

    def __t21_game_in_progress_player_ahead_in_game_and_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_possible_to_win_game(player,game))

    def __t21_game_in_progress_player_behind_in_game_and_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 30
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_possible_to_win_game(player,game))

    def __t21_game_in_progress_player_ahead_in_game_and_behind_in_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 5.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 25
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM2)
        self.assertTrue(self.calc.is_player_possible_to_win_game(player,game))

    def __t21_game_in_progress_player_behind_in_game_and_ahead_in_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_possible_to_win_game(player,game))

    def __t21_game_not_started_player_ahead_in_game_and_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 25
        game.team2_actual_points = 10
        game.game_state = NOT_STARTED

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_possible_to_win_game(player,game))

    def __t21_game_not_started_player_behind_in_game_and_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 30
        game.game_state = NOT_STARTED

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_possible_to_win_game(player,game))

    def __t21_game_not_started_player_ahead_in_game_and_behind_in_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 5.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 25
        game.game_state = NOT_STARTED

        self.__change_player_pick(player,game,TEAM2)
        self.assertTrue(self.calc.is_player_possible_to_win_game(player,game))

    def __t21_game_not_started_player_behind_in_game_and_ahead_in_pool(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM2
        game.spread = 1.5
        game.team1_actual_points = 20 
        game.team2_actual_points = 21
        game.game_state = NOT_STARTED

        self.__change_player_pick(player,game,TEAM1)
        self.assertTrue(self.calc.is_player_possible_to_win_game(player,game))

    def __t22_invalid_player_name(self):
        bad_player = Player()
        bad_player.id = -1
        with self.assertRaises(Exception):
            self.calc.get_number_of_projected_wins(bad_player)

    def __t22_no_games_started(self):
        player = self.week1.get_player("holden_brent")
        self.__modify_game_states([NOT_STARTED]*10)
        self.assertEqual(self.calc.get_number_of_projected_wins(player),10)

    def __t22_some_games_in_progress(self):
        player = self.week1.get_player("holden_brent")
        num_projected_wins_last_7_games_2013_week_1 = 6

        states = [NOT_STARTED]*3 + [IN_PROGRESS]*7
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_projected_wins(player),num_projected_wins_last_7_games_2013_week_1)

    def __t22_mixed_game_states(self):
        num_projected_wins_first_3_games = 2
        num_projected_wins_next_3_games = 3
        num_projected_wins_last_4_games = 2
        num_projected_wins_2013_week_1 = num_projected_wins_first_3_games + num_projected_wins_next_3_games + num_projected_wins_last_4_games

        player = self.week1.get_player("holden_brent")

        states = [FINAL]*3 + [NOT_STARTED]*3 + [IN_PROGRESS]*4
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_projected_wins(player),num_projected_wins_2013_week_1)

    def __t22_all_games_final(self):
        player = self.week1.get_player("reams_byron")
        num_projected_wins_2013_week_1 = 6
        self.assertEqual(self.calc.get_number_of_projected_wins(player),num_projected_wins_2013_week_1)

    def __t22_player_with_no_picks(self):
        player = self.week1.get_player("holden_brent")
        self.__make_all_player_picks_not_entered(player)
        self.assertEqual(self.calc.get_number_of_projected_wins(player),0)

    def __t22_game_final_player_0_wins(self):
        player = self.week1.get_player("robbins_dale")
        self.__make_dale_0_wins()
        self.__modify_game_states([FINAL]*10)
        self.assertEqual(self.calc.get_number_of_projected_wins(player),0)

    def __t22_game_final_player_10_wins(self):
        player = self.week1.get_player("murphy_william")
        self.__make_william_10_wins()
        self.__modify_game_states([FINAL]*10)
        self.assertEqual(self.calc.get_number_of_projected_wins(player),10)

    def __t22_game_in_progress_player_0_wins(self):
        player = self.week1.get_player("robbins_dale")
        self.__make_dale_0_wins()
        self.__modify_game_states([IN_PROGRESS]*10)
        self.assertEqual(self.calc.get_number_of_projected_wins(player),0)

    def __t22_game_in_progress_player_10_wins(self):
        player = self.week1.get_player("murphy_william")
        self.__make_william_10_wins()
        self.__modify_game_states([IN_PROGRESS]*10)
        self.assertEqual(self.calc.get_number_of_projected_wins(player),10)

    def __t22_game_not_started_player_0_wins(self):
        player = self.week1.get_player("robbins_dale")
        self.__make_dale_0_wins()
        self.__modify_game_states([NOT_STARTED]*10)
        self.assertEqual(self.calc.get_number_of_projected_wins(player),10)

    def __t22_game_not_started_player_10_wins(self):
        player = self.week1.get_player("murphy_william")
        self.__make_william_10_wins()
        self.__modify_game_states([NOT_STARTED]*10)
        self.assertEqual(self.calc.get_number_of_projected_wins(player),10)

    def __t23_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        with self.assertRaises(Exception):
            self.calc.get_number_of_possible_wins(bad_player)

    def __t23_no_games_started(self):
        player = self.week1.get_player("holden_brent")
        self.__modify_game_states([NOT_STARTED]*10)
        self.assertEqual(self.calc.get_number_of_possible_wins(player),10)

    def __t23_some_games_in_progress(self):
        player = self.week1.get_player("holden_brent")
        states = [NOT_STARTED]*3 + [IN_PROGRESS]*7
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_possible_wins(player),10)

    def __t23_mixed_game_states(self):
        num_possible_wins_first_3_games = 2
        num_possible_wins_next_3_games = 3
        num_possible_wins_last_4_games = 4
        num_possible_wins_2013_week_1 = num_possible_wins_first_3_games + num_possible_wins_next_3_games + num_possible_wins_last_4_games

        player = self.week1.get_player("holden_brent")

        states = [FINAL]*3 + [NOT_STARTED]*3 + [IN_PROGRESS]*4
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_possible_wins(player),num_possible_wins_2013_week_1)

    def __t23_all_games_final(self):
        num_possible_wins_2013_week_1 = 6
        player = self.week1.get_player("reams_byron")
        self.assertEqual(self.calc.get_number_of_possible_wins(player),num_possible_wins_2013_week_1)

    def __t23_player_with_no_picks(self):
        player = self.week1.get_player("holden_brent")
        self.__make_all_player_picks_not_entered(player)
        self.assertEqual(self.calc.get_number_of_possible_wins(player),0)

    def __t23_game_final_player_0_wins(self):
        player = self.week1.get_player("robbins_dale")
        self.__make_dale_0_wins()
        self.__modify_game_states([FINAL]*10)
        self.assertEqual(self.calc.get_number_of_possible_wins(player),0)

    def __t23_game_final_player_10_wins(self):
        player = self.week1.get_player("murphy_william")
        self.__make_william_10_wins()
        self.__modify_game_states([FINAL]*10)
        self.assertEqual(self.calc.get_number_of_possible_wins(player),10)

    def __t23_game_in_progress_player_0_wins(self):
        player = self.week1.get_player("robbins_dale")
        self.__make_dale_0_wins()
        self.__modify_game_states([IN_PROGRESS]*10)
        self.assertEqual(self.calc.get_number_of_possible_wins(player),10)

    def __t23_game_in_progress_player_10_wins(self):
        player = self.week1.get_player("murphy_william")
        self.__make_william_10_wins()
        self.__modify_game_states([IN_PROGRESS]*10)
        self.assertEqual(self.calc.get_number_of_possible_wins(player),10)

    def __t23_game_not_started_player_0_wins(self):
        player = self.week1.get_player("robbins_dale")
        self.__make_dale_0_wins()
        self.__modify_game_states([NOT_STARTED]*10)
        self.assertEqual(self.calc.get_number_of_possible_wins(player),10)

    def __t23_game_not_started_player_10_wins(self):
        player = self.week1.get_player("murphy_william")
        self.__make_william_10_wins()
        self.__modify_game_states([NOT_STARTED]*10)
        self.assertEqual(self.calc.get_number_of_possible_wins(player),10)

    def __t24_no_games_started(self):
        self.__modify_game_states([NOT_STARTED]*10)
        self.assertFalse(self.calc.all_games_final())

    def __t24_some_games_in_progress(self):
        states = [NOT_STARTED]*3 + [IN_PROGRESS]*7
        self.__modify_game_states(states)
        self.assertFalse(self.calc.all_games_final())

    def __t24_mixed_game_states(self):
        states = [FINAL]*3 + [NOT_STARTED]*3 + [IN_PROGRESS]*4
        self.__modify_game_states(states)
        self.assertFalse(self.calc.all_games_final())

    def __t24_all_games_final(self):
        self.assertTrue(self.calc.all_games_final())

    def __t25_no_games_started(self):
        self.__modify_game_states([NOT_STARTED]*10)
        self.assertTrue(self.calc.no_games_started())

    def __t25_some_games_in_progress(self):
        states = [NOT_STARTED]*3 + [IN_PROGRESS]*7
        self.__modify_game_states(states)
        self.assertFalse(self.calc.no_games_started())

    def __t25_mixed_game_states(self):
        states = [FINAL]*3 + [NOT_STARTED]*3 + [IN_PROGRESS]*4
        self.__modify_game_states(states)
        self.assertFalse(self.calc.no_games_started())

    def __t25_all_games_final(self):
        self.assertFalse(self.calc.no_games_started())

    def __t26_no_games_started(self):
        self.__modify_game_states([NOT_STARTED]*10)
        self.assertFalse(self.calc.at_least_one_game_in_progress())

    def __t26_one_game_in_progress(self):
        states = [NOT_STARTED]*1 + [IN_PROGRESS]*9
        self.__modify_game_states(states)
        self.assertTrue(self.calc.at_least_one_game_in_progress())

    def __t26_some_games_in_progress(self):
        states = [NOT_STARTED]*3 + [IN_PROGRESS]*7
        self.__modify_game_states(states)
        self.assertTrue(self.calc.at_least_one_game_in_progress())

    def __t26_mixed_game_states(self):
        states = [FINAL]*3 + [NOT_STARTED]*3 + [IN_PROGRESS]*4
        self.__modify_game_states(states)
        self.assertTrue(self.calc.at_least_one_game_in_progress())

    def __t26_all_games_final(self):
        self.assertFalse(self.calc.at_least_one_game_in_progress())

    def __t27_no_games_started(self):
        self.__modify_game_states([NOT_STARTED]*10)
        self.assertEqual(self.calc.get_summary_state_of_all_games(),NOT_STARTED)

    def __t27_one_game_in_progress(self):
        states = [NOT_STARTED]*1 + [IN_PROGRESS]*9
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_summary_state_of_all_games(),IN_PROGRESS)

    def __t27_some_games_in_progress(self):
        states = [NOT_STARTED]*3 + [IN_PROGRESS]*7
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_summary_state_of_all_games(),IN_PROGRESS)

    def __t27_mixed_game_states(self):
        states = [FINAL]*3 + [NOT_STARTED]*3 + [IN_PROGRESS]*4
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_summary_state_of_all_games(),IN_PROGRESS)

    def __t27_all_games_final(self):
        self.assertEqual(self.calc.get_summary_state_of_all_games(),FINAL)

    def __t28_game_none(self):
        valid_player = self.week1.get_player("holden_brent")
        with self.assertRaises(Exception):
            self.calc.get_game_result_string(valid_player,None)

    def __t28_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        game = self.__get_a_valid_game()
        with self.assertRaises(Exception):
            self.calc.get_game_result_string(bad_player,game)

    def __t28_player_pick_missing(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 25
        game.game_state = IN_PROGRESS

        self.__make_winner_missing(player,game)
        self.assertEqual(self.calc.get_game_result_string(player,game),"loss")

    def __t28_game_win(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 25
        game.game_state = FINAL

        self.__change_player_pick(player,game,TEAM2)
        self.assertEqual(self.calc.get_game_result_string(player,game),"win")

    def __t28_game_loss(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 25
        game.game_state = FINAL

        self.__change_player_pick(player,game,TEAM1)
        self.assertEqual(self.calc.get_game_result_string(player,game),"loss")

    def __t28_game_ahead(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 25
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM2)
        self.assertEqual(self.calc.get_game_result_string(player,game),"ahead")

    def __t28_game_behind(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 25
        game.game_state = IN_PROGRESS

        self.__change_player_pick(player,game,TEAM1)
        self.assertEqual(self.calc.get_game_result_string(player,game),"behind")

    def __t28_game_not_started(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 25
        game.game_state = NOT_STARTED

        self.__change_player_pick(player,game,TEAM1)
        self.assertEqual(self.calc.get_game_result_string(player,game),"")

    def __t29_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_favored_team_name(None)

    def __t29_invalid_favored(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = 0

        with self.assertRaises(AssertionError):
            self.calc.get_favored_team_name(game)

    def __t29_team1_favored(self):
        game = self.__find_game("LSU","TCU")
        self.assertEqual(self.calc.get_favored_team_name(game),"LSU")

    def __t29_team2_favored(self):
        game = self.__find_game("North Carolina","South Carolina")
        self.assertEqual(self.calc.get_favored_team_name(game),"South Carolina")

    def __t30_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_game_score_spread(None)

    def __t30_game_not_started(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 25
        game.game_state = NOT_STARTED

        with self.assertRaises(Exception):
            self.calc.get_game_score_spread(game)

    def __t30_game_in_progress(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 10
        game.team2_actual_points = 25
        game.game_state = IN_PROGRESS

        self.assertEqual(self.calc.get_game_score_spread(game),15)

    def __t30_tied_score(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 13 
        game.team2_actual_points = 13
        game.game_state = FINAL

        self.assertEqual(self.calc.get_game_score_spread(game),0)

    def __t30_team1_ahead(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 24
        game.team2_actual_points = 11
        game.game_state = FINAL

        self.assertEqual(self.calc.get_game_score_spread(game),13)

    def __t30_team2_ahead(self):
        player = self.week1.get_player("holden_brent")

        game = self.__get_a_valid_game()
        game.favored = TEAM1
        game.spread = 5.5
        game.team1_actual_points = 9
        game.team2_actual_points = 31
        game.game_state = FINAL

        self.assertEqual(self.calc.get_game_score_spread(game),22)

    def __t31_pick_none(self):
        with self.assertRaises(Exception):
            self.calc.get_pick_score_spread(None)

    def __t31_pick_team1_score_none(self):
        pick = Pick()
        pick.team1_predicted_points = None
        pick.team2_predicted_points = 10
        with self.assertRaises(AssertionError):
            self.calc.get_pick_score_spread(pick)

    def __t31_pick_team2_score_none(self):
        pick = Pick()
        pick.team1_predicted_points = 10
        pick.team2_predicted_points = None
        with self.assertRaises(AssertionError):
            self.calc.get_pick_score_spread(pick)

    def __t31_pick_team1_score_negative(self):
        pick = Pick()
        pick.team1_predicted_points = None
        pick.team2_predicted_points = -1
        with self.assertRaises(AssertionError):
            self.calc.get_pick_score_spread(pick)

    def __t31_pick_team2_score_negative(self):
        pick = Pick()
        pick.team1_predicted_points = -1
        pick.team2_predicted_points = None
        with self.assertRaises(AssertionError):
            self.calc.get_pick_score_spread(pick)

    def __t31_tied_score(self):
        pick = Pick()
        pick.team1_predicted_points = 15 
        pick.team2_predicted_points = 15
        self.assertEqual(self.calc.get_pick_score_spread(pick),0)

    def __t31_team1_ahead(self):
        pick = Pick()
        pick.team1_predicted_points = 20 
        pick.team2_predicted_points = 11
        self.assertEqual(self.calc.get_pick_score_spread(pick),9)

    def __t31_team2_ahead(self):
        pick = Pick()
        pick.team1_predicted_points = 3
        pick.team2_predicted_points = 11
        self.assertEqual(self.calc.get_pick_score_spread(pick),8)

    def __t32_featured_game(self):
        game = self.calc.get_featured_game()
        self.assertEqual(game.gamenum,10)

    def __t32_featured_game_missing(self):
        featured_game = self.week1.games[10]
        del self.week1.games[10]
        self.week1.games[11] = featured_game
        self.week1.games[11].gamenum = 11

        with self.assertRaises(AssertionError):
            self.calc.get_featured_game()

    def __t33_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        with self.assertRaises(Exception):
            self.calc.get_win_percent(bad_player)

    def __t33_games_not_started(self):
        player = self.week1.get_player("holden_brent")
        self.__modify_game_states([NOT_STARTED]*10)
        self.assertEqual(self.calc.get_win_percent(player),0.00)

    def __t33_games_in_progress(self):
        player = self.week1.get_player("holden_brent")
        states = [IN_PROGRESS]*10
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_win_percent(player),0.00)

    def __t33_games_mixed(self):
        player = self.week1.get_player("holden_brent")
        states = [FINAL]*3 + [NOT_STARTED]*3 + [IN_PROGRESS]*4

        num_wins_in_first_3_games = 2
        num_games_final = 3
        expected_win_pct = float(num_wins_in_first_3_games) / float(num_games_final)

        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_win_percent(player),expected_win_pct)

    def __t33_games_final(self):
        player = self.week1.get_player("holden_brent")
        num_wins = 5
        num_games_final = 10 
        expected_win_pct = float(num_wins) / float(num_games_final)

        self.assertEqual(self.calc.get_win_percent(player),expected_win_pct)

    def __t34_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        with self.assertRaises(Exception):
            self.calc.get_win_percent_string(bad_player)

    def __t34_games_not_started(self):
        player = self.week1.get_player("holden_brent")
        self.__modify_game_states([NOT_STARTED]*10)
        self.assertEqual(self.calc.get_win_percent_string(player),"0.000")

    def __t34_games_in_progress(self):
        player = self.week1.get_player("holden_brent")
        states = [IN_PROGRESS]*10
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_win_percent_string(player),"0.000")

    def __t34_games_mixed(self):
        player = self.week1.get_player("holden_brent")
        states = [FINAL]*3 + [NOT_STARTED]*3 + [IN_PROGRESS]*4

        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_win_percent_string(player),"0.667")

    def __t34_games_final(self):
        player = self.week1.get_player("holden_brent")
        self.assertEqual(self.calc.get_win_percent_string(player),"0.500")

    def __t35_game_none(self):
        player = self.week1.get_player("holden_brent")
        with self.assertRaises(Exception):
            self.calc.get_player_pick_for_game(player,None)

    def __t35_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        game = self.__get_a_valid_game()
        with self.assertRaises(Exception):
            self.calc.get_player_pick_for_game(bad_player,game)

    def __t35_game_invalid(self):
        player = self.week1.get_player("holden_brent")
        invalid_game = self.__get_a_valid_game2()
        with self.assertRaises(Exception):
            self.calc.get_player_pick_for_game(player,invalid_game)

    def __t35_valid_player_pick(self):
        player = self.week1.get_player("holden_brent")
        game = self.__get_a_valid_game()
        pick = self.calc.get_player_pick_for_game(player,game)
        self.assertEqual(pick.game.id,game.id)

    def __t36_invalid_player(self):
        bad_player = Player()
        bad_player.id = -1
        with self.assertRaises(Exception):
            self.calc.get_player_submit_time(bad_player)

    def __t36_pick_created_entry_time(self):
        player = self.week1.get_player("holden_brent")
        games = self.week1.games
        self.__change_player_pick_time(player,games[1],created=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[2],created=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[3],created=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[4],created=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[5],created=dt.datetime(2013,8,11))
        self.__change_player_pick_time(player,games[6],created=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[7],created=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[8],created=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[9],created=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[10],created=dt.datetime(2013,8,10))
        self.assertEqual(self.calc.get_player_submit_time(player),dt.datetime(2013,8,11))

    def __t36_pick_updated_entry_time(self):
        player = self.week1.get_player("holden_brent")
        games = self.week1.games
        created_time=dt.datetime(2013,8,1)
        self.__change_player_pick_time(player,games[1],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[2],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[3],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[4],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[5],created=created_time,updated=dt.datetime(2013,8,11))
        self.__change_player_pick_time(player,games[6],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[7],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[8],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[9],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[10],created=created_time,updated=dt.datetime(2013,8,10))
        self.assertEqual(self.calc.get_player_submit_time(player),dt.datetime(2013,8,11))

    def __t36_week_lock_picks_not_specified(self):
        player = self.week1.get_player("holden_brent")
        games = self.week1.games
        week = self.week1.week
        week.lock_picks = None
        created_time=dt.datetime(2013,8,1)
        self.__change_player_pick_time(player,games[1],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[2],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[3],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[4],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[5],created=created_time,updated=dt.datetime(2013,8,11))
        self.__change_player_pick_time(player,games[6],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[7],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[8],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[9],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[10],created=created_time,updated=dt.datetime(2013,8,10))
        self.assertIsNone(self.calc.get_player_submit_time(player,week))

    def __t36_submit_after_week_lock(self):
        player = self.week1.get_player("holden_brent")
        games = self.week1.games
        week = self.week1.week
        week.lock_picks = dt.datetime(2013,8,10)
        created_time=dt.datetime(2013,8,1)
        self.__change_player_pick_time(player,games[1],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[2],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[3],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[4],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[5],created=created_time,updated=dt.datetime(2013,8,11))
        self.__change_player_pick_time(player,games[6],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[7],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[8],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[9],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[10],created=created_time,updated=dt.datetime(2013,8,10))
        self.assertIsNone(self.calc.get_player_submit_time(player,week))

    def __t36_submit_before_week_lock(self):
        player = self.week1.get_player("holden_brent")
        games = self.week1.games
        week = self.week1.week
        week.lock_picks = dt.datetime(2013,8,12)
        created_time=dt.datetime(2013,8,1)
        self.__change_player_pick_time(player,games[1],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[2],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[3],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[4],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[5],created=created_time,updated=dt.datetime(2013,8,11))
        self.__change_player_pick_time(player,games[6],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[7],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[8],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[9],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[10],created=created_time,updated=dt.datetime(2013,8,10))
        self.assertEqual(self.calc.get_player_submit_time(player,week),dt.datetime(2013,8,11))

    def __t36_submit_same_as_week_lock(self):
        player = self.week1.get_player("holden_brent")
        games = self.week1.games
        week = self.week1.week
        week.lock_picks = dt.datetime(2013,8,11)
        created_time=dt.datetime(2013,8,1)
        self.__change_player_pick_time(player,games[1],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[2],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[3],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[4],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[5],created=created_time,updated=dt.datetime(2013,8,11))
        self.__change_player_pick_time(player,games[6],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[7],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[8],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[9],created=created_time,updated=dt.datetime(2013,8,10))
        self.__change_player_pick_time(player,games[10],created=created_time,updated=dt.datetime(2013,8,10))
        self.assertEqual(self.calc.get_player_submit_time(player,week),dt.datetime(2013,8,11))

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

    def __change_player_pick_time(self,player,game,created=None,updated=None):
        assert created != None or updated != None,"At least one of the time fields should be specified"

        create_and_update = created != None and updated != None
        create_only = created != None and updated == None
        update_only = created == None and updated != None

        player_picks = self.week1.player_picks[player.id]
        for i,pick in enumerate(player_picks):
            if pick.game == game:
                if create_and_update:
                    self.week1.player_picks[player.id][i].created = created
                    self.week1.player_picks[player.id][i].updated = updated
                elif create_only:
                    self.week1.player_picks[player.id][i].created = created
                    self.week1.player_picks[player.id][i].updated = created
                elif update_only:
                    self.week1.player_picks[player.id][i].created = updated
                    self.week1.player_picks[player.id][i].updated = updated
