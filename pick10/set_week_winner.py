from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from datetime import datetime
from .models import get_week, get_player_by_private_name
from .forms import SetWeekWinnerForm

class SetWeekWinnerView:

    def get(self,request, year_num, week_num):
        form = SetWeekWinnerForm()
        return render(request, 'pick10/set_week_winner_form.html', {'form': form, 'year_num': year_num, 'week_num': week_num})

    def post(self, request, year_num, week_num):
        form = SetWeekWinnerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            winner = cd.get('winner')
            w = get_week(year_num, week_num)
            w.winner = get_player_by_private_name(winner)
            w.save()
            return redirect('/pick10/commissioner')
        return render(request, 'pick10/set_week_winner_form.html', {'form': form, 'year_num': year_num, 'week_num': week_num})

