from django.shortcuts import render
from pick10.models import get_yearlist, get_weeklist, get_profile_by_user, calc_weekly_points
from forms import IndexForm

class IndexView:

    def get(self,request):
        yearlist = get_yearlist()
        year_num = 0
        week_num = 0
        if len(yearlist) > 0:
            year_num = yearlist[-1]
            weeklist = get_weeklist(year_num)
            if len(weeklist) > 0:
                week_num = weeklist[-1]
            else:
                year_num = 0
        profile = get_profile_by_user(user=request.user)
        over_under_list = calc_weekly_points(year_num, request.user.username, overunder=True)
        form = IndexForm()
        context = {
                'year_num': year_num,
                'week_num': week_num,
                'week_range': range(1, week_num + 1),
                'profile': profile,
                'over_under_list': over_under_list,
                'form': form,
                }

        return render(request,"pick10/index.html", context)

    def post(self, request):
        form = IndexForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            year_num = int(cd.get('year'))

        yearlist = get_yearlist()
        if year_num in yearlist:
            week_num = 0
            weeklist = get_weeklist(year_num)
            if len(weeklist) > 0:
                week_num = weeklist[-1]
            else:
                year_num = 0
        profile = get_profile_by_user(user=request.user)
        over_under_list = calc_weekly_points(year_num, request.user.username, overunder=True)
        context = {
                'year_num': year_num,
                'week_num': week_num,
                'week_range': range(1, week_num + 1),
                'profile': profile,
                'over_under_list': over_under_list,
                'form': form,
                }

        return render(request,"pick10/index.html", context)

