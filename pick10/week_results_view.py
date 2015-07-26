from django.shortcuts import render
from pick10.models import *
from pick10.calculate_week_results import *

class WeekResultsView:

    def get(self,request,year,week_number):

        if self.__bad_year_or_week_number(year,week_number):
            data={'year':year,'week_number':week_number}
            return render(request,"pick10/bad_week.html",data)

        year = int(year)
        week_number = int(week_number)

        cwr = CalculateWeekResults(year,week_number)
        results = cwr.get_results()
        week_state = cwr.get_week_state()
        winner_info = cwr.get_winner_info()

        if week_state == FINAL:
            self.__render_file = "pick10/week_final_results.html"
        elif week_state == IN_PROGRESS:
            self.__render_file = "pick10/week_in_progress_results.html"
        elif week_state == NOT_STARTED:
            self.__render_file = "pick10/week_not_started_results.html"
        else:
            raise AssertionError,"Invalid week state %s" % (week_state)

        params = dict()
        params['year'] = year
        params['week_number'] = week_number
        #params['weeks_in_year'] = weeks_in_year
        #params['content'] = self.__initial_content(results,winner_info)
        params['content'] = '<div>Week Results Content</div>'
        #params['sorted_by_wins'] = self.__sort_by_wins(results,winner_info)
        #params['sorted_by_wins_reversed'] = self.__sort_by_wins_reversed(results,winner_info)
        #params['sorted_by_losses'] = self.__sort_by_losses(results,winner_info)
        #params['sorted_by_losses_reversed'] = self.__sort_by_losses_reversed(results,winner_info)
        #params['sorted_by_players'] = self.__sort_by_players(results,winner_info)
        #params['sorted_by_players_reversed'] = self.__sort_by_players_reversed(results,winner_info)

        #if week_state == "in_progress":
            #params['sorted_by_projected_wins'] = self.__sort_by_projected_wins(results,winner_info)
            #params['sorted_by_projected_wins_reversed'] = self.__sort_by_projected_wins_reversed(results,winner_info)
            #params['sorted_by_possible_wins'] = self.__sort_by_possible_wins(results,winner_info)
            #params['sorted_by_possible_wins_reversed'] = self.__sort_by_possible_wins_reversed(results,winner_info)
        #elif week_state == "not_started":
            #params['sorted_by_possible_wins'] = self.__sort_by_possible_wins(results,winner_info)
            #params['sorted_by_possible_wins_reversed'] = self.__sort_by_possible_wins_reversed(results,winner_info)

        return render(request,"pick10/week_results.html",params)

    def __bad_year_or_week_number(self,year,week_number):
        try:
            year_int = int(year)
            week_int = int(week_number)
            w = get_week(year_int,week_int)
        except Exception:
            return True
        return False
