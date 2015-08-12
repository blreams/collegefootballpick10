from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from week_results_view import *
from player_results_view import *

@login_required
def home(request):
    return render(request, 'pick10/home.html')

def index(request):
    return render(request, 'pick10/index.html')

def week_results(request,year,week_number):
    response = WeekResultsView().get(request,year,week_number)
    return response

def player_results(request,year,week_number,player_id):
    response = PlayerResultsView().get(request,year,week_number,player_id)
    return response
