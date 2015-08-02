from django.shortcuts import render
from django.template.loader import render_to_string
from pick10.models import *
from update_games import *

class UpdateGamesView:

    def get(self,request,year,week_number):

        if self.__bad_year_or_week_number(year,week_number):
            data={'year':year,'week_number':week_number}
            return render(request,"pick10/bad_week.html",data)

        d = Database()

        year = int(year)
        week_number = int(week_number)
        weeks_in_year = d.get_week_numbers(year)

        params = dict()
        params['year'] = year
        params['week_number'] = week_number
        params['weeks_in_year'] = weeks_in_year
        params['games'] = UpdateGames(year,week_number).get_games()
        params['locked'] = self.__is_week_scores_locked(year,week_number)

        return render(request,"pick10/update_games.html",params)

    def post(self,request,year,week_number):
        return None

    def __bad_year_or_week_number(self,year,week_number):
        try:
            year_int = int(year)
            week_int = int(week_number)
            w = get_week(year_int,week_int)
        except Exception:
            return True
        return False

    def __is_week_scores_locked(self,year,week_number):
        week = get_week(year,week_number)
        return week.lock_scores
