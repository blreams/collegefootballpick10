from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

import itertools
import random
try:
    from itertools import izip as zip
except ImportError:
    pass
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

import pytz
from datetime import datetime, timedelta

def create_a_kickoff_time(yearnum, weeknum, gamenum):
    """Given a year, week, game calculate an appropriate kickoff time
    with timezone.
    """
    # Start by getting noon Jan 1, year
    dt = datetime(yearnum, 1, 1, 12, 0, 0, 0, pytz.timezone('EST'))
    # Figure out the first Saturday
    if dt.isoweekday() == 6:
        days_to_add = 6
    else:
        days_to_add = 5 - dt.weekday()
    dt += timedelta(days=days_to_add)
    # Forward to week 35 + weeknum
    dt += timedelta(days=7*(34 + weeknum - 1))

    return dt + timedelta(hours=gamenum)

def calc_default_pick_deadline():
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

def get_pick_deadline(yearnum=0, weeknum=0):
    '''Returns a value for pick_deadline as follows:
        1. If the current year/week has any games with kickoffs assigned, use the earliest kickoff.
        2. If the current year/week has a pick_deadline, return that.
        3. Call calc_default_pick_deadline and return that.
    '''
    if not yearnum or not weeknum or yearnum not in get_yearlist() or weeknum not in get_weeklist(yearnum):
        return calc_default_pick_deadline()

    gameobjs = get_games(yearnum, weeknum)
    kickoffs = sorted([getattr(g, 'kickoff') for g in gameobjs if getattr(g, 'kickoff') is not None])
    if kickoffs:
        return kickoffs[0]

    weekobj = get_week(yearnum, weeknum)
    if weekobj and getattr(weekobj, 'pick_deadline'):
        return getattr(weekobj, 'pick_deadline')


@python_2_unicode_compatible
class Year(models.Model):
    yearnum = models.IntegerField()
    entry_fee = models.DecimalField(default=10.0, decimal_places=2, max_digits=6)
    payout_week = models.DecimalField(default=15.0, decimal_places=2, max_digits=6)
    payout_first = models.DecimalField(default=0.0, decimal_places=2, max_digits=7)
    payout_second = models.DecimalField(default=0.0, decimal_places=2, max_digits=7)
    payout_third = models.DecimalField(default=0.0, decimal_places=2, max_digits=7)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '1. Years'

    def __str__(self):
        return 'Year %d'%(self.yearnum,)

@python_2_unicode_compatible
class Player(models.Model):
    public_name = models.CharField(max_length=100, null=True, blank=True, default='')
    private_name = models.CharField(max_length=100, null=True, blank=True, default='')
    ss_name = models.CharField(max_length=100, null=True, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '2. Players'
        ordering = ('ss_name', 'private_name',)

    def __str__(self):
        return '%s/%s/%s'%(self.private_name, self.public_name, self.ss_name)

@python_2_unicode_compatible
class PlayerYear(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    year = models.ForeignKey('Year', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '3. PlayerYears'

    def __str__(self):
        return '%s:%s'%(self.player.private_name, self.year.yearnum,)

@python_2_unicode_compatible
class Conference(models.Model):
    conf_name = models.CharField(max_length=40)                            # Conference name, 'Southeastern'
    div_name = models.CharField(max_length=40, null=True, blank=True, default='')      # Division name, 'East'
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '4. Conferences'

    def __str__(self):
        return '%s %s'%(self.conf_name, self.div_name,)

@python_2_unicode_compatible
class Team(models.Model):
    team_name = models.CharField(max_length=40)                            # Team name, 'South Carolina'
    mascot = models.CharField(max_length=40)                               # Team mascot, 'Gamecocks'
    #TODO Save helmet field for later.
    #helmet = models.ImageField()                                          # Helmet pic, local file (.png, .gif, .jpg)
    conference = models.ForeignKey('Conference', default=None, on_delete=models.CASCADE)             # Pointer back to Conference entry
    current = models.BooleanField(default=True)                            # True if team should be included in selection lists
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '5. Teams'

    def __str__(self):
        return '%s %s'%(self.team_name, self.mascot,)

@python_2_unicode_compatible
class Week(models.Model):
    year = models.ForeignKey('Year', on_delete=models.CASCADE)                                        # Season year corresponding to this week
    weeknum = models.IntegerField()                                         # Week number within the season
    winner = models.ForeignKey(Player, null=True, blank=True, default=None, on_delete=models.CASCADE) # Link to Player who won the week
    pick_deadline = models.DateTimeField(null=True, blank=True)             # When generating a new Week, use get_default_pick_deadline()
    lock_picks = models.BooleanField(default=False)                         # Commissioner sets to False once games are finalized and picks can begin
    lock_scores = models.BooleanField(default=False)                        # Commissioner sets to True, after which only commissioner can update scores
    #created = models.DateTimeField(auto_now=False, auto_now_add=True)
    #updated = models.DateTimeField(auto_now=True, auto_now_add=True)
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField()

    def save(self, *args, **kwargs):
        '''On save, update timestamps'''
        rightnow = timezone.now()
        if not self.id:
            self.created = rightnow
        self.updated = rightnow
        return super(Week, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '6. Weeks'

    def __str__(self):
        return 'Year=%d, Week=%d'%(self.year.yearnum, self.weeknum,)

@python_2_unicode_compatible
class Game(models.Model):
    week = models.ForeignKey('Week', on_delete=models.CASCADE)                                        # Pointer back to Week entry
    gamenum = models.IntegerField(default=0)                                # Game number within the week (ie. 1-10)
    team1 = models.ForeignKey('Team', related_name='team1', on_delete=models.CASCADE)                 # Pointer back to Team entry
    team2 = models.ForeignKey('Team', related_name='team2', on_delete=models.CASCADE)                 # Pointer back to Team entry
    team1_actual_points = models.IntegerField(default=-1)                   # Actual points scored 
    team2_actual_points = models.IntegerField(default=-1)                   # Actual points scored 
    favored = models.IntegerField(default=0)                                # Indicates which team is the favorite
    spread = models.DecimalField(default=0.0, decimal_places=1, max_digits=4) # Point spread added to underdog's score to determine winner
    kickoff = models.DateTimeField(null=True, blank=True)                   # Kickoff date/time
    game_state = models.IntegerField(default=0)                             # Enum (0=invalid, 1=not_started, 2=in_progress, 3=final)
    quarter = models.CharField(max_length=3, default='')                    # Used to indicate game progress ('1st', '2nd', '3rd', '4th', 'OT')
    time_left = models.CharField(max_length=10, default='')                 # Time left in the quarter (MM:SS)
    winner = models.IntegerField(default=0)                                 # Winner according to spread
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '7. Games'

    def __str__(self):
        return 'Year=%d, Week=%d, Game=%d'%(self.week.year.yearnum, self.week.weeknum, self.gamenum,)

@python_2_unicode_compatible
class Pick(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)                                 # Link to player for which this pick applies
    game = models.ForeignKey('Game', on_delete=models.CASCADE)                                   # Link to game for which this pick applies
    winner = models.IntegerField(default=0)                            # Indicates which team was picked to win (1 or 2)
    team1_predicted_points = models.IntegerField(default=-1)           # Points predicted for team (tie-break game)
    team2_predicted_points = models.IntegerField(default=-1)           # Points predicted for team (tie-break game)
    submit_time = models.DateTimeField(null=True, blank=True)          # DateTime, must be set only when pick is posted.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '8. Picks'

    def __str__(self):
        return 'User=%s, Year=%d, Week=%d, Game=%d'%(self.player.private_name, self.game.week.year.yearnum, self.game.week.weeknum, self.game.gamenum,)

@python_2_unicode_compatible
class PlayerWeekStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    picks = models.IntegerField(default=0)
    winner = models.BooleanField(default=False)
    defaulter = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '9. PlayerWeekStats'

    def __str__(self):
        return 'Player={}, Year={}, Week={}'.format(self.player.ss_name, self.week.year.yearnum, self.week.weeknum)

@python_2_unicode_compatible
class UserProfile(models.Model):
    tz_choices = [(tz, tz) for tz in pytz.all_timezones if tz.startswith('US')] + [(tz, tz) for tz in pytz.all_timezones if not tz.startswith('US')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    player = models.OneToOneField('Player', blank=True, null=True, on_delete=models.CASCADE)
    company = models.CharField(max_length=50, blank=True)
    # You can customize this with whatever fields you want to extend User.
    favorite_team = models.CharField(max_length=100, blank=True, null=True)
    preferredtz = models.CharField(max_length=100, null=True, blank=True, choices=tz_choices, default='US/Eastern')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'User=%s, Player=%s' % (self.user.username, self.player,)

def add_year(yearnum):
    y, created = Year.objects.get_or_create(yearnum=yearnum)
    return y

#def add_player(public_name, private_name):
#    p = Player.objects.get_or_create(public_name=public_name, private_name=private_name)[0]
#    return p

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

def add_game(week, team1, team2, gamenum, favored=0, spread=0.0, kickoff=None, allowupdate=False):
    g, created = Game.objects.get_or_create(week=week, team1=team1, team2=team2, gamenum=gamenum)
    if not allowupdate:
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

def add_week(yearnum, weeknum, lock_picks=False):
    year = Year.objects.get(yearnum=yearnum)
    w, created = Week.objects.get_or_create(year=year, weeknum=weeknum)
    if created:
        w.pick_deadline = timezone.now()
        w.lock_picks = lock_picks
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

def get_player_by_private_name(private_name, index=0):
    players = Player.objects.filter(private_name=private_name)
    return players[index]

def get_player_by_ss_name(ss_name):
    p = Player.objects.get(ss_name=ss_name)
    return p

def get_player_by_id(player_id):
    p = Player.objects.get(id=player_id)
    return p

def get_player_id_list_by_year(yearnum):
    playeryears = PlayerYear.objects.filter(year__yearnum=yearnum).order_by('player__private_name')
    return [py.player.id for py in playeryears]

def get_user_by_username(username):
    u = User.objects.get(username=username)
    return u

def get_profile_by_user(user):
    try:
        userprofile = UserProfile.objects.get(user=user)
    except:
        return
    return userprofile

def get_profile_by_player(player):
    try:
        userprofile = UserProfile.objects.get(player=player)
    except:
        return
    return userprofile

def get_staff():
    return User.objects.filter(is_staff=True)

def get_team(team):
    t = Team.objects.get(team_name=team)
    return t

def get_game(yearnum, weeknum, gamenum):
    week = Week.objects.get(year__yearnum=yearnum, weeknum=weeknum)
    g = Game.objects.get(week=week, gamenum=gamenum)
    return g

def get_games(yearnum, weeknum):
    try:
        week = Week.objects.get(year__yearnum=yearnum, weeknum=weeknum)
    except DoesNotExist:
        return []
    return Game.objects.filter(week=week).order_by('gamenum')

def get_week(yearnum, weeknum):
    year = Year.objects.get(yearnum=yearnum)
    w = Week.objects.get(year=year, weeknum=weeknum)
    return w

def get_week_with_no_winner(yearnum):
    weekobjs = Week.objects.filter(year__yearnum=yearnum, lock_picks=False, winner=None).order_by('weeknum')
    if not weekobjs:
        return 0
    return weekobjs[0].weeknum

def get_last_week_with_winner(yearnum):
    weekobjs = Week.objects.filter(year__yearnum=yearnum, lock_picks=False).exclude(winner=None).order_by('weeknum')
    if not weekobjs:
        return 0
    return weekobjs[len(weekobjs) - 1].weeknum

def query_picks(username, yearnum, weeknum):
    user = get_user_by_username(username)
    player = user.userprofile.player
    picks = Pick.objects.filter(player=player, game__week__year__yearnum=yearnum, game__week__weeknum=weeknum).order_by('game__gamenum')
    return picks

def query_picks_by_player_id(player_id, yearnum, weeknum):
    player = get_player_by_id(player_id)
    picks = Pick.objects.filter(player=player, game__week__year__yearnum=yearnum, game__week__weeknum=weeknum).order_by('game__gamenum')
    return picks

def query_picks_week(yearnum, weeknum):
    picks = Pick.objects.filter(game__week__year__yearnum=yearnum, game__week__weeknum=weeknum)
    return picks

def get_yearlist():
    return sorted([y.yearnum for y in Year.objects.all()])

def get_weeklist(year, only_unlocked_picks=False, only_locked_scores=False):
    yearobj = Year.objects.filter(yearnum=year)[0]
    if only_locked_scores:
        return [w.weeknum for w in Week.objects.filter(year=yearobj, lock_scores=True).order_by('weeknum')]
    elif only_unlocked_picks:
        return [w.weeknum for w in Week.objects.filter(year=yearobj, lock_picks=False).order_by('weeknum')]
    else:
        return [w.weeknum for w in Week.objects.filter(year=yearobj).order_by('weeknum')]

def get_createweek_year_week():
    thisyear = timezone.now().year
    try:
        lastpoolyear = get_yearlist()[-1]
    except:
        return (thisyear, 1)
    try:
        latestweek = get_weeklist(lastpoolyear)[-1]
    except:
        return (thisyear, 1)
    if not query_picks_week(lastpoolyear, latestweek):
        return (lastpoolyear, latestweek)
    if latestweek == 13:
        return (thisyear, 1)
    else:
        return (lastpoolyear, latestweek + 1)

def get_teamlist():
    return sorted([t.team_name for t in Team.objects.all()])

def get_commish_can_post(yearnum, weeknum):
    if query_picks_week(yearnum, weeknum):
        return False
    return True

def get_week_info(yearnum, weeknum):
    weekfields = {}
    week = get_week(yearnum, weeknum)
    weekfields['pick_deadline'] = week.pick_deadline
    weekfields['lock_picks'] = week.lock_picks
    weekfields['lock_scores'] = week.lock_scores
    return weekfields

def get_games_info_for_week(yearnum, weeknum):
    gamefields = {}
    games = get_games(yearnum, weeknum)
    for game in games:
        gamestr = 'game%d_' % game.gamenum
        gamefields[gamestr + 'team1'] = game.team1.team_name
        gamefields[gamestr + 'team2'] = game.team2.team_name
        gamefields[gamestr + 'favored'] = game.favored
        gamefields[gamestr + 'spread'] = game.spread
        gamefields[gamestr + 'kickoff'] = game.kickoff
    return gamefields

def set_week_lock_picks(yearnum, weeknum, value):
    """Sets a value for Week.lock_picks.

    Returns:
      The value of Week.lock_picks when called.
    """
    w = get_week(yearnum, weeknum)
    lock_picks = w.lock_picks
    if lock_picks != value:
        w.lock_picks = value
        w.save()

def calc_completed_games(yearnum, weeknum=0):
    """Calculate number of complete games for the given yearnum, weeknum.
    yearnum is required. weeknum=0 means calculate for the entire year.
    """
    if weeknum == 0:
        weeknums = get_weeklist(yearnum)
    else:
        weeknums = [weeknum]

    completed_games = 0
    for weeknum in weeknums:
        games = get_games(yearnum, weeknum)
        for game in games:
            if game.game_state == 3:
                completed_games += 1
    return completed_games

def calc_picked_games(playerid, yearnum, weeknum=0):
    """Calculate number of picked games for the given playerid, yearnum,
    weeknum. weeknum=0 means calculate for the entire year.
    """
    if weeknum == 0:
        weeknums = get_weeklist(yearnum)
    else:
        weeknums = [weeknum]

    picked_games = 0
    for weeknum in weeknums:
        w = get_week(yearnum, weeknum)
        for game in Game.objects.filter(week=w).exclude(winner=0):
            picked_games += len(Pick.objects.filter(player__id=playerid, game=game).exclude(winner=0))

    return picked_games

def calc_weekly_points(yearnum, username_or_player_id=None, overunder=False):
    """Return list of cumulative points over/under, one per week, for the given year.
    Can query using username or player_id. If neither is given, it picks a random
    player.
    """
    scorelist = []
    if yearnum == 0:
        return ('', scorelist)
    if isinstance(username_or_player_id, six.string_types):
        user = get_user_by_username(username_or_player_id)
        if not user or not hasattr(user, 'userprofile') or not hasattr(user.userprofile, 'player') or user.userprofile.player is None:
            return ('', scorelist)
        player_id = user.userprofile.player.id
    elif username_or_player_id is not None:
        if not get_player_by_id(username_or_player_id):
            return ('', scorelist)
        player_id = username_or_player_id
    else:
        player_id = random.sample(set([pws.player.id for pws in PlayerWeekStat.objects.filter(week__year__yearnum=yearnum)]), 1)[0]
    player_name = get_player_by_id(player_id).private_name
    scorelist = [pws.score for pws in PlayerWeekStat.objects.filter(player__id=player_id, week__year__yearnum=yearnum).order_by('week__weeknum')]
    if overunder:
        cumulative = 0
        new_scorelist = []
        for score in scorelist:
            cumulative += score - 5
            new_scorelist.append(cumulative)
        scorelist = new_scorelist
    return (player_name, scorelist)

def calc_player_week_points_picks_winner(player_id, yearnum, weeknum):
    picks = query_picks_by_player_id(player_id, yearnum, weeknum)
    if len(picks) == 0:
        return [0, 0, False]
    week = Week.objects.get(year__yearnum=yearnum, weeknum=weeknum)
    if week.winner is not None:
        week_winner = week.winner.id == player_id
    else:
        week_winner = None
    picks_entered = 0
    points = 0
    games = get_games(yearnum, weeknum)
    for pick, game in zip(picks, games):
        if game.game_state == 3:
            picks_entered += 1
            if pick.winner == game.winner:
                points += 1
    return [points, picks_entered, week_winner]

def get_playeryears_by_id(player_id):
    playeryears = PlayerYear.objects.filter(player_id=player_id)
    return sorted([py.year.yearnum for py in playeryears], reverse=True)

def get_player_id_with_stats_list(yearnum, weeknum):
    playerweekstats = PlayerWeekStat.objects.filter(week__year__yearnum=yearnum, week__weeknum=weeknum)
    return [pws.player_id for pws in playerweekstats]

def update_player_stats(week):
    players = [py.player for py in PlayerYear.objects.filter(year__yearnum=week.year.yearnum)]
    for player in players:
        points, picks, winner = calc_player_week_points_picks_winner(player.id, week.year.yearnum, week.weeknum)
        if winner is None:
            print("Warning: Year {} Week {} has no winner".format(week.year.yearnum, week.weeknum))
            return
        pws, created = PlayerWeekStat.objects.get_or_create(player=player, week=week)
        pws.score = points
        pws.picks = picks
        pws.winner = winner
        pws.save()

