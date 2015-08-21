from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from datetime import datetime
from models import Year, Week
from models import get_commish_can_post, get_games_info_for_week, set_week_lock_picks
from models import add_game, get_week, get_team
from forms import CreateWeekForm, EditWeekForm

class EditWeekView:

    def get(self,request, year, week_number):
        gamefields = get_games_info_for_week(year, week_number)
        form = EditWeekForm(gamefields=gamefields)
        context = {'form': form, 'year': year, 'week_number': week_number, 'commish_can_post': get_commish_can_post(year, week_number)}
        return render(request,"pick10/edit_week_form.html", context)

    def post(self, request, year, week_number):
        form = EditWeekForm(request.POST)
        context = {'form': form, 'year': year, 'week_number': week_number, 'commish_can_post': True}
        # Need to set a LOCK that players will observe before getting/posting picks
        saved_lock_picks = set_week_lock_picks(year, week_number, datetime.now())
        if not get_commish_can_post(year, week_number):
            context['commish_can_post'] = False
            set_week_lock_picks(year, week_number, saved_lock_picks)
            return render(request,"pick10/edit_week_form.html", context)
        if form.is_valid():
            cd = form.cleaned_data
            for i in range(1, 11):
                gamestr = 'game%d_' % i
                gameobj = add_game(
                        week=get_week(year, week_number),
                        team1=get_team(cd[gamestr + 'team1']),
                        team2=get_team(cd[gamestr + 'team2']),
                        gamenum=i,
                        favored=int(cd[gamestr + 'favored'].replace('Team', '')),
                        spread=cd[gamestr + 'spread'],
                        kickoff=cd[gamestr + 'kickoff'],
                        allowupdate=True,
                        )

            # Need to clear the LOCK that players will observe before getting/posting picks
            set_week_lock_picks(year, week_number, saved_lock_picks)
            return redirect('/pick10/')
        # Need to clear the LOCK that players will observe before getting/posting picks
        set_week_lock_picks(year, week_number, saved_lock_picks)
        return render(request, 'pick10/edit_week_form.html', context)

