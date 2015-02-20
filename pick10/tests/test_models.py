from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from pick10.views import home
from pick10.models import Team, Game

from unittest import skip

class ModelTeamTest(TestCase):
    def test_save_to_team_model(self):
        team1 = Team()
        team1.team_name = 'South Carolina'
        team1.mascot = 'Gamecocks'
        team1.current = True
        team1.save()

        team2 = Team()
        team2.team_name = 'Georgia Tech'
        team2.mascot = 'Yellow Jackets'
        team2.current = False
        team2.save()

        teams = Team.objects.all()
        self.assertEqual(teams.count(), 2)
        self.assertEqual(teams[0].team_name, 'South Carolina')
        self.assertEqual(teams[1].team_name, 'Georgia Tech')
        self.assertEqual(teams[0].mascot, 'Gamecocks')
        self.assertEqual(teams[1].mascot, 'Yellow Jackets')

        teams = Team.objects.filter(current=True)
        self.assertEqual(teams.count(), 1)
        self.assertEqual(teams[0].team_name, 'South Carolina')
        self.assertEqual(teams[0].mascot, 'Gamecocks')

    def test_save_to_game_model(self):
        team1 = Team()
        team1.team_name = 'South Carolina'
        team1.mascot = 'Gamecocks'
        team1.current = True
        team1.save()

        team2 = Team()
        team2.team_name = 'Georgia Tech'
        team2.mascot = 'Yellow Jackets'
        team2.current = False
        team2.save()

        game1 = Game()
        game1.team1 = team1
        game1.team2 = team2
        game1.save()

        games = Game.objects.all()
        self.assertEqual(games[0].team1.team_name, 'South Carolina')
        self.assertEqual(games[0].team2.team_name, 'Georgia Tech')

