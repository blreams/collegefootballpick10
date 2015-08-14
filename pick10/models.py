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
    tz_choices = [(tz, tz) for tz in pytz.all_timezones if tz.startswith('US')] + [(tz, tz) for tz in pytz.all_timezones if not tz.startswith('US')]
    user = models.OneToOneField(User)
    player = models.OneToOneField('Player', blank=True, null=True)
    company = models.CharField(max_length=50, blank=True)
    # You can customize this with whatever fields you want to extend User.
    preferredtz = models.CharField(max_length=100, null=True, blank=True, choices=tz_choices, default='US/Eastern')
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return 'User=%s, Player=%s' % (self.user.username, self.player,)

class Year(models.Model):
    yearnum = models.IntegerField()
    entry_fee = models.DecimalField(default=10.0, decimal_places=2, max_digits=6)
    payout_week = models.DecimalField(default=15.0, decimal_places=2, max_digits=6)
    payout_first = models.DecimalField(default=0.0, decimal_places=2, max_digits=7)
    payout_second = models.DecimalField(default=0.0, decimal_places=2, max_digits=7)
    payout_third = models.DecimalField(default=0.0, decimal_places=2, max_digits=7)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = '1. Years'

    def __unicode__(self):
        return 'Year %d'%(self.yearnum,)

class Player(models.Model):
    public_name = models.CharField(max_length=100, null=True, blank=True, default='')
    private_name = models.CharField(max_length=100, null=True, blank=True, default='')
    ss_name = models.CharField(max_length=100, null=True, blank=True, default='')
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = '2. Players'

    def __unicode__(self):
        return '%s/%s/%s'%(self.private_name, self.public_name, self.ss_name)

class PlayerYear(models.Model):
    player = models.ForeignKey('Player')
    year = models.ForeignKey('Year')
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = '3. PlayerYears'

    def __unicode__(self):
        return '%s:%s'%(self.player.private_name, self.year.yearnum,)

class Conference(models.Model):
    conf_name = models.CharField(max_length=40)                            # Conference name, 'Southeastern'
    div_name = models.CharField(max_length=40, null=True, blank=True, default='')      # Division name, 'East'
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = '4. Conferences'

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
        verbose_name_plural = '5. Teams'

    def __unicode__(self):
        return '%s %s'%(self.team_name, self.mascot,)

class Week(models.Model):
    year = models.ForeignKey('Year')                                        # Season year corresponding to this week
    weeknum = models.IntegerField()                                         # Week number within the season
    winner = models.ForeignKey(Player, null=True, blank=True, default=None) # Link to Player who won the week
    lock_picks = models.DateTimeField(null=True, blank=True)                # When generating a new Week, use get_default_pick_deadline()
    lock_scores = models.BooleanField(default=False)                        # Commissioner sets to True, after which only commissioner can update scores
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = '6. Weeks'

    def __unicode__(self):
        return 'Year=%d, Week=%d'%(self.year.yearnum, self.weeknum,)

class Game(models.Model):
    week = models.ForeignKey('Week')                                        # Pointer back to Week entry
    gamenum = models.IntegerField(default=0)                                # Game number within the week (ie. 1-10)
    team1 = models.ForeignKey('Team', related_name='team1')                 # Pointer back to Team entry
    team2 = models.ForeignKey('Team', related_name='team2')                 # Pointer back to Team entry
    team1_actual_points = models.IntegerField(default=-1)                   # Actual points scored 
    team2_actual_points = models.IntegerField(default=-1)                   # Actual points scored 
    favored = models.IntegerField(default=0)                                # Indicates which team is the favorite
    spread = models.DecimalField(default=0.0, decimal_places=1, max_digits=4) # Point spread added to underdog's score to determine winner
    kickoff = models.DateTimeField(null=True, blank=True)                   # Kickoff date/time
    game_state = models.IntegerField(default=0)                             # Enum (0=invalid, 1=not_started, 2=in_progress, 3=final)
    quarter = models.CharField(max_length=3, default='')                    # Used to indicate game progress ('1st', '2nd', '3rd', '4th', 'OT')
    time_left = models.CharField(max_length=10, default='')                 # Time left in the quarter (MM:SS)
    winner = models.IntegerField(default=0)                                 # Winner according to spread
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = '7. Games'

    def __unicode__(self):
        return 'Year=%d, Week=%d, Game=%d'%(self.week.year.yearnum, self.week.weeknum, self.gamenum,)

class Pick(models.Model):
    player = models.ForeignKey(Player)                                 # Link to player for which this pick applies
    game = models.ForeignKey('Game')                                   # Link to game for which this pick applies
    winner = models.IntegerField(default=0)                            # Indicates which team was picked to win (1 or 2)
    team1_predicted_points = models.IntegerField(default=-1)           # Points predicted for team (tie-break game)
    team2_predicted_points = models.IntegerField(default=-1)           # Points predicted for team (tie-break game)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = '8. Picks'

    def __unicode__(self):
        return 'User=%s, Year=%d, Week=%d, Game=%d'%(self.player.private_name, self.game.week.year.yearnum, self.game.week.weeknum, self.game.gamenum,)

def add_player(public_name, private_name):
    p = Player.objects.get_or_create(public_name=public_name, private_name=private_name)[0]
    return p

def add_user(username, email, firstname, lastname):
    u, created = User.objects.get_or_create(username=username, email=email, first_name=firstname, last_name=lastname)
    if created:
        u.set_password(u.last_name)
        u.save()
    return u

def add_conference(conf_name, div_name=''):
    c = Conference.objects.get_or_create(conf_name=conf_name, div_name=div_name)[0]
    return c

def add_team(team_name, mascot, conference, current=True):
    t = Team.objects.get_or_create(team_name=team_name, mascot=mascot, conference=conference)[0]
    t.current = current
    t.save()
    return t

def add_game(week, team1, team2, gamenum, favored=0, spread=0.0, kickoff=None):
    g, created = Game.objects.get_or_create(week=week, team1=team1, team2=team2, gamenum=gamenum)
    assert created, "Something weird with add_game()..."
    g.favored = favored
    g.spread = spread
    if kickoff:
        g.kickoff = kickoff
    g.save()
    return g

def update_game(yearnum, weeknum, gamenum, team1_actual_points, team2_actual_points, game_state):
    games = Game.objects.filter(week__year__yearnum=yearnum, week__weeknum=weeknum, gamenum=gamenum)
    assert len(games) == 1, "Something weird with update_game()..."
    g = games[0]
    g.team1_actual_points = team1_actual_points
    g.team2_actual_points = team2_actual_points
    g.game_state = game_state
    g.save()

def add_week(yearnum, weeknum):
    year = Year.objects.get(yearnum=yearnum)
    w = Week.objects.get_or_create(year=year, weeknum=weeknum)[0]
    deadline = get_default_pick_deadline()
    w.lock_picks = deadline
    w.save()
    return w

def add_pick(player, game, winner, team1_predicted_points=-1, team2_predicted_points=-1):
    p = Pick.objects.get_or_create(player=player, game=game, winner=winner)[0]
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

def get_game(yearnum, weeknum, gamenum):
    week = Week.objects.get(year__yearnum=yearnum, weeknum=weeknum)
    g = Game.objects.get(week=week, gamenum=gamenum)
    return g

def get_week(yearnum, weeknum):
    year = Year.objects.get(yearnum=yearnum)
    w = Week.objects.get(year=year, weeknum=weeknum)
    return w

def query_picks(email, yearnum, weeknum):
    picks = Pick.objects.filter(pick_user__email=u, game__week__year__yearnum=yearnum, game__week__weeknum=weeknum).order_by('game__gamenum')
    return picks

