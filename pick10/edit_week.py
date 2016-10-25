from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.utils import timezone
from models import get_commish_can_post, get_games_info_for_week, get_week_info, set_week_lock_picks
from models import add_game, get_week, get_team
from forms import CreateWeekForm, EditWeekForm, EditWeekSelForm

def make_boolean(val):
    if isinstance(val, basestring):
        if val.lower() == 'true':
            return True
        else:
            return False
    elif isinstance(val, int):
        if val != 0:
            return True
        else:
            return False

class EditWeekSelView:

    def get(self, request):
        form = EditWeekSelForm()
        return render(request, 'pick10/edit_week_sel_form.html', {'form': form})

    def post(self, request):
        form = EditWeekSelForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            year = cd.get('year')
            week = cd.get('week')
            return redirect('/pick10/commissioner/editweek/' + str(year) + '/week/' + str(week))
        return render(request, 'pick10/commissioner/edit_week_form.html', {'form': form})


class EditWeekView:

    def get(self,request, year, week_number):
        weekfields = get_week_info(year, week_number)
        gamefields = get_games_info_for_week(year, week_number)
        form = EditWeekForm(weekfields=weekfields, gamefields=gamefields)
        context = {'form': form, 'gamenums': range(1, 11), 'year': year, 'week_number': week_number, 'commish_can_post': get_commish_can_post(year, week_number)}
        return render(request,"pick10/edit_week_form.html", context)

    def post(self, request, year, week_number):
        form = EditWeekForm(request.POST)
        context = {'form': form, 'gamenums': range(1, 11), 'year': year, 'week_number': week_number, 'commish_can_post': True}
        # Need to set a LOCK that players will observe before getting/posting picks
        set_week_lock_picks(year, week_number, True)
        if not get_commish_can_post(year, week_number):
            context['commish_can_post'] = False
            set_week_lock_picks(year, week_number, False)
            return render(request,"pick10/edit_week_form.html", context)
        if form.is_valid():
            cd = form.cleaned_data
            weekobj=get_week(year, week_number)
            weekobj.lock_picks = make_boolean(cd['lock_picks'])
            weekobj.pick_deadline = cd['pick_deadline']
            weekobj.save()
            for i in range(1, 11):
                gamestr = 'game%d_' % i
                gameobj = add_game(
                        week=weekobj,
                        team1=get_team(cd[gamestr + 'team1']),
                        team2=get_team(cd[gamestr + 'team2']),
                        gamenum=i,
                        favored=int(cd[gamestr + 'favored'].replace('Team', '')),
                        spread=cd[gamestr + 'spread'],
                        kickoff=cd[gamestr + 'kickoff'],
                        allowupdate=True,
                        )
                gameobj.game_state = 1
                gameobj.quarter = '1st'
                gameobj.time_left = '15:00'
                gameobj.save()

            # Need to clear the LOCK that players will observe before getting/posting picks
            if not cd['lock_picks']:
                set_week_lock_picks(year, week_number, False)
            return redirect('/pick10/')
        # Need to clear the LOCK that players will observe before getting/posting picks
        # Actually, if you get here, the picks are not ready, so keep lock_picks set
        return render(request, 'pick10/edit_week_form.html', context)

