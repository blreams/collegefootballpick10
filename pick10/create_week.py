from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from datetime import datetime
from models import Year, Week
from models import add_year, add_week
from forms import CreateWeekForm

class CreateWeekView:

    def get(self,request):
        form = CreateWeekForm()
        return render(request, 'pick10/create_week_form.html', {'form': form})

    def post(self, request):
        form = CreateWeekForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            year = cd.get('year')
            week = cd.get('week')
            add_year(year)
            w = add_week(year, week)
            return redirect('/pick10/commissioner/editweek/' + str(year) + '/week/' + str(week))
        return render(request, 'pick10/create_week_form.html', {'form': form})

