from django.test import TestCase

class CalculateWeekResultsTests(TestCase):

    def test_week_results_against_expected_data(self):
        pass

    def test_t1_week_not_started(self):
        return
        self.__t1_week_not_started()
        self.__t1_week_not_started_with_defaulters()

    def test_t2_assign_rank(self):
        return
        self.__t2_win_loss_all_different()
        self.__t2_week_not_started()
        self.__t2_week_not_started_with_defaulters()
        self.__t2_week_not_started_with_some_missing_picks()
        self.__t2_win_loss_with_ties()
        self.__t2_win_loss_with_ties_less_than_10_games_complete()
        self.__t2_win_loss_with_first_place_ties()
        self.__t2_win_loss_with_first_place_ties_and_winner_specified()
        self.__t2_winner_missing()
        self.__t2_winner_insane()

    def test_t3_assign_projected_rank(self):
        return
        self.__t3_wins_all_different()
        self.__t3_week_not_started()
        self.__t3_week_not_started_with_defaulters()
        self.__t3_week_not_started_with_some_missing_picks()
        self.__t3_wins_with_ties()
        self.__t3_less_than_10_wins()
        self.__t3_all_wins_0()
        self.__t3_first_place_ties()
        self.__t3_winner_specified()
        self.__t3_first_place_tie_with_winner_specified()
        self.__t3_winner_missing()
        self.__t3_winner_insane()

    def test_t4_get_week_results_week_in_progress(self):
        return
        self.__t4_week_in_progress()
        self.__t4_week_in_progress_with_games_in_progress()

    def test_t5_get_week_state(self):
        return
        self.__t5_week_not_started()
        self.__t5_week_in_progress()
        self.__t5_week_final()
