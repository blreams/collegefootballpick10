from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from datetime import datetime
from models import Year, Week
from models import get_commish_can_post, get_teams_dict_for_week, set_week_lock_picks
from forms import CreateWeekForm, EditWeekForm

class EditWeekView:

    def get(self,request, year, week_number):
        teams = get_teams_dict_for_week(year, week_number)
        form = EditWeekForm(teams=teams)
        context = {'form': form, 'year': year, 'week_number': week_number, 'commish_can_post': get_commish_can_post(year, week_number)}
        return render(request,"pick10/edit_week_form.html", context)

    def post(self, request, year, week_number):
        teams = get_teams_dict_for_week(year, week_number)
        form = EditWeekForm(request.POST)
        context = {'form': form, 'year': year, 'week_number': week_number}
        # Need to set a LOCK that players will observe before getting/posting picks
        saved_lock_picks = set_week_lock_picks(year, week_number, datetime.now())
        if not get_commish_can_post(year, week_number):
            context['commish_can_post'] = False
            set_week_lock_picks(year, week_number, saved_lock_picks)
            return render(request,"pick10/edit_week_form.html", context)
        if form.is_valid():
            cd = form.cleaned_data
            teams = cd
            # Need to clear the LOCK that players will observe before getting/posting picks
            set_week_lock_picks(year, week_number, saved_lock_picks)
            return redirect('/pick10/')
        # Need to clear the LOCK that players will observe before getting/posting picks
        set_week_lock_picks(year, week_number, saved_lock_picks)
        return redirect('edit_week', year=year, week_number=week_number)

