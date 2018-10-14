from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

from django.shortcuts import render
from .models import get_yearlist, get_weeklist, get_profile_by_user, calc_weekly_points
from .forms import IndexForm
from .calculator import CalculateResults, IN_PROGRESS, FINAL
from .database import Database

class IndexView:

    def get(self,request):
        year_num = 0
        week_num = 0
        last_completed_week_num = 0
        last_inprogress_week_num = 0
        yearlist = get_yearlist()
        if len(yearlist) > 0:
            year_num = yearlist[-1]
            weeklist = get_weeklist(year_num, only_unlocked_picks=True)
            if len(weeklist) > 0:
                week_num = weeklist[-1]
            else:
                year_num = 0
            if year_num:
                db = Database()
                try:
                    for w in weeklist:
                        cr = CalculateResults(db.load_week_data(year_num, w))
                        week_state = cr.get_summary_state_of_all_games()
                        if week_state == FINAL:
                            last_completed_week_num = w
                        elif week_state == IN_PROGRESS:
                            last_inprogress_week_num = w
                except:
                    pass
        profile = get_profile_by_user(user=request.user)
        player_name, player_over_under_list = calc_weekly_points(year_num, request.user.username, overunder=True)
        compare_name, compare_over_under_list = calc_weekly_points(year_num, None, overunder=True)
        form = IndexForm()
        context = {
                'year_num': year_num,
                'week_num': week_num,
                'last_completed_week_num': last_completed_week_num,
                'last_inprogress_week_num': last_inprogress_week_num,
                'week_range': range(1, week_num + 1),
                'profile': profile,
                'player_name': player_name,
                'player_over_under_list': player_over_under_list,
                'player_color': '#009999',
                'compare_name': compare_name,
                'compare_over_under_list': compare_over_under_list,
                'compare_color': '#cc0099',
                'form': form,
                }

        return render(request,"pick10/index.html", context)

    def post(self, request):
        form = IndexForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            year_num = int(cd.get('year'))

        week_num = 0
        last_completed_week_num = 0
        last_inprogress_week_num = 0
        yearlist = get_yearlist()
        if year_num in yearlist:
            week_num = 0
            weeklist = get_weeklist(year_num, only_unlocked_picks=True)
            if len(weeklist) > 0:
                week_num = weeklist[-1]
            else:
                year_num = 0
            if year_num:
                db = Database()
                try:
                    for w in weeklist:
                        cr = CalculateResults(db.load_week_data(year_num, w))
                        week_state = cr.get_summary_state_of_all_games()
                        if week_state == FINAL:
                            last_completed_week_num = w
                        elif week_state == IN_PROGRESS:
                            last_inprogress_week_num = w
                except:
                    pass
        profile = get_profile_by_user(user=request.user)
        player_name, player_over_under_list = calc_weekly_points(year_num, request.user.username, overunder=True)
        compare_name, compare_over_under_list = calc_weekly_points(year_num, None, overunder=True)
        context = {
                'year_num': year_num,
                'week_num': week_num,
                'last_completed_week_num': last_completed_week_num,
                'last_inprogress_week_num': last_inprogress_week_num,
                'week_range': range(1, week_num + 1),
                'profile': profile,
                'player_name': player_name,
                'player_over_under_list': player_over_under_list,
                'player_color': '#009999',
                'compare_name': compare_name,
                'compare_over_under_list': compare_over_under_list,
                'compare_color': '#cc0099',
                'form': form,
                }

        return render(request,"pick10/index.html", context)

