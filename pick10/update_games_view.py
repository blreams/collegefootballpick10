from django.shortcuts import render
from django.template.loader import render_to_string
from pick10.models import *

class UpdateGamesView:

    def get(self,request,year,week_number):
        import pdb; pdb.set_trace()
        return None

    def post(self,request,year,week_number):
        return None
