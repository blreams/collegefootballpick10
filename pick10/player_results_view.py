from django.shortcuts import render
from django.template.loader import render_to_string
from pick10.models import *
from pick10.calculate_player_results import *
import string
import re

class PlayerResultsView:

    def get(self,request,year,week_number):
        return None

