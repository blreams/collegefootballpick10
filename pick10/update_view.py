from django.shortcuts import render
from django.template.loader import render_to_string
from pick10.overall_results_view import *
from pick10.week_results_view import *
from pick10.tiebreak_view import *

class UpdatePageView:

    def get(self,request,year,week_number):
        data={'year':year,'week_number':week_number}
        return render(request, "pick10/update_pages.html", data)
        #html = render_to_string("pick10/update_pages.html",data)
        #return HttpResponse(html)

    def update_overall(self,request,year):
        response = OverallResultsView().get(request,year,use_private_names=False,use_memcache=False)
        response = OverallResultsView().get(request,year,use_private_names=True,use_memcache=False)
        return HttpResponse("<html>success</html>")

    def update_week(self,request,year,week_number):
        response = WeekResultsView().get(request,year,week_number,use_private_names=False,use_memcache=False)
        response = WeekResultsView().get(request,year,week_number,use_private_names=True,use_memcache=False)
        return HttpResponse("<html>success</html>")

    def update_tiebreak(self,request,year,week_number):
        response = TiebreakView().get(request,year,week_number,use_private_names=False,use_memcache=False)
        response = TiebreakView().get(request,year,week_number,use_private_names=True,use_memcache=False)
        return HttpResponse("<html>success</html>")
