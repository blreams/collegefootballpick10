from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseNotFound, HttpResponse
from .overall_results_view import OverallResultsView
from .week_results_view import WeekResultsView
from .tiebreak_view import TiebreakView
from .user_access import UserAccess

class UpdatePageView:

    def get(self,request,year,week_number):
        access = UserAccess(request.user)

        if access.is_superuser() or access.is_private_user():
            data={'year':year,'week_number':week_number}
            return render(request, "pick10/update_pages.html", data)

        return HttpResponseNotFound('<h1>Page not found</h1>')

    def update_overall(self,request,year):
        access = UserAccess(request.user)

        if access.is_superuser() or access.is_private_user():
            response = OverallResultsView().get(request,year,use_private_names=False,use_memcache=False)
            response = OverallResultsView().get(request,year,use_private_names=True,use_memcache=False)
            return HttpResponse("<html>success</html>")

        return HttpResponseNotFound('<h1>Page not found</h1>')

    def update_week(self,request,year,week_number):
        access = UserAccess(request.user)

        if access.is_superuser() or access.is_private_user():
            response = WeekResultsView().get(request,year,week_number,use_private_names=False,use_memcache=False)
            response = WeekResultsView().get(request,year,week_number,use_private_names=True,use_memcache=False)
            return HttpResponse("<html>success</html>")

        return HttpResponseNotFound('<h1>Page not found</h1>')

    def update_tiebreak(self,request,year,week_number):
        access = UserAccess(request.user)

        if access.is_superuser() or access.is_private_user():
            response = TiebreakView().get(request,year,week_number,use_private_names=False,use_memcache=False)
            response = TiebreakView().get(request,year,week_number,use_private_names=True,use_memcache=False)
            return HttpResponse("<html>success</html>")

        return HttpResponseNotFound('<h1>Page not found</h1>')
