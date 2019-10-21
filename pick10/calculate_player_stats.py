from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

from django.core.cache import cache
from .models import get_playeryears_by_id, get_player_by_id, get_weeklist, PlayerWeekStat, Week, calc_player_week_points_picks_winner
from .player_results import PlayerResult, PlayerSummary
from .database import Database
from .calculator import CalculateResults
from .calculator import NOT_STARTED, IN_PROGRESS, FINAL

class Stat(object):
    def __init__(self):
        pass

class CalculatePlayerStats:

    def __init__(self,player_id,private_names=False):
        self.player_id = player_id
        self.summary = dict()
        self.stats = list()
        self.__use_private_names = private_names
        #self.__calculate_player_stats()

    def get_player_summary(self):
        self.playeryearnums = get_playeryears_by_id(self.player_id)
        self.summary['number_of_years'] = len(self.playeryearnums)
        self.player = get_player_by_id(self.player_id)
        self.summary['player_name'] = self.player.public_name
        if self.__use_private_names:
            self.summary['player_name'] = self.player.private_name
        self.summary['year_numbers'] = self.playeryearnums
        self.summary['total_points'] = 0
        self.summary['total_picks'] = 0
        self.summary['total_wins'] = 0
        self.summary['total_tens'] = 0
        self.summary['total_zeros'] = 0
        return self.summary

    def get_player_stats(self):
        self.__calculate_player_stats()
        self.summary['pick_pct'] = "{:.1f}%".format(100.0 * self.summary['total_points'] / self.summary['total_picks'])
        return self.stats

    def __calculate_player_stats(self):
        playerweekstats = PlayerWeekStat.objects.filter(player__id=self.player_id).order_by('week__weeknum').order_by('-week__year__yearnum')
        if len(playerweekstats) == 0:
            self.refresh_database()
            playerweekstats = PlayerWeekStat.objects.filter(player__id=self.player_id).order_by('week__weeknum').order_by('-week__year__yearnum')
        year = 10000
        week = 13
        for playerweekstat in playerweekstats:
            if playerweekstat.week.year.yearnum < year:
                # starting a new year
                try:
                    self.stats.append(stat)
                except:
                    pass
                stat = Stat()
                stat.year = playerweekstat.week.year.yearnum
                stat.total_score = 0
                year = stat.year
            stat_attr = 'week{}_score'.format(playerweekstat.week.weeknum)
            setattr(stat, stat_attr, playerweekstat.score)
            stat.total_score += getattr(stat, stat_attr)
            self.summary['total_points'] += playerweekstat.score
            self.summary['total_picks'] += playerweekstat.picks
            if playerweekstat.winner:
                self.summary['total_wins'] += 1
            if playerweekstat.score == 10:
                self.summary['total_tens'] += 1
            if playerweekstat.score == 0 and playerweekstat.picks != 0:
                self.summary['total_zeros'] += 1
        self.stats.append(stat)

    def refresh_database(self):
        for yearnum in get_playeryears_by_id(self.player.id):
            for weeknum in get_weeklist(yearnum, only_locked_scores=True):
                week = Week.objects.get(year__yearnum=yearnum, weeknum=weeknum)
                self.add_to_database(self.player, week)

    def add_to_database(self, player, week):
        points, picks, winner = calc_player_week_points_picks_winner(player.id, week.year.yearnum, week.weeknum)
        if winner is None:
            print("WARNING: Year {} Week {} has no winner".format(week.year.yearnum, week.weeknum))
            return
        pws, created = PlayerWeekStat.objects.get_or_create(player=player, week=week)
        pws.score = points
        pws.picks = picks
        pws.winner = winner
        print("Adding PlayerWeekStat({})".format(pws))
        pws.save()

