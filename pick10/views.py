from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from profile import *
from overall_results_view import *
from week_results_view import *
from player_results_view import *
from update_view import *
from tiebreak_view import *
from update_games_view import *
from enter_picks_view import *
from django.core.cache import *
from django.http import HttpResponseNotFound

def home(request):
    return render(request, 'pick10/home.html')

@login_required
def index(request):
    return render(request, 'pick10/index.html')

@login_required
def profile(request):
    if request.method == 'GET':
        response = ProfileView().get(request)
        return response
    elif request.method == 'POST':
        response = ProfileView().post(request)
        return response
    return HttpResponseNotFound('<h1>Page not found</h1>')

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
