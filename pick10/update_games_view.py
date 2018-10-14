from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import get_week
from .database import Database
from .update_games import UpdateGames
from .week_navbar import WeekNavbar
from .user_access import UserAccess
from .calculator import NOT_STARTED, IN_PROGRESS, FINAL

class BadInputException(Exception):
    def __init__(self,errmsg):
        self.errmsg = errmsg

class UpdateGamesView:

    def get(self,request,year,week_number):

        if self.__bad_year_or_week_number(year,week_number):
            data={'year':year,'week_number':week_number}
            return render(request,"pick10/bad_week.html",data,status=400)

        access = UserAccess(request.user)

        d = Database()

        year = int(year)
        week_number = int(week_number)
        weeks_in_year = d.get_week_numbers(year)
        years_in_pool = sorted(d.get_years(),reverse=True)

        # check user/player privileges
        # superuser is allowed to access page no matter what
        if access.is_superuser() == False:

            # only private player can update scores
            if access.is_public_user():
                data={'year':year,'error':'user_not_participant','years_in_pool':years_in_pool}
                WeekNavbar(year,week_number,'update_games',request.user).add_parameters(data)
                return render(request,"pick10/update_games_error.html",data)

            # user's player not in the pool this year
            if access.is_player_in_year(year) == False:
                player_id = access.get_player().id
                data={'year':year,'player_id':player_id,'error':'bad_year','years_in_pool':years_in_pool}
                WeekNavbar(year,week_number,'update_games',request.user).add_parameters(data)
                return render(request,"pick10/update_games_error.html",data)

        if d.is_week_being_setup(year,week_number):
            data={'year':year,'error':'week_not_setup','years_in_pool':years_in_pool}
            WeekNavbar(year,week_number,'update_games',request.user).add_parameters(data)
            return render(request,"pick10/update_games_error.html",data)

        params = dict()
        params['year'] = year
        params['week_number'] = week_number
        params['weeks_in_year'] = weeks_in_year
        params['years_in_pool'] = years_in_pool
        params['games'] = UpdateGames(year,week_number).get_games()
        params['locked'] = self.__is_week_scores_locked(year,week_number)
        params['FINAL'] = FINAL
        params['IN_PROGRESS'] = IN_PROGRESS
        params['NOT_STARTED'] = NOT_STARTED

        WeekNavbar(year,week_number,'update_games',request.user).add_parameters(params)

        return render(request,"pick10/update_games.html",params)

    def post(self,request,year,week_number):

        if self.__bad_year_or_week_number(year,week_number):
            data={'year':year,'week_number':week_number}
            return render(request,"pick10/bad_week.html",data)

        d = Database()

        year = int(year)
        week_number = int(week_number)
        weeks_in_year = d.get_week_numbers(year)

        cancel_clicked = request.POST.get("cancel_form")
        if cancel_clicked:
            return redirect("week_results",year=year,week_number=week_number)

        if request.user.is_superuser:

            unlocked_clicked = request.POST.get("unlock_form")
            if unlocked_clicked:
                w = get_week(year,week_number)
                w.lock_scores = False
                w.save()
                return redirect("update_games",year=year,week_number=week_number)

            locked_clicked = request.POST.get("lock_form")
            if locked_clicked:
                w = get_week(year,week_number)
                w.lock_scores = True
                w.save()
                return redirect("update_games",year=year,week_number=week_number)

        submit_clicked = request.POST.get("submit_form")
        if not submit_clicked:
            errmsg = "Unexpected Error!  Expected submit button to be clicked but wasn't"
            return render(request,"pick10/error_message.html",message=errmsg)

        # check user/player privileges
        # superuser is allowed to access page no matter what
        access = UserAccess(request.user)

        if access.is_superuser() == False:

            # only private player can update scores
            if access.is_public_user():
                data={'year':year,'error':'user_not_participant'}
                data['years_in_pool'] = sorted(d.get_years(),reverse=True)
                WeekNavbar(year,week_number,'update_games',request.user).add_parameters(data)
                return render(request,"pick10/update_games_error.html",data)

            # user's player not in the pool this year
            if access.is_player_in_year(year) == False:
                player_id = access.get_player().id
                data={'year':year,'player_id':player_id,'error':'bad_year'}
                data['years_in_pool'] = sorted(d.get_years(),reverse=True)
                WeekNavbar(year,week_number,'update_games',request.user).add_parameters(data)
                return render(request,"pick10/update_games_error.html",data)

        if d.is_week_being_setup(year,week_number):
            data={'year':year,'error':'week_not_setup'}
            data['years_in_pool'] = sorted(d.get_years(),reverse=True)
            WeekNavbar(year,week_number,'update_games',request.user).add_parameters(data)
            return render(request,"pick10/update_games_error.html",data)

        if self.__is_week_scores_locked(year,week_number):
            data={'year':year,'week_number':week_number,'error':'scores_locked'}
            data['years_in_pool'] = sorted(d.get_years(),reverse=True)
            WeekNavbar(year,week_number,'update_games',request.user).add_parameters(data)
            return render(response,"pick10/update_games_error.html",data)

        u = UpdateGames(year,week_number)
        week_games = u.get_games()

        try:
            for game_number in range(1,11):
                input_data = self.__get_game_input_data(request,game_number)

                index = game_number - 1
                assert week_games[index].number == game_number

                week_games[index].team1_score = input_data['team1_score']
                week_games[index].team2_score = input_data['team2_score']
                week_games[index].quarter = input_data['quarter']
                week_games[index].time_left = input_data['time_left']
                week_games[index].state = input_data['state']

        except BadInputException as e:
            return render(request,"pick10/error_message.html",message=e.errmsg)

        u.update_games(week_games)
        return redirect("update_pages",year=year,week_number=week_number)

    def __bad_year_or_week_number(self,year,week_number):
        try:
            year_int = int(year)
            week_int = int(week_number)
            w = get_week(year_int,week_int)
        except Exception:
            return True
        return False

    def __is_week_scores_locked(self,year,week_number):
        week = get_week(year,week_number)
        return week.lock_scores

    def __get_game_input_data(self,request,game_number):
        team1_score_input = "team1_score_%d" % (game_number)
        quarter_input = "quarter_%d" % (game_number)
        team2_score_input = "team2_score_%d" % (game_number)
        time_input = "time_%d" % (game_number)
        final_input = "final_%d" % (game_number)

        data = dict()

        team1_score_str = request.POST.get(team1_score_input)
        team2_score_str = request.POST.get(team2_score_input)
        final_checked_str = request.POST.get(final_input)

        final_checked = final_checked_str == "checked"

        data['quarter'] = request.POST.get(quarter_input)
        data['time_left'] = request.POST.get(time_input)
        data['team1_score'] = self.__convert_score_to_int(game_number,1,team1_score_str)
        data['team2_score'] = self.__convert_score_to_int(game_number,2,team2_score_str)

        scores_blank = data['team1_score'] == "" or data['team2_score'] == ""
        not_started = not final_checked and scores_blank
        in_progress = not final_checked and not scores_blank
        final = final_checked

        if not_started:
            data['state'] = "not_started"
            data['quarter'] = ""
            data['time_left'] = ""
            data['team1_score'] = ""
            data['team2_score'] = ""
        elif in_progress:
            data['state'] = "in_progress"
        elif final:
            data['state'] = "final"
            data['quarter'] = ""
            data['time_left'] = ""

        return data

    def __convert_score_to_int(self,game_number,team,score_str):
        if score_str == None or score_str == "":
            return ""

        try:
            score = int(score_str)
        except ValueError:
            raise BadInputException("Game %d Team %d score must be blank or an Integer" % (game_number,team))

        return score
