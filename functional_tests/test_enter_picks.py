from .base import FunctionalTest
from django.core.urlresolvers import reverse
from pick10.tests.unit_test_database import *
from pick10.models import *
from pick10.calculator import *
import unittest
from django.contrib.auth.models import User
from django.test.client import Client

class EnterPicksTest(FunctionalTest):

    def test_page_up(self):
        pass

    def test_wrong_player(self):
        pass

    def test_pick_team1(self):
        pass

    def test_pick_team2(self):
        pass

    def test_pick_score(self):
        pass

    def test_no_picks(self):
        pass

    def test_no_score(self):
        pass

    def test_bad_score(self):
        pass

    def test_cancel_button(self):
        pass

    def test_no_picks_yet(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,1)
        #self.__open_page(year=1978,week_number=1)

    def test_picks_already_made(self):
        pass

    def test_no_change_to_picks(self):
        pass

    def test_after_pick_deadline(self):
        pass

    def test_week_in_progress(self):
        pass

    def test_week_final(self):
        pass

    def test_GET_invalid_user(self):
        pass

    def test_GET_user_not_logged_in(self):
        pass

    def test_GET_invalid_year(self):
        pass

    def test_GET_invalid_week(self):
        pass

    def test_GET_invalid_player(self):
        pass

    def test_POST_invalid_user(self):
        pass

    def test_POST_user_not_logged_in(self):
        pass

    def test_POST_invalid_year(self):
        pass

    def test_POST_invalid_week(self):
        pass

    def test_POST_invalid_player(self):
        pass
