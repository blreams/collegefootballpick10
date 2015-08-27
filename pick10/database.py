from week_data import WeekData
from pick10.models import *
import datetime
from calculator import *

class Database:

    def load_week_data(self,year,week_number):
        data = WeekData()
        data.week = self.__get_week_in_database(year,week_number)
        data.games = self.__get_week_games_in_database_indexed_by_game_number(year,week_number)
        data.games_id = self.__get_week_games_in_database_indexed_by_id(year,week_number)
        data.picks = self.__get_week_picks_in_database(data.week)
        data.player_picks = self.__get_player_week_picks_in_database(data.picks)
        data.players = self.load_players(year)
        data.teams = self.load_teams()
        return data

    def put_games_week_in_database(self,games,week):
        raise AssertionError,"Not implemented"

    def is_year_valid(self,year):
        weeks_and_years = self.load_weeks_and_years()
        return year in weeks_and_years

    def is_week_valid(self,week,year,update=False):
        raise AssertionError,"Not implemented"

    def is_week_scores_locked(self,year,week_number):
        week = self.__get_week_in_database(year,week_number)
        return week.lock_scores

    def are_picks_locked(self,year,week_number):
        week = self.__get_week_in_database(year,week_number)
        return week.lock_picks

    def before_pick_deadline(self,year,week_number):
        # TODO tests
        week = self.__get_week_in_database(year,week_number)
        return self.__before_pick_deadline(week)

    def after_pick_deadline(self,year,week_number):
        # TODO tests
        week = self.__get_week_in_database(year,week_number)
        return self.__after_pick_deadline(week)

    def get_pick_deadline(self,year,week_number):
        # TODO tests
        week = self.__get_week_in_database(year,week_number)
        return week.pick_deadline

    def get_next_year_week_for_create_week(self,update=False):
        raise AssertionError,"Not implemented"

    def get_week_numbers(self,year):
        weeks_and_years = self.load_weeks_and_years()
        return sorted(weeks_and_years[year])

    def get_years(self):
        weeks_and_years = self.load_weeks_and_years()
        return sorted(weeks_and_years.keys())

    def get_pool_state(self,year):
        if not(self.is_year_valid(year)):
            return "invalid"

        week_numbers = self.get_week_numbers(year)
        last_week_number = week_numbers[-1]

        week = self.__get_week_in_database(year,week_number=last_week_number)
        week_has_no_games = self.__week_has_no_games(year,last_week_number)

        only_week_one_exists = last_week_number == 1 and len(week_numbers) == 1

        if only_week_one_exists and week_has_no_games:
            return "not_started"

        assert not(week_has_no_games),"Every week should have games except for a week 1 exception"

        if self.__before_pick_deadline(week):
            return "enter_picks"

        week_state = self.__get_week_state(year,last_week_number)

        if last_week_number == 13 and week_state == FINAL:
            return "end_of_year"

        if week_state == NOT_STARTED:
            return "week_not_started"
        elif week_state == IN_PROGRESS:
            return "week_in_progress"
        elif week_state == FINAL:
            return "week_final"

    def get_week_state(self,year,week_number):
        return self.__get_week_state(year,week_number)

    def __get_week_state(self,year,week_number):
        week_data = WeekData()
        week_data.games = self.__get_week_games_in_database_indexed_by_game_number(year,week_number)
        calc = CalculateResults(week_data)
        return calc.get_summary_state_of_all_games()

    def load_weeks_and_years(self):
        weeks_and_years = self.__load_week_numbers_and_years()
        return weeks_and_years

    def load_players(self,year):
        year_obj = Year.objects.get(yearnum=year)
        players_year = PlayerYear.objects.filter(year=year_obj)
        players = { p.player.id:p.player for p in players_year }
        return players

    def delete_players_from_memcache(self,year):
        raise AssertionError,"Not implemented"

    def load_teams(self):
        teams = Team.objects.all()
        return { t.team_name:t for t in teams }

    def load_week_data_timed(self,year,week_number,update=False):
        raise AssertionError,"Not implemented"

    def __get_week_in_database(self,year,week_number):
        return get_week(year,week_number)

    def __get_week_games_in_database_indexed_by_id(self,year,week_number):
        game_numbers = range(1,11)
        week_games = dict()
        for game_num in game_numbers:
            game = get_game(year,week_number,game_num)
            week_games[game.id] = game
        return week_games

    def __get_week_games_in_database_indexed_by_game_number(self,year,week_number):
        game_numbers = range(1,11)
        return { game_num:get_game(year,week_number,game_num) for game_num in game_numbers }

    def __get_player_week_picks_in_database(self,week_picks):
        player_picks = dict()
        for pick in week_picks.values():
            player_id = pick.player.id
            if player_id not in player_picks:
                player_picks[player_id] = [pick]
            else:
                player_picks[player_id].append(pick)
        return player_picks

    def __get_week_picks_in_database(self,week):
        picks = Pick.objects.filter(game__week=week)
        return { p.id:p for p in picks }

    def __load_week_numbers_and_years(self):
        week_numbers_and_years = dict()
        weeks = Week.objects.all()

        for week in weeks:
            year = week.year.yearnum
            week_number = week.weeknum

            if year not in week_numbers_and_years:
                week_numbers_and_years[year] = []

            week_numbers_and_years[year].append(week_number)
        return week_numbers_and_years

    def __before_pick_deadline(self,week):
        if week.pick_deadline == None:
            return False
        current_time = datetime.datetime.utcnow()
        current_time_tz = pytz.timezone('UTC').localize(current_time)
        return current_time_tz <= week.pick_deadline

    def __after_pick_deadline(self,week):
        if week.pick_deadline == None:
            return False
        current_time = datetime.datetime.utcnow()
        current_time_tz = pytz.timezone('UTC').localize(current_time)
        return current_time_tz > week.pick_deadline

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

    def __week_has_no_games(self,year,week_number):
        week = Week.objects.get(year__yearnum=year, weeknum=week_number)
        games = Game.objects.filter(week=week)
        return len(games) == 0
