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

        use_private_names = request.user.is_authenticated()

        if not(self.__is_player_in_year(player_id,year)):
            data={'year':year,'player_id':player_id,'error':'bad_year'}
            return render(request,"pick10/bad_player.html",data)

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
