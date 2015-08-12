from django.shortcuts import render
from django.template.loader import render_to_string
from pick10.overall_results_view import *
from pick10.week_results_view import *
from pick10.tiebreak_view import *

class UpdatePageView:

    def get(self,year,week_number):
        data={'year':year,'week_number':week_number}
        html = render_to_string("pick10/update_pages.html",data)
        return HttpResponse(html)

    def update_overall(self,year):
        response = OverallResultsView().get(year,use_private_names=False,use_memcache=False)
        response = OverallResultsView().get(year,use_private_names=True,use_memcache=False)
        return HttpResponse("<html>success</html>")

    def update_week(self,year,week_number):
        response = WeekResultsView().get(year,week_number,use_private_names=False,use_memcache=False)
        response = WeekResultsView().get(year,week_number,use_private_names=True,use_memcache=False)
        return HttpResponse("<html>success</html>")

    def update_tiebreak(self,year,week_number):
        response = TiebreakView().get(year,week_number,use_private_names=False,use_memcache=False)
        response = TiebreakView().get(year,week_number,use_private_names=True,use_memcache=False)
        return HttpResponse("<html>success</html>")
