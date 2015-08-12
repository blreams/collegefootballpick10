from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from pick10.models import *
from enter_picks import *
from calculator import *
from database import *
from django.http import HttpResponseNotFound

class EnterPicksView:

    def get(self,request,year,week_number,player_id):

        if self.__bad_year_or_week_number(year,week_number):
            data={'year':year,'week_number':week_number}
            return render(request,"pick10/bad_week.html",data)

        if not(self.__is_player_id_valid(player_id)):
            data={'player_id':player_id,'error':'bad_id'}
            return render(request,"pick10/bad_player.html",data)

        d = Database()

        year = int(year)
        week_number = int(week_number)
        player_id = int(player_id)
        weeks_in_year = d.get_week_numbers(year)
        years_in_pool = sorted(d.get_years(),reverse=True)

        if not(self.__is_player_in_year(player_id,year)):
            data={'year':year,'player_id':player_id,'error':'bad_year'}
            return render(request,"pick10/bad_player.html",data)

        params = dict()
        params['year'] = year
        params['week_number'] = week_number
        params['weeks_in_year'] = weeks_in_year
        params['years_in_pool'] = years_in_pool

        picks = EnterPicks(year,week_number,player_id).get_game_picks()
        self.__setup_pick_team_rows(picks)
        self.__setup_pick_error_messages(picks)

        params['picks'] = picks

        return render(request,"pick10/enter_picks.html",params)

    def post(self,request,year,week_number,player_id):

        if self.__bad_year_or_week_number(year,week_number):
            data={'year':year,'week_number':week_number}
            return render(request,"pick10/bad_week.html",data)

        if not(self.__is_player_id_valid(player_id)):
            data={'player_id':player_id,'error':'bad_id'}
            return render(request,"pick10/bad_player.html",data)

        year = int(year)
        week_number = int(week_number)
        player_id = int(player_id)

        if not(self.__is_player_in_year(player_id,year)):
            data={'year':year,'player_id':player_id,'error':'bad_year'}
            return render(request,"pick10/bad_player.html",data)

        cancel_clicked = request.POST.get("cancel_form")
        if cancel_clicked:
            return redirect("week_results",year=year,week_number=week_number)

        submit_clicked = request.POST.get("submit_form")
        if not submit_clicked:
            errmsg = "Unexpected Error!  Expected submit button to be clicked but wasn't"
            return render(request,"pick10/error_message.html",message=errmsg)

        picks = EnterPicks(year,week_number,player_id).get_game_picks()
        self.__verify_post_data(request,picks)

        return HttpResponseNotFound('<h1>Page not found</h1>')

    def __bad_year_or_week_number(self,year,week_number):
        try:
            year_int = int(year)
            week_int = int(week_number)
            w = get_week(year_int,week_int)
        except Exception:
            return True
        return False

    def __is_player_id_valid(self,player_id):
        try:
            id_int = int(player_id)
            player = Player.objects.get(id=id_int)
        except Exception:
            return False
        return True

    def __is_player_in_year(self,player_id,year):
        d = Database()
        players_in_year = d.load_players(year)
        return player_id in players_in_year

    def __setup_pick_team_rows(self,picks):
        for i,pick_info in enumerate(picks):
            if pick_info.pick == TEAM1:
                picks[i].team1_row_class = "info"
                picks[i].team1_checked = "checked"
                picks[i].team2_row_class = ""
                picks[i].team2_checked = ""
            elif pick_info.pick == TEAM2:
                picks[i].team1_row_class = ""
                picks[i].team1_checked = ""
                picks[i].team2_row_class = "info"
                picks[i].team2_checked = "checked"
            else:
                picks[i].team1_row_class = ""
                picks[i].team1_checked = ""
                picks[i].team2_row_class = ""
                picks[i].team2_checked = ""

    def __setup_pick_error_messages(self,picks):
        for i in range(len(picks)):
            picks[i].error_message = None

    def __verify_post_data(self,request,picks):
        error_found = False

        for game_number in range(1,11):
            index = game_number - 1

            pick = request.POST.get('pick_%d' % (game_number))

            if pick == "team1":
                picks[index].pick = TEAM1
            elif pick == "team2":
                picks[index].pick = TEAM2
            else:
                picks[index].pick = 0
                picks[index].error_message = "Please pick a team"
                error_found = True

            if game_number == 10:
                pass # get scores
