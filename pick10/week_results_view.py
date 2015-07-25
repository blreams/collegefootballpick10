from django.shortcuts import render
from pick10.models import *
from django.core.exceptions import ObjectDoesNotExist

class WeekResultsView:

    def get(self,request,year,week_number):
        if self.__bad_year_or_week_number(year,week_number):
            data={'year':year,'week_number':week_number}
            return render(request,"pick10/bad_week.html",data)
        return render(request, 'pick10/index.html')

    def __bad_year_or_week_number(self,year,week_number):
        try:
            w = get_week(year,week_number)
        except ObjectDoesNotExist:
            return True
        return False
