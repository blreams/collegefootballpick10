from django.shortcuts import render
from django.template.loader import render_to_string
from pick10.models import *
from pick10.calculate_overall_results import *

class OverallResultsView:

    def get(self,request,year):
        return
