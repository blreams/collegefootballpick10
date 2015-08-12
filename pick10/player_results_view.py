from django.shortcuts import render
from django.template.loader import render_to_string
from pick10.models import *
from pick10.calculate_player_results import *
import string
import re

class PlayerResultsView:

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
        d = Database()

        if not(self.__is_player_in_year(player_id,year)):
            data={'year':year,'player_id':player_id,'error':'bad_year'}
            return render(request,"pick10/bad_player.html",data)

        # TODO set timezone for kickoff date and lock picks time
        timezone = 'US/Eastern'

        if self.__hide_player_results(request.user,player_id,year,week_number):
            pick_deadline_utc = d.get_pick_deadline(year,week_number)
            pick_deadline = self.__format_pick_deadline(pick_deadline_utc,timezone)
            data={'year':year,'player_id':player_id,'error':'before_pick_deadline','deadline':pick_deadline}
            return render(request,"pick10/bad_player.html",data)

        use_private_names = request.user.is_authenticated()

        calc = CalculatePlayerResults(year,week_number,player_id,use_private_names)
        summary = calc.get_player_summary()
        results = calc.get_results()

        params = dict()
        params['year'] = year
        params['week_number'] = week_number
        params['weeks_in_year'] = d.get_week_numbers(year)
        params['summary'] = summary
        params['results'] = results
        params['FINAL'] = FINAL
        params['IN_PROGRESS'] = IN_PROGRESS
        params['NOT_STARTED'] = NOT_STARTED

        self.set_game_status_params(params,results,timezone)

        return render(request,"pick10/player_results.html",params)

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

    def set_game_status_params(self,params,results,timezone):
        top_ids = []
        top_statuses = []
        bottom_ids = []
        bottom_statuses = []

        for result in results:
            top_status,bottom_status,top_id,bottom_id = self.get_game_status(result,timezone)

            top_ids.append(top_id)
            top_statuses.append(top_status)
            bottom_ids.append(bottom_id)
            bottom_statuses.append(bottom_status)

        params['top_status_id'] = top_ids
        params['top_status'] = top_statuses
        params['bottom_status_id'] = bottom_ids
        params['bottom_status'] = bottom_statuses

    def get_game_status(self,result,timezone):
        if result.game_state == NOT_STARTED:
            return self.__game_not_started_status(result,timezone)
        elif result.game_state == IN_PROGRESS:
            return self.__game_in_progress_status(result)
        elif result.game_state == FINAL:
            return self.__game_final_status()
        raise AssertionError,"bad game state: %s" % (result.game_state)

    def __game_not_started_status(self,result,timezone):
        if result.game_date == None:
            top_status = ""
            bottom_status = ""
            top_id = "status-empty"
            bottom_id = "status-empty"
        else:
            local_game_date = self.__get_local_time(result.game_date,timezone)
            weekday_month_day = "%a %m/%d"
            hour_minutes_ampm_timezone = "%I:%M %p %Z"
            top_status = local_game_date.strftime(weekday_month_day)
            bottom_status = local_game_date.strftime(hour_minutes_ampm_timezone)
            top_id = "game-time"
            bottom_id = "game-time"
        return top_status,bottom_status,top_id,bottom_id

    def __get_local_time(self,utc_date,timezone_name):
        tz = pytz.timezone(timezone_name)
        return utc_date.astimezone(tz)

    def __game_in_progress_status(self,result):
        quarter_missing = not(result.game_quarter) or result.game_quarter == ""
        time_left_missing = not(result.game_time_left) or result.game_time_left == ""

        if quarter_missing and time_left_missing:
            top_status = ""
            bottom_status = "in progress"
            top_id = "status-empty"
            bottom_id = "game-in-progress"
        elif quarter_missing and not(time_left_missing):
            top_status = ""
            bottom_status = result.game_time_left
            top_id = "status-empty"
            bottom_id = "game-time-in-progress"
        elif not(quarter_missing) and time_left_missing:
            top_status = ""
            bottom_status = result.game_quarter
            top_id = "status-empty"
            bottom_id = "game-quarter"
        else:
            top_status = result.game_quarter 
            bottom_status = result.game_time_left
            top_id = "game-quarter"
            bottom_id = "game-time-in-progress"

        return top_status,bottom_status,top_id,bottom_id

    def __game_final_status(self):
        top_status = ""
        bottom_status = "final"
        top_id = "status-empty"
        bottom_id = "game-final"

        return top_status,bottom_status,top_id,bottom_id

    def __hide_player_results(self,user,player_id,year,week_number):

        show_results = False
        hide_results = True

        # TODO:  possible bug getting user profile, so need to implement this later
        # check that player_id == user.profile.player.id
        player_id_matches_logged_in_user = False
        if player_id_matches_logged_in_user:
            return show_results

        d = Database()

        if d.before_pick_deadline(year,week_number):
            return hide_results
        else:
            return show_results

    def __format_pick_deadline(self,pick_deadline_utc,timezone):
        pick_deadline = self.__get_local_time(pick_deadline_utc,timezone)
        date_format = "%a %m/%d/%Y %I:%M %p %Z"
        return pick_deadline.strftime(date_format)
