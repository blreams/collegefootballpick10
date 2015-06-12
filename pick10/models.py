from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#from utils import getLatestWeekNum

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    company = models.CharField(max_length=50, blank=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Conference(models.Model):
    conf_name = models.CharField(max_length=40)                            # Conference name, 'Southeastern'
    div_name = models.CharField(max_length=40, null=True, blank=True)      # Division name, 'East'
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = '1. Conferences'

    def __unicode__(self):
        return '%s %s'%(self.conf_name, self.div_name,)

class Team(models.Model):
    team_name = models.CharField(max_length=40)                            # Team name, 'South Carolina'
    mascot = models.CharField(max_length=40)                               # Team mascot, 'Gamecocks'
    #TODO Save helmet field for later.
    #helmet = models.ImageField()                                          # Helmet pic, local file (.png, .gif, .jpg)
    conference = models.ForeignKey('Conference', default=None)             # Pointer back to Conference entry
    current = models.BooleanField(default=True)                            # True if team should be included in selection lists
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = '2. Teams'

    def __unicode__(self):
        return '%s %s'%(self.team_name, self.mascot,)

class Game(models.Model):
    game_year = models.IntegerField(default=timezone.now().year)            # Season year corresponding to this game
    #TODO default for game_week should call a function to figure out week number based on now()
    game_week = models.IntegerField(default=1)                              # Season week corresponding to this game
    game_num = models.IntegerField(default=0)                               # Game number within the week (ie. 1-10)
    team1 = models.ForeignKey('Team', related_name='team1')                 # Pointer back to Team entry
    team2 = models.ForeignKey('Team', related_name='team2')                 # Pointer back to Team entry
    team1_actual_points = models.IntegerField(default=-1)                   # Actual points scored 
    team2_actual_points = models.IntegerField(default=-1)                   # Actual points scored 
    favored = models.IntegerField(default=0)                                # Indicates which team is the favorite
    spread = models.FloatField(default=0.0)                                 # Point spread added to underdog's score to determine winner
    game_state = models.IntegerField(default=0)                             # Enum (0=invalid, 1=not_started, 2=in_progress, 3=final)
    quarter = models.CharField(max_length=3, default='1st')                 # Used to indicate game progress ('1st', '2nd', '3rd', '4th', 'OT')
    time_left = models.CharField(max_length=10, default='15:00')            # Time left in the quarter (MM:SS)
    #kickoff_datetime = models.DateTimeField(default=getCurrentSaturday())   # Kickoff timestamp, no picks allowed after this time
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = '3. Games'

    def __unicode__(self):
        return 'Year=%d, Week=%d, Game=%d'%(self.game_year, self.game_week, self.game_num,)

class Week(models.Model):
    week_year = models.IntegerField()                                       # Season year corresponding to this week
    week_num = models.IntegerField()                                        # Week number within the season
    #games = models.IntegerFields(default=10)                               # Number of games that make up the week
    winner = models.ForeignKey(User, null=True, blank=True, default=None)   # Link to User who won the week
    lock_picks = models.BooleanField(default=False)                         # Once the first game kickoff occurs, update to True
    lock_scores = models.BooleanField(default=False)                        # Once all scores have been submitted as final by admin, update to True
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = '4. Weeks'

    def __unicode__(self):
        return 'Year=%d, Week=%d'%(self.week_year, self.week_num,)

class Pick(models.Model):
    pick_week = models.ForeignKey('Week')                                   # Link to week for which this pick applies
    pick_user = models.ForeignKey(User)                                     # Link to user for which this pick applies
    pick_game = models.ForeignKey('Game')                                   # Link to game for which this pick applies
    game_winner = models.IntegerField(default=0)                            # Indicates which team won (1 or 2)
    team1_predicted_points = models.IntegerField(default=-1)                # Points predicted for team (tie-break game)
    team2_predicted_points = models.IntegerField(default=-1)                # Points predicted for team (tie-break game)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = '5. Picks'

    def __unicode__(self):
        return 'User=%s, Year=%d, Week=%d, Game=%d'%(self.pick_user.email, self.pick_game.game_year, self.pick_game.game_week, self.pick_game.game_num,)

def add_user(username, email, firstname, lastname):
    u, created = User.objects.get_or_create(username=username, email=email, first_name=firstname, last_name=lastname)
    if created:
        u.set_password(u.last_name)
        u.save()
    return u

def add_conference(conf_name, div_name=None):
    c = Conference.objects.get_or_create(conf_name=conf_name, div_name=div_name)[0]
    return c

def add_team(team_name, mascot, conference, current=True):
    t = Team.objects.get_or_create(team_name=team_name, mascot=mascot, conference=conference)[0]
    t.current = current
    t.save()
    return t

def add_game(team1, team2, game_year, game_week, game_num):
    g = Game.objects.get_or_create(team1=team1, team2=team2)[0]
    g.game_year = game_year
    g.game_week = game_week
    g.game_num = game_num
    g.save()
    return g

def add_week(week_year, week_num):
    w = Week.objects.get_or_create(week_year=week_year, week_num=week_num)[0]
    return w

def add_pick(pick_week, pick_user, pick_game, game_winner):
    p = Pick.objects.get_or_create(pick_week=pick_week, pick_user=pick_user, pick_game=pick_game)[0]
    p.game_winner = game_winner
    p.save()
    return p

def get_user_by_username(username):
    u = User.objects.get(username=username)
    return u

def get_user_by_email(email):
    u = User.objects.get(email=email)
    return u

def get_team(team):
    t = Team.objects.get(team_name=team)
    return t

def get_game(year, week, num):
    g = Game.objects.get(game_year=year, game_week=week, game_num=num)
    return g

def get_week(year, num):
    w = Week.objects.get(week_year=year, week_num=num)
    return w

def query_picks(email, year, week):
    u = get_user_by_email(email)
    w = get_week(year, week)
    picks = Pick.objects.filter(pick_user=u, pick_week=w).order_by('pick_game__game_num')
    return picks

