from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.cache import *
from django.http import HttpResponseNotFound
from django.contrib.admin.views.decorators import staff_member_required
from .profile import ProfileView
from .create_week import CreateWeekView
from .edit_week import EditWeekSelView
from .edit_week import EditWeekView
from .set_week_winner import SetWeekWinnerView
from .index_view import IndexView
from .week_results_view import WeekResultsView
from .player_results_view import PlayerResultsView
from .update_view import UpdatePageView
from .tiebreak_view import TiebreakView
from .update_games_view import UpdateGamesView
from .enter_picks_view import EnterPicksView
from .overall_results_view import OverallResultsView
from .models import get_yearlist, get_weeklist, get_profile_by_user, get_week_with_no_winner

def home(request):
    return render(request, 'pick10/home.html')

@login_required
def index(request):
    if request.method == 'GET':
        response = IndexView().get(request)
        return response
    elif request.method == 'POST':
        response = IndexView().post(request)
        return response
    return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required
def profile(request):
    if request.method == 'GET':
        response = ProfileView().get(request)
        return response
    elif request.method == 'POST':
        response = ProfileView().post(request)
        return response
    return HttpResponseNotFound('<h1>Page not found</h1>')

@staff_member_required
def commissioner(request):
    year_num = get_yearlist()[-1]
    week_num = get_weeklist(year_num, only_unlocked_picks=True)[-1]
    week_num_no_winner = get_week_with_no_winner(year_num)
    context = {'year_num': year_num, 'week_num': week_num, 'week_num_no_winner': week_num_no_winner}
    return render(request, 'pick10/commissioner.html', context)

@staff_member_required
def create_week(request):
    if request.method == 'GET':
        response = CreateWeekView().get(request)
    elif request.method == 'POST':
        response = CreateWeekView().post(request)
    return response

@staff_member_required
def edit_week_sel(request):
    if request.method == 'GET':
        response = EditWeekSelView().get(request)
    elif request.method == 'POST':
        response = EditWeekSelView().post(request)
    return response

@staff_member_required
def edit_week(request, year, week_number):
    if request.method == 'GET':
        response = EditWeekView().get(request, year, week_number)
    elif request.method == 'POST':
        response = EditWeekView().post(request, year, week_number)
    return response

@staff_member_required
def set_week_winner(request, year_num, week_num):
    if request.method == 'GET':
        response = SetWeekWinnerView().get(request, year_num, week_num)
    elif request.method == 'POST':
        response = SetWeekWinnerView().post(request, year_num, week_num)
    return response

@staff_member_required
def commissioner_stats(request, year_num):
    context = {'year_num': year_num}
    return render(request, 'pick10/commissioner_stats.html', context)

@login_required
def overall_results(request,year):
    if request.method == "GET":
        response = OverallResultsView().get(request,year)
        return response
    return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required
def week_results(request,year,week_number):
    if request.method == "GET":
        response = WeekResultsView().get(request,year,week_number)
        return response
    return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required
def player_results(request,year,week_number,player_id):
    if request.method == "GET":
        response = PlayerResultsView().get(request,year,week_number,player_id)
        return response
    return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required
def tiebreak(request,year,week_number):
    if request.method == "GET":
        response = TiebreakView().get(request,year,week_number)
        return response
    return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required
def update_games(request,year,week_number):
    if request.method == "GET":
        response = UpdateGamesView().get(request,year,week_number)
        return response
    elif request.method == "POST":
        response = UpdateGamesView().post(request,year,week_number)
        return response
    return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required
def enter_picks(request,year,week_number,player_id):
    if request.method == "GET":
        response = EnterPicksView().get(request,year,week_number,player_id)
        return response
    elif request.method == "POST":
        response = EnterPicksView().post(request,year,week_number,player_id)
        return response
    return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required
def update_pages(request,year,week_number):
    if request.method == "GET":
        response = UpdatePageView().get(request,year,week_number)
        return response
    return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required
def update_overall(request,year):
    if request.method == "POST":
        response = UpdatePageView().update_overall(request,year)
        return response
    return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required
def update_week(request,year,week_number):
    if request.method == "POST":
        response = UpdatePageView().update_week(request,year,week_number)
        return response
    return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required
def update_tiebreak(request,year,week_number):
    if request.method == "POST":
        response = UpdatePageView().update_tiebreak(request,year,week_number)
        return response
    return HttpResponseNotFound('<h1>Page not found</h1>')
