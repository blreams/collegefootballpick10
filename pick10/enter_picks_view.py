from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from pick10.models import *
from enter_picks import *
from calculator import *
from database import *
from django.http import HttpResponseNotFound
import pytz
from pick10.week_navbar import *

class EnterPicksView:

    def get(self,request,year,week_number,player_id):

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

        if self.__user_is_not_participant(request.user):
            data = self.__setup_basic_params(year,week_number)
            data['error'] = 'user_not_participant'
            WeekNavbar(year,week_number,'enter_picks',request.user).add_parameters(data)
            return render(request,"pick10/enter_picks_error.html",data)

        if not(self.__does_logged_in_user_match_player(request,player_id)):
            data = self.__setup_basic_params(year,week_number)
            data['player_id'] = player_id
            data['error'] = 'user_player_mismatch'
            WeekNavbar(year,week_number,'enter_picks',request.user).add_parameters(data)
            return render(request,"pick10/enter_picks_error.html",data)

        week_state = Database().get_week_state(year,week_number)

        if week_state == IN_PROGRESS:
            data = self.__setup_basic_params(year,week_number)
            data['error'] = 'week_in_progress'
            WeekNavbar(year,week_number,'enter_picks',request.user).add_parameters(data)
            return render(request,"pick10/enter_picks_error.html",data)

        if week_state == FINAL:
            data = self.__setup_basic_params(year,week_number)
            data['error'] = 'week_final'
            WeekNavbar(year,week_number,'enter_picks',request.user).add_parameters(data)
            return render(request,"pick10/enter_picks_error.html",data)

        if self.__is_after_pick_deadline(year,week_number):
            data = self.__setup_basic_params(year,week_number)
            data['error'] = 'after_pick_deadline'
            data['deadline'] = self.__get_pick_deadline(year,week_number,player_id)
            WeekNavbar(year,week_number,'enter_picks',request.user).add_parameters(data)
            return render(request,"pick10/enter_picks_error.html",data)

        picks = EnterPicks(year,week_number,player_id).get_game_picks()
        self.__setup_pick_error_messages(picks)
        return self.__render_form_from_data(request,year,week_number,player_id,picks)

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

        if self.__user_is_not_participant(request.user):
            data = self.__setup_basic_params(year,week_number)
            data['error'] = 'user_not_participant'
            return render(request,"pick10/enter_picks_error.html",data)

        if not(self.__does_logged_in_user_match_player(request,player_id)):
            data = self.__setup_basic_params(year,week_number)
            data['player_id'] = player_id
            data['error'] = 'user_player_mismatch'
            return render(request,"pick10/enter_picks_error.html",data)

        week_state = Database().get_week_state(year,week_number)

        if week_state == IN_PROGRESS:
            data = self.__setup_basic_params(year,week_number)
            data['error'] = 'week_in_progress'
            return render(request,"pick10/enter_picks_error.html",data)

        if week_state == FINAL:
            data = self.__setup_basic_params(year,week_number)
            data['error'] = 'week_final'
            return render(request,"pick10/enter_picks_error.html",data)

        if self.__is_after_pick_deadline(year,week_number):
            data = self.__setup_basic_params(year,week_number)
            data['error'] = 'after_pick_deadline'
            data['deadline'] = self.__get_pick_deadline(year,week_number,player_id)
            return render(request,"pick10/enter_picks_error.html",data)

        cancel_clicked = request.POST.get("cancel_form")
        if cancel_clicked:
            return redirect("week_results",year=year,week_number=week_number)

        submit_clicked = request.POST.get("submit_form")
        if not submit_clicked:
            errmsg = "Unexpected Error!  Expected submit button to be clicked but wasn't"
            return render(request,"pick10/error_message.html",message=errmsg)

        enter_picks = EnterPicks(year,week_number,player_id)

        picks = enter_picks.get_game_picks()
        self.__setup_pick_error_messages(picks)
        error_found = self.__get_and_verify_post_data(request,picks)
        if error_found:
            return self.__render_form_from_data(request,year,week_number,player_id,picks)

        enter_picks.save_picks(picks)
        return redirect("player_results",year=year,week_number=week_number,player_id=player_id)

    def __render_form_from_data(self,request,year,week_number,player_id,picks):
        d = Database()

        weeks_in_year = d.get_week_numbers(year)
        years_in_pool = sorted(d.get_years(),reverse=True)

        params = dict()
        params['year'] = year
        params['week_number'] = week_number
        params['weeks_in_year'] = weeks_in_year
        params['years_in_pool'] = years_in_pool
        params['player_name'] = self.__get_player_name(player_id)

        self.__setup_pick_team_rows(picks)
        self.__set_game10_params(picks,params)

        params['picks'] = picks


        WeekNavbar(year,week_number,'enter_picks',request.user).add_parameters(params)
        return render(request,"pick10/enter_picks.html",params)

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

    def __get_and_verify_post_data(self,request,picks):
        error_found = False

        for game_number in range(1,11):
            index = game_number - 1

            pick = request.POST.get('pick_%d' % (game_number))

            if game_number != 10:
                if pick == "team1":
                    picks[index].pick = TEAM1
                elif pick == "team2":
                    picks[index].pick = TEAM2
                else:
                    picks[index].pick = 0
                    picks[index].error_message = "Please pick a team"
                    error_found = True
            else:
                team1_score = self.__get_score(request,'team1-score')
                team2_score = self.__get_score(request,'team2-score')

                if team1_score == None or team2_score == None:
                    error_found = True
                    picks[index].error_message = "Team score is invalid"
                    picks[index].team1_predicted_points = "" if team1_score == None else team1_score
                    picks[index].team2_predicted_points = "" if team2_score == None else team2_score
                else:
                    picks[index].team1_predicted_points = team1_score
                    picks[index].team2_predicted_points = team2_score
                    picks[index].pick = self.__get_team_pick(picks[index],team1_score,team2_score)

        return error_found

    def __get_score(self,request,input_name):
        try:
            score_string = request.POST.get(input_name)
            score = int(score_string)
            if score < 0:
                return None
            return score
        except:
            return None

    def __get_player_name(self,player_id):
        player = Player.objects.get(id=player_id)
        return player.private_name

    def __does_logged_in_user_match_player(self,request,player_id):
        try:
            profile = UserProfile.objects.get(player__id=player_id)
            return profile.user == request.user
        except:
            return False
    
    def __setup_basic_params(self,year,week_number):
        d = Database()

        weeks_in_year = d.get_week_numbers(year)
        years_in_pool = sorted(d.get_years(),reverse=True)

        params = dict()
        params['year'] = year
        params['week_number'] = week_number
        params['weeks_in_year'] = weeks_in_year
        params['years_in_pool'] = years_in_pool

        return params

    def __is_after_pick_deadline(self,year,week_number):
        d = Database()
        return d.after_pick_deadline(year,week_number)

    def __get_pick_deadline(self,year,week_number,player_id):
        profile = UserProfile.objects.get(player__id=player_id)
        deadline = Database().get_pick_deadline(year,week_number)
        return self.__format_pick_deadline(deadline,profile.preferredtz)

    def __get_local_time(self,utc_date,timezone_name):
        tz = pytz.timezone(timezone_name)
        return utc_date.astimezone(tz)

    def __format_pick_deadline(self,pick_deadline_utc,timezone):
        pick_deadline = self.__get_local_time(pick_deadline_utc,timezone)
        date_format = "%a %m/%d/%Y %I:%M %p %Z"
        return pick_deadline.strftime(date_format)

    def __user_is_not_participant(self,user):
        try:
            profile = UserProfile.objects.get(user=user)
            return profile.player == None
        except:
            return True

    def __get_team_pick(self,data,team1_score,team2_score):
        # setup dummy Game() required to use calculator.py function
        game = Game()
        game.team1_actual_points = team1_score
        game.team2_actual_points = team2_score
        game.spread = data.spread
        game.favored = data.favored

        # calculate winner
        calc = CalculateResults(None)
        if calc.is_team1_winning_pool(game):
            return TEAM1
        elif calc.is_team2_winning_pool(game):
            return TEAM2

        raise AssertionError,"Team1 or Team2 should be winning the game"

    def __set_game10_params(self,picks,params):
        for pick in picks:
            if pick.number == 10:
                params['game10_spread'] = pick.spread
                params['game10_favored'] = pick.favored
                return
        raise AssertionError,'Could not find game 10'
