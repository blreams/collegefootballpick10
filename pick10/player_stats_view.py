from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

import string
import re
import pytz
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import Player, get_week
from .database import Database
from .calculate_player_stats import CalculatePlayerStats
from .week_navbar import WeekNavbar
from .user_access import UserAccess
from .calculator import NOT_STARTED, IN_PROGRESS, FINAL

class PlayerStatsView:

    def get(self,request,player_id):

        if not(self.__is_player_id_valid(player_id)):
            data={'player_id':player_id,'error':'bad_id'}
            return render(request,"pick10/bad_player.html",data,status=400)

        player_id = int(player_id)
        d = Database()

        access = UserAccess(request.user)

        use_private_names = access.is_private_user()

        calc = CalculatePlayerStats(player_id, use_private_names)
        summary = calc.get_player_summary()
        stats = calc.get_player_stats()
        years_in_pool = sorted(d.get_years(),reverse=True)
        year = summary['year_numbers'][0]
        week_number = 1

        sidebar = render_to_string("pick10/year_sidebar.html", {'years_in_pool': years_in_pool, 'year': year})

        params = dict()
        params['summary'] = summary
        params['stats'] = stats
        params['side_block_content'] = sidebar

        WeekNavbar(year,week_number,'player_stats',request.user).add_parameters(params)

        return render(request,"pick10/player_stats.html",params)

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

