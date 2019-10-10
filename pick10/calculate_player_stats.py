from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

from django.core.cache import cache
from .models import get_playeryears_by_id, get_player_by_id, get_weeklist
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
        player = get_player_by_id(self.player_id)
        self.summary['player_name'] = player.public_name
        if self.__use_private_names:
            self.summary['player_name'] = player.private_name
        self.summary['year_numbers'] = self.playeryearnums

        return self.summary

    def get_player_stats(self):
        self.__calculate_player_stats()
        return self.stats

    def __calculate_player_stats(self):
        for year in self.summary['year_numbers']:
            stat = Stat()
            stat.year = year
            stat.total_score = 0
            for i in range(1, 14):
                stat_attr = 'week{}_score'.format(i)
                try:
                    setattr(stat, stat_attr, self.__calculate_player_score_for_week(year, i))
                    stat.total_score += getattr(stat, stat_attr)
                except:
                    setattr(stat, stat_attr, '')
            self.stats.append(stat)

    def __calculate_player_score_for_week(self, year, week):
        player_score_key = "{year},{week},{player_id}".format(year=year, week=week, player_id=self.player_id)
        player_score = cache.get(player_score_key)
        if player_score is None:
            database = Database()
            self.__week_data = database.load_week_data(year,week)
            self.__calc = CalculateResults(self.__week_data)

            assert self.player_id in self.__week_data.players,"Bad player id"
            self.__player = self.__week_data.players[self.player_id]
            player_score = self.__calc.get_number_of_wins(self.__player)
            #if database.is_week_scores_locked(year, week):
            #    cache.set(player_score_key, player_score) # do this only if week is complete
        return player_score

