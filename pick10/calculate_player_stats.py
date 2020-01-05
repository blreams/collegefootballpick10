from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

from django.core.cache import cache
from .models import Week, PlayerWeekStat
from .models import get_playeryears_by_id, get_player_by_id, get_weeklist, calc_player_week_points_picks_winner_defaulter, get_last_week_with_winner
from .player_results import PlayerResult, PlayerSummary
from .database import Database
from .calculator import CalculateResults
from .calculator import NOT_STARTED, IN_PROGRESS, FINAL

def get_decoration(score, winner, defaulter):
    if not winner and not defaulter:
        if   score == 10: decoration = 'p_content_grn5'
        elif score ==  9: decoration = 'p_content_grn4'
        elif score ==  8: decoration = 'p_content_grn3'
        elif score ==  7: decoration = 'p_content_grn2'
        elif score ==  6: decoration = 'p_content_grn1'
        elif score ==  5: decoration = 'p_content'
        elif score ==  4: decoration = 'p_content_red1'
        elif score ==  3: decoration = 'p_content_red2'
        elif score ==  2: decoration = 'p_content_red3'
        elif score ==  1: decoration = 'p_content_red4'
        elif score ==  0: decoration = 'p_content_red5'
    elif winner:
        decoration = 'p_winner'
    elif defaulter:
        decoration = 'p_defaulter'
    return decoration

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
        self.summary['number_of_weeks'] = 0
        for yearnum in self.playeryearnums:
            self.summary['number_of_weeks'] += get_last_week_with_winner(yearnum)
        self.player = get_player_by_id(self.player_id)
        self.summary['player_name'] = self.player.public_name
        if self.__use_private_names:
            self.summary['player_name'] = self.player.private_name
        self.summary['year_numbers'] = self.playeryearnums
        self.summary['total_points'] = 0
        self.summary['earned_points'] = 0
        self.summary['total_picks'] = 0
        self.summary['earned_picks'] = 0
        self.summary['total_wins'] = 0
        self.summary['total_tens'] = 0
        self.summary['total_zeros'] = 0
        self.summary['histo'] = [0] * 11
        return self.summary

    def get_player_stats(self):
        self.__calculate_player_stats()
        self.summary['pick_pct'] = "{:.1f}%".format(100.0 * self.summary['earned_points'] / self.summary['earned_picks'])
        return self.stats

    def __calculate_player_stats(self):
        playerweekstats = PlayerWeekStat.objects.filter(player__id=self.player_id).order_by('week__weeknum').order_by('-week__year__yearnum')
        if len(playerweekstats) < self.summary['number_of_weeks']:
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
                stat.earned_score = 0
                stat.min_score = playerweekstat.score
                stat.max_score = playerweekstat.score
                year = stat.year
            if stat.min_score > playerweekstat.score: stat.min_score = playerweekstat.score
            if stat.max_score < playerweekstat.score: stat.max_score = playerweekstat.score
            stat_attr = 'week{}_score'.format(playerweekstat.week.weeknum)
            setattr(stat, stat_attr, playerweekstat.score)
            stat_decoration = 'week{}_decoration'.format(playerweekstat.week.weeknum)
            setattr(stat, stat_decoration, get_decoration(playerweekstat.score, playerweekstat.winner, playerweekstat.defaulter))
            #stat.total_score += getattr(stat, stat_attr)
            stat.total_score += playerweekstat.score
            if not playerweekstat.defaulter:
                stat.earned_score += playerweekstat.score
                self.summary['earned_points'] += playerweekstat.score
                self.summary['earned_picks'] += playerweekstat.picks
            self.summary['total_points'] += playerweekstat.score
            self.summary['histo'][playerweekstat.score] += 1
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
        points, picks, winner, defaulter = calc_player_week_points_picks_winner_defaulter(player.id, week.year.yearnum, week.weeknum)
        if winner is None:
            print("WARNING: Year {} Week {} has no winner".format(week.year.yearnum, week.weeknum))
            return
        pws, created = PlayerWeekStat.objects.get_or_create(player=player, week=week)
        pws.score = points
        pws.picks = picks
        pws.winner = winner
        pws.defaulter = defaulter
        pws.save()

