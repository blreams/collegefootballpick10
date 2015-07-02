from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

import pytz
from datetime import datetime, timedelta

def get_default_pick_deadline():
    # The idea behind this is to grab the current day, then figure out the
    # next Thursday and use 4:00pm in the US/Eastern timezone.
    # Start with the current datetime
    naive_dt_now = datetime.now()
    # Figure out how many days to add to get to the next Thursday
    days_to_add = 3 - naive_dt_now.weekday()
    if days_to_add < 0:
        days_to_add += 7
    # Create a naive datetime corresponding to next Thursday at 4:00pm
    naive_dt_deadline = datetime(naive_dt_now.year, naive_dt_now.month, naive_dt_now.day, 16, 0, 0) + timedelta(days=days_to_add)
    # Localize it assuming US/Eastern time zone
    deadline = pytz.timezone('US/Eastern').localize(naive_dt_deadline)
    return deadline


class UserProfile(models.Model):
    tz_choices = [(tz, tz) for tz in pytz.all_timezones if tz.startswith('US')]
    user = models.OneToOneField(User)
    company = models.CharField(max_length=50, blank=True)
    # You can customize this with whatever fields you want to extend User.
    preferredtz = models.CharField(max_length=100, null=True, blank=True, choices=tz_choices)

class Player(models.Model):
    public_name = models.CharField(max_length=100, null=True, blank=True, default='')
    private_name = models.CharField(max_length=100, null=True, blank=True, default='')

    class Meta:
        verbose_name_plural = '0. Players'

    def __unicode__(self):
        return '%s/%s'%(self.private_name, self.public_name,)

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

class Week(models.Model):
    week_year = models.IntegerField()                                       # Season year corresponding to this week
    week_num = models.IntegerField()                                        # Week number within the season
    #games = models.IntegerFields(default=10)                               # Number of games that make up the week
    winner = models.ForeignKey(User, null=True, blank=True, default=None)   # Link to User who won the week
    lock_picks = models.DateTimeField(null=True, blank=True)                # When generating a new Week, use get_default_pick_deadline()
    lock_scores = models.BooleanField(default=False)                        # Once all scores are submitted as final by admin, update to True
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = '3. Weeks'

    def __unicode__(self):
        return 'Year=%d, Week=%d'%(self.week_year, self.week_num,)

class Game(models.Model):
    week = models.ForeignKey('Week')                                        # Pointer back to Week entry
    game_num = models.IntegerField(default=0)                               # Game number within the week (ie. 1-10)
    team1 = models.ForeignKey('Team', related_name='team1')                 # Pointer back to Team entry
    team2 = models.ForeignKey('Team', related_name='team2')                 # Pointer back to Team entry
    team1_actual_points = models.IntegerField(default=-1)                   # Actual points scored 
    team2_actual_points = models.IntegerField(default=-1)                   # Actual points scored 
    favored = models.IntegerField(default=0)                                # Indicates which team is the favorite
    spread = models.DecimalField(default=0.0, decimal_places=1, max_digits=4) # Point spread added to underdog's score to determine winner
    kickoff = models.DateTimeField(null=True, blank=True)                   # Kickoff date/time
    game_state = models.IntegerField(default=0)                             # Enum (0=invalid, 1=not_started, 2=in_progress, 3=final)
    quarter = models.CharField(max_length=3, default='1st')                 # Used to indicate game progress ('1st', '2nd', '3rd', '4th', 'OT')
    time_left = models.CharField(max_length=10, default='15:00')            # Time left in the quarter (MM:SS)
    #kickoff_datetime = models.DateTimeField(default=getCurrentSaturday())   # Kickoff timestamp, no picks allowed after this time
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = '4. Games'

    def __unicode__(self):
        return 'Year=%d, Week=%d, Game=%d'%(self.week.week_year, self.week.week_num, self.game_num,)

class Pick(models.Model):
    pick_player = models.ForeignKey(Player)                                 # Link to player for which this pick applies
    pick_game = models.ForeignKey('Game')                                   # Link to game for which this pick applies
    pick_winner = models.IntegerField(default=0)                            # Indicates which team was picked to win (1 or 2)
    team1_predicted_points = models.IntegerField(default=-1)                # Points predicted for team (tie-break game)
    team2_predicted_points = models.IntegerField(default=-1)                # Points predicted for team (tie-break game)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = '5. Picks'

    def __unicode__(self):
        return 'User=%s, Year=%d, Week=%d, Game=%d'%(self.pick_player.private_name, self.pick_game.week.week_year, self.pick_game.week.week_num, self.pick_game.game_num,)

def add_player(public_name, private_name):
    p = Player.objects.get_or_create(public_name=public_name, private_name=private_name)[0]
    return p

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

def add_game(week, team1, team2, game_num, favored=0, spread=0.0, kickoff=None):
    g, created = Game.objects.get_or_create(week=week, team1=team1, team2=team2, game_num=game_num)
    assert created, "Something weird with add_game()..."
    g.favored = favored
    g.spread = spread
    if kickoff:
        g.kickoff = kickoff
    g.save()
    return g

def update_game(yearnum, weeknum, gamenum, team1_actual_points, team2_actual_points, game_state):
    games = Game.objects.filter(week__week_year=yearnum, week__week_num=weeknum, game_num=gamenum)
    assert len(games) == 1, "Something weird with update_game()..."
    g = games[0]
    g.team1_actual_points = team1_actual_points
    g.team2_actual_points = team2_actual_points
    g.game_state = game_state
    g.save()

def add_week(week_year, week_num):
    w = Week.objects.get_or_create(week_year=week_year, week_num=week_num)[0]
    deadline = get_default_pick_deadline()
    w.lock_picks = deadline
    w.save()
    return w

def add_pick(pick_player, pick_game, pick_winner, team1_predicted_points=-1, team2_predicted_points=-1):
    p = Pick.objects.get_or_create(pick_player=pick_player, pick_game=pick_game, pick_winner=pick_winner)[0]
    if team1_predicted_points != -1:
        p.team1_predicted_points = team1_predicted_points
    if team2_predicted_points != -1:
        p.team2_predicted_points = team2_predicted_points
    p.save()
    return p

def get_player_by_public_name(public_name):
    p = Player.objects.get(public_name=public_name)
    return p

def get_player_by_private_name(private_name):
    p = Player.objects.get(private_name=private_name)
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
    g = Game.objects.get(week__week_year=year, week__week_num=week, game_num=num)
    return g

def get_week(year, num):
    w = Week.objects.get(week_year=year, week_num=num)
    return w

def query_picks(email, year, week):
    picks = Pick.objects.filter(pick_user__email=u, pick_game__week__week_year=year, pick_game__week__week_num=week).order_by('pick_game__game_num')
    return picks

