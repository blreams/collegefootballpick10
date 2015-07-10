from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape
from django.contrib.auth.models import User

from pick10.views import home
from pick10.models import Conference, Team, Game, Week, Pick, Player
from pick10.models import query_picks
from stage_history import main as shmain

from unittest import skip

class BasicModelTest(TestCase):
    def setUp(self):
        players = Player.objects.all()
        if len(players) == 0:
            # This will load the test database with data for 2 players, 1 week
            shmain(years=2014, playersperyear=2, weeks=1)

    def test_conference_model(self):
        confs = Conference.objects.all()
        self.assertEqual(confs.count(), 11)
        confs = Conference.objects.filter(conf_name='Southeastern')
        self.assertEqual(confs[0].conf_name, 'Southeastern')
        self.assertEqual(confs.count(), 2)
        confs = Conference.objects.filter(conf_name='Southeastern', div_name='East')
        self.assertEqual(confs.count(), 1)

    def test_team_model(self):
        teams = Team.objects.all()
        self.assertGreaterEqual(teams.count(), 20)
        team = Team.objects.get(team_name='South Carolina')
        self.assertEqual(team.mascot, 'Gamecocks')
        self.assertEqual(team.conference.conf_name, 'Southeastern')

        teams = Team.objects.filter(current=False)
        self.assertEqual(teams.count(), 0)

    def test_game_model(self):
        games = Game.objects.all()
        self.assertGreaterEqual(len(games), 10)
        games = Game.objects.order_by('gamenum').filter(week__year__yearnum=2014, week__weeknum=1)
        self.assertEqual(games[0].team1.team_name, 'Texas A&M')
        self.assertEqual(games[0].team2.team_name, 'South Carolina')
        self.assertEqual(games[9].team1.team_name, 'Clemson')
        self.assertEqual(games[9].team2.team_name, 'Georgia')

    def test_week_model(self):
        weeks = Week.objects.filter(year__yearnum=2014, weeknum=1)
        self.assertEqual(len(weeks), 1)
        week= weeks[0]
        self.assertEqual(week.year.yearnum, 2014)
        self.assertEqual(week.weeknum, 1)

    def test_pick_model(self):
        players = Player.objects.all()
        for player in players:
            picks = Pick.objects.filter(player__public_name=player.public_name, game__week__year__yearnum=2014, game__week__weeknum=1)
            self.assertEqual(len(picks), 10)

