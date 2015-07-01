from week_data import WeekData
from pick10.models import *

class Database:

    def load_week_data(self,year,week_number):
        data = WeekData()
        data.week = self.__get_week_in_database(year,week_number)
        data.games = self.__get_week_games_in_database(year,week_number)
        return data

    def put_games_week_in_database(self,games,week):
        raise AssertionError,"Not implemented"

    def is_year_valid(self,year,update=False):
        raise AssertionError,"Not implemented"

    def is_week_valid(self,week,year,update=False):
        raise AssertionError,"Not implemented"

    def before_pick_deadline(self,year,week_number,update=False):
        raise AssertionError,"Not implemented"

    def get_pick_deadline(self,year,week_number,update=False):
        raise AssertionError,"Not implemented"

    def get_next_year_week_for_create_week(self,update=False):
        raise AssertionError,"Not implemented"

    def get_week_numbers(self,year,update=False):
        raise AssertionError,"Not implemented"

    def get_years(self,update=False):
        raise AssertionError,"Not implemented"

    def get_pool_state(self,year,update=False):
        raise AssertionError,"Not implemented"

    def __get_week_state(self,week,update=False):
        raise AssertionError,"Not implemented"

    def load_weeks_and_years(self,update=False):
        raise AssertionError,"Not implemented"

    def load_players(self,year,update=False):
        raise AssertionError,"Not implemented"

    def delete_players_from_memcache(self,year):
        raise AssertionError,"Not implemented"

    def load_teams(self,key,update=False):
        raise AssertionError,"Not implemented"

    def load_week_data_timed(self,year,week_number,update=False):
        raise AssertionError,"Not implemented"

    def __get_week_in_database(self,year,week_number):
        return get_week(year,week_number)

    def __get_week_games_in_database(self,year,week_number):
        game_numbers = range(1,11)
        return { game_num:get_game(year,week_number,game_num) for game_num in game_numbers }

    def __get_player_week_picks_in_database(self,week,update):
        raise AssertionError,"Not implemented"

    def __get_week_picks_in_database(self,week,update):
        raise AssertionError,"Not implemented"

    def __load_week_numbers_and_years(self):
        raise AssertionError,"Not implemented"

    def __before_pick_deadline(self,week):
        raise AssertionError,"Not implemented"

    def update_games_cache(self,year,week_number,data):
        raise AssertionError,"Not implemented"

    def update_games(self,year,week_number):
        raise AssertionError,"Not implemented"

    def update_week_cache(self,year,week_number):
        raise AssertionError,"Not implemented"

    def add_team_to_memcache(self,team):
        raise AssertionError,"Not implemented"

    def delete_team_from_memcache(self,team):
        raise AssertionError,"Not implemented"



