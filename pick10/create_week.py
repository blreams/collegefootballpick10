from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from datetime import datetime
from models import Year, Week

class CreateWeekView:

    def get(self,request):
        year = datetime.now().year
        yearlist = sorted([y.yearnum for y in Year.objects.all()])
        if year in yearlist:
            yearobj = Year.objects.filter(yearnum=year)
            weeks_in_year = sorted([w.weeknum for w in Week.objects.filter(year=yearobj)])
            if weeks_in_year[-1] == 13:
                year += 1
                week = 1
            else:
                week = weeks_in_year[-1] + 1
        else:
            year = yearlist[-1] + 1
            week = 1

        context = {'year': year, 'week': week}
        return render(request,"pick10/create_week_form.html", context)

