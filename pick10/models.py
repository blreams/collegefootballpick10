from django.db import models
from django.utils.timezone import now
#from utils import getLatestWeekNum

# Create your models here.

# We will use the django admin User model instead of creating a Player model
# Users can belong to groups that define their privileges, groups like
# 'pooler' and 'commissioner'.

## For now I'm going to start with only the Team model as it has no dependencies
## on other models.
class Team(models.Model):
    team_name = models.CharField(max_length=100)                            # Team name, 'South Carolina'
    mascot = models.CharField(max_length=100)                               # Team mascot, 'Gamecocks'
    #TODO Save helmet field for later.
    #helmet = models.ImageField()                                            # Helmet pic, local file (.png, .gif, .jpg)
    current = models.BooleanField(default=True)                             # True if team should be included in selection lists
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

class Game(models.Model):
    game_year = models.IntegerField(default=now().year)                     # Season year corresponding to this game
    #TODO default for game_week should call a function to figure out week number based on now()
    game_week = models.IntegerField(default=1)                              # Season week corresponding to this game
    game_num = models.IntegerField(default=0)                               # Game number within the week (ie. 1-10)
    team1 = models.ForeignKey('Team', related_name='team1')                 # Pointer back to Team entry
    team2 = models.ForeignKey('Team', related_name='team2')                 # Pointer back to Team entry
    team1_actual_points = models.IntegerField(default=-1)                   # Actual points scored 
    team2_actual_points = models.IntegerField(default=-1)                   # Actual points scored 
    favored = models.IntegerField(default=0)                                # Indicates which team is the favorite
    spread = models.IntegerField(default=0)                                 # Point spread added to underdog's score to determine winner
    game_state = models.IntegerField(default=0)                             # Enum (0=invalid, 1=not_started, 2=in_progress, 3=final)
    quarter = models.CharField(max_length=3, default='1st')                 # Used to indicate game progress ('1st', '2nd', '3rd', '4th', 'OT')
    time_left = models.CharField(max_length=10, default='15:00')            # Time left in the quarter (MM:SS)
    #kickoff_datetime = models.DateTimeField(default=getCurrentSaturday())   # Kickoff timestamp, no picks allowed after this time
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

#TODO Comment the rest of the models until later when we have UTs for them.
#class Week(models.Model):
#    week_year = models.IntegerField()                                       # Season year corresponding to this week
#    week_num = models.IntegerField()                                        # Week number within the season
#    #games = models.IntegerFields(default=10)                                # Number of games that make up the week
#    winner = models.ForeignKey('User')                                      # Link to User who won the week
#    lock_picks = models.BooleanField(default=False)                         # Once the first game kickoff occurs, update to True
#    lock_scores = models.BooleanField(default=False)                        # Once all scores have been submitted as final by admin, update to True
#    created = models.DateTimeField(auto_now=False, auto_now_add=True)
#    updated = models.DateTimeField(auto_now=True, auto_now_add=True)
#
#class Pick(models.Model):
#    pick_week = models.ForeignKey('Week')                                   # Link to week for which this pick applies
#    pick_user = models.ForeignKey('User')                                   # Link to user for which this pick applies
#    pick_game = models.ForeignKey('Game')                                   # Link to game for which this pick applies
#    game_winner = models.IntegerField(default=0)                            # Indicates which team won (1 or 2)
#    team1_predicted_points = models.IntegerField(default=-1)                # Points predicted for team (tie-break game)
#    team2_predicted_points = models.IntegerField(default=-1)                # Points predicted for team (tie-break game)
#    created = models.DateTimeField(auto_now=False, auto_now_add=True)
#    updated = models.DateTimeField(auto_now=True, auto_now_add=True)
#
