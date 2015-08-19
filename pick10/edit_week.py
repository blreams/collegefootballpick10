from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from datetime import datetime
from models import Year, Week
from forms import CreateWeekForm, EditWeekForm

class EditWeekView:

    def get(self,request, year, week_number):
        form = EditWeekForm()
        context = {'form': form, 'year': year, 'week_number': week_number}
        return render(request,"pick10/edit_week_form.html", context)

    def post(self, request):
        form = CreateWeekForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #year = cd.get('year')
            #week = cd.get('week')
            return redirect('/pick10/commissioner/editweek/' + str(year) + '/week/' + str(week) + '/')
        return redirect('/pick10/commissioner/createweek/')
