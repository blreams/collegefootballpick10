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
        pass

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

    def test_invalid_user(self):
        pass

    def test_user_not_logged_in(self):
        pass
