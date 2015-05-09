from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from pick10.views import home
from pick10.models import User, Conference, Team, Game, Week, Pick
from pick10.models import query_picks
from stage_models import populate_users, populate_conferences_teams
from stage_models import populate_games, populate_weeks, populate_picks

from unittest import skip

class BasicModelTest(TestCase):
    def setUp(self):
        users = User.objects.all()
        if len(users) == 0:
            populate_users()
            populate_conferences_teams()
            populate_games()
            populate_weeks()
            populate_picks()

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
        team = Team.objects.get(team_name='South Carolina')
        self.assertEqual(team.mascot, 'Gamecocks')
        self.assertEqual(team.conference.conf_name, 'Southeastern')

        teams = Team.objects.filter(current=False)
        self.assertEqual(teams.count(), 0)

    def test_save_to_game_model(self):
        games = Game.objects.all()
        self.assertGreaterEqual(len(games), 10)
        games = Game.objects.order_by('game_num').filter(game_year=2014, game_week=1)
        self.assertEqual(games[0].team1.team_name, 'South Carolina')
        self.assertEqual(games[0].team2.team_name, 'Texas A&M')
        self.assertEqual(games[9].team1.team_name, 'Clemson')
        self.assertEqual(games[9].team2.team_name, 'Georgia')

    def test_save_to_week_model(self):
        week1 = Week.objects.get(week_year=2014, week_num=1)
        self.assertEqual(week1.week_year, 2014)
        self.assertEqual(week1.week_num, 1)

    def test_save_pick_model(self):
        picks = query_picks('aaa@aaa.com', 2014, 1)
        self.assertEqual(len(picks), 10)
        self.assertEqual(picks[0].pick_game.team1.team_name, 'South Carolina')
        self.assertEqual(picks[0].pick_game.team2.team_name, 'Texas A&M')
        self.assertEqual(picks[9].pick_game.team1.team_name, 'Clemson')
        self.assertEqual(picks[9].pick_game.team2.team_name, 'Georgia')

