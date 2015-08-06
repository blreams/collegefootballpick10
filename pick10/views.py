from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from overall_results_view import *
from week_results_view import *
from player_results_view import *
from update_view import *
from tiebreak_view import *
from update_games_view import *
from django.core.cache import *

@login_required
def home(request):
    return render(request, 'pick10/home.html')

def index(request):
    return render(request, 'pick10/index.html')

def overall_results(request,year):
    response = OverallResultsView().get(year)
    return response

def week_results(request,year,week_number):
    response = WeekResultsView().get(year,week_number)
    return response

def player_results(request,year,week_number,player_id):
    response = PlayerResultsView().get(request,year,week_number,player_id)
    return response

def tiebreak(request,year,week_number):
    response = TiebreakView().get(year,week_number)
    return response

def update_games(request,year,week_number):
    if request.method == "GET":
        response = UpdateGamesView().get(request,year,week_number)
    elif request.method == "POST":
        response = UpdateGamesView().post(request,year,week_number)
    return response

def update_pages(request,year,week_number):
    response = UpdatePageView().get(year,week_number)
    return response

def update_overall(request,year):
    response = UpdatePageView().update_overall(year)
    return response

def update_week(request,year,week_number):
    response = UpdatePageView().update_week(year,week_number)
    return response

def update_tiebreak(request,year,week_number):
    response = UpdatePageView().update_tiebreak(year,week_number)
    return response
