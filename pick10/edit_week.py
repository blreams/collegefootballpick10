from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from datetime import datetime
from models import Year, Week
from forms import CreateWeekForm, EditWeekForm

class EditWeekView:

    def get(self,request, year, week_number):
        teams = {'game1_team1': u'South Carolina', 'game1_team2': u'North Carolina'}
        form = EditWeekForm(teams=teams)
        context = {'form': form, 'year': year, 'week_number': week_number}
        return render(request,"pick10/edit_week_form.html", context)

    def post(self, request, year, week_number):
        form = EditWeekForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            teams = cd
            return redirect('/pick10/')
        return redirect('edit_week', year=year, week_number=week_number)

