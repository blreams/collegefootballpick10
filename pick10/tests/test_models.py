from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from pick10.views import home
from pick10.models import User, Conference, Team, Game, Week, Pick
from pick10.models import add_conference, add_team
from stage_models import populate_conferences_teams

from unittest import skip

class BasicModelTest(TestCase):
    def setUp(self):
        conferences = Conference.objects.all()
        if len(conferences) == 0:
            populate_conferences_teams()

    def test_save_to_conference_model(self):
        confs = Conference.objects.all()
        self.assertGreaterEqual(confs.count(), 10)
        confs = Conference.objects.filter(conf_name='Southeastern')
        self.assertEqual(confs[0].conf_name, 'Southeastern')
        self.assertEqual(confs.count(), 2)
        confs = Conference.objects.filter(conf_name='Southeastern', div_name='East')
        self.assertEqual(confs.count(), 1)

    def test_save_to_team_model(self):
        teams = Team.objects.all()
        self.assertGreaterEqual(teams.count(), 120)
        teams = Team.objects.filter(team_name='South Carolina')
        self.assertEqual(teams.count(), 1)
        self.assertEqual(teams[0].mascot, 'Gamecocks')
        self.assertEqual(teams[0].conference.conf_name, 'Southeastern')

        teams = Team.objects.filter(current=False)
        self.assertEqual(teams.count(), 0)

    def test_save_to_game_model(self):
        game1 = Game()
        game1.team1 = Team.objects.filter(team_name='South Carolina')[0]
        game1.team2 = Team.objects.filter(team_name='Clemson')[0]
        game1.save()

        games = Game.objects.all()
        self.assertEqual(games[0].team1.team_name, 'South Carolina')
        self.assertEqual(games[0].team2.team_name, 'Clemson')

    def test_save_to_week_model(self):
        user1 = User()
        user1.email = 'aaa@bbb.com'
        user1.save()

        week1 = Week()
        week1.week_year = 2014
        week1.week_num = 1
        week1.winner = user1
        week1.save()

        weeks = Week.objects.all()
        self.assertEqual(weeks[0].week_year, 2014)
        self.assertEqual(weeks[0].week_num, 1)
        self.assertEqual(weeks[0].winner.email, 'aaa@bbb.com')

    def test_save_pick_model(self):
        user1 = User()
        user1.email = 'aaa@bbb.com'
        user1.save()

        week1 = Week()
        week1.week_year = 2014
        week1.week_num = 1
        week1.winner = user1
        week1.save()

        game1 = Game()
        game1.team1 = Team.objects.filter(team_name='South Carolina')[0]
        game1.team2 = Team.objects.filter(team_name='Clemson')[0]
        game1.save()

        pick1 = Pick()
        pick1.pick_week = week1
        pick1.pick_user = user1
        pick1.pick_game = game1
        pick1.save()

        picks = Pick.objects.all()
        self.assertEqual(picks[0].pick_week.week_year, 2014)
        self.assertEqual(picks[0].pick_user.email, 'aaa@bbb.com')
        self.assertEqual(picks[0].pick_game.team1.team_name, 'South Carolina')
        self.assertEqual(picks[0].pick_game.team2.team_name, 'Clemson')
        self.assertEqual(picks[0].game_winner, 0)
        self.assertEqual(picks[0].team1_predicted_points, -1)
        self.assertEqual(picks[0].team2_predicted_points, -1)

