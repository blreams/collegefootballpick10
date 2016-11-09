import string
import re
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.cache import *
#from pick10.models import *
#from pick10.database import *
#from pick10.calculate_week_results import *
#from django.http import HttpResponse
#from pick10.week_navbar import *
#from pick10.user_access import *
from pick10.models import get_week
from pick10.database import Database
from pick10.calculate_week_results import CalculateWeekResults
from pick10.week_navbar import WeekNavbar
from pick10.user_access import UserAccess
from pick10.calculator import NOT_STARTED, IN_PROGRESS, FINAL

class WeekResultsView:

    def get(self,request,year,week_number,use_private_names=None,use_memcache=True):

        loading_memcache = request == None

        if self.__bad_year_or_week_number(year,week_number):
            assert not loading_memcache,"When loading memcache, year/week needs to be valid "
            data={'year':year,'week_number':week_number}
            return render(request,"pick10/bad_week.html",data,status=400)

        year = int(year)
        week_number = int(week_number)

        d = Database()

        if d.is_week_being_setup(year,week_number):
            assert not loading_memcache,"Loading memcache does not support week being setup"
            years_in_pool = sorted(d.get_years(),reverse=True)
            data={'error':'week_not_setup','years_in_pool':years_in_pool,'year':year}
            WeekNavbar(year,week_number,'week_results',request.user).add_parameters(data)
            return render(request,"pick10/week_results_error.html",data,status=400)

        if loading_memcache:
            access = None
        else:
            access = UserAccess(request.user)

        use_private_names = self.__determine_private_access(access,use_private_names)

        # setup memcache parameters
        cache = get_cache('default')
        if use_private_names:
            body_key = "week_private_%d_%d" % (year,week_number)
        else:
            body_key = "week_public_%d_%d" % (year,week_number)

        years_in_pool = sorted(d.get_years(),reverse=True)
        sidebar = render_to_string("pick10/year_sidebar.html",{'years_in_pool':years_in_pool,'year':year})

        # look for hit in the memcache
        if not loading_memcache and use_memcache:
            body = cache.get(body_key)
            memcache_hit = body != None
            if memcache_hit:
                data = {'body_content':body,'side_block_content':sidebar,'week_number':week_number }
                self.__set_player_id(access,data)
                WeekNavbar(year,week_number,'week_results',request.user).add_parameters(data)
                return render(request,"pick10/week_results.html",data)

        cwr = CalculateWeekResults(year,week_number,use_private_names)
        results = cwr.get_results()
        week_state = cwr.get_week_state()
        winner_info = cwr.get_winner_info()

        if week_state == FINAL:
            self.week_state_string = 'final'
        elif week_state == IN_PROGRESS:
            self.week_state_string = 'in_progress'
        elif week_state == NOT_STARTED:
            self.week_state_string = 'not_started'
        else:
            raise AssertionError,"Invalid week state %s" % (week_state)

        self.__render_file = "pick10/week_results_combined.html"

        params = dict()
        params['year'] = year
        params['week_number'] = week_number
        params['years_in_pool'] = years_in_pool
        params['content'] = self.__initial_content(results,winner_info)
        params['sorted_by_wins'] = self.__sort_by_wins(results,winner_info)
        params['sorted_by_wins_reversed'] = self.__sort_by_wins_reversed(results,winner_info)
        params['sorted_by_losses'] = self.__sort_by_losses(results,winner_info)
        params['sorted_by_losses_reversed'] = self.__sort_by_losses_reversed(results,winner_info)
        params['sorted_by_players'] = self.__sort_by_players(results,winner_info)
        params['sorted_by_players_reversed'] = self.__sort_by_players_reversed(results,winner_info)

        if week_state == IN_PROGRESS:
            params['sorted_by_projected_wins'] = self.__sort_by_projected_wins(results,winner_info)
            params['sorted_by_projected_wins_reversed'] = self.__sort_by_projected_wins_reversed(results,winner_info)
            params['sorted_by_possible_wins'] = self.__sort_by_possible_wins(results,winner_info)
            params['sorted_by_possible_wins_reversed'] = self.__sort_by_possible_wins_reversed(results,winner_info)
        elif week_state == NOT_STARTED:
            params['sorted_by_possible_wins'] = self.__sort_by_possible_wins(results,winner_info)
            params['sorted_by_possible_wins_reversed'] = self.__sort_by_possible_wins_reversed(results,winner_info)

        body = render_to_string("pick10/week_results_body.html",params)

        cache.set(body_key,body)
        if loading_memcache:
            return

        data = {'body_content':body,'side_block_content':sidebar,'week_number':week_number }
        self.__set_player_id(access,data)
        WeekNavbar(year,week_number,'week_results',request.user).add_parameters(data)

        return render(request,"pick10/week_results.html",data)

    def __initial_content(self,results,winner_info):
        return self.__sort_by_wins(results,winner_info,escape=False)

    def __sort_by_wins(self,results,winner_info,escape=True):
        sorted_by_players = sorted(results,key=lambda result:result.player_name)
        sorted_by_wins = sorted(sorted_by_players,key=lambda result:result.rank)
        self.__move_winner_to_top(sorted_by_wins,results)
        highlight = self.__highlight_column('wins')

        params = dict()
        params['week_state'] = self.week_state_string
        params['results'] = sorted_by_wins
        params['winner'] = winner_info
        params.update(highlight)

        content = render_to_string(self.__render_file,params)
        if escape:
            html_str = self.escape_string(content)
            return self.compress_html(html_str)
        return content

    def __sort_by_wins_reversed(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name,reverse=True)
        sorted_by_wins = sorted(sorted_by_players,key=lambda result:result.rank,reverse=True)
        self.__move_winner_to_bottom(sorted_by_wins,results)
        highlight = self.__highlight_column('wins')

        params = dict()
        params['week_state'] = self.week_state_string
        params['results'] = sorted_by_wins
        params['winner'] = winner_info
        params.update(highlight)

        content = render_to_string(self.__render_file,params)
        html_str = self.escape_string(content)
        return self.compress_html(html_str)

    def __sort_by_losses(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name,reverse=False)
        sorted_by_losses = sorted(sorted_by_players,key=lambda result:result.rank,reverse=True)
        highlight = self.__highlight_column('losses')

        params = dict()
        params['week_state'] = self.week_state_string
        params['results'] = sorted_by_losses
        params['winner'] = winner_info
        params.update(highlight)

        content = render_to_string(self.__render_file,params)
        html_str = self.escape_string(content)
        return self.compress_html(html_str)

    def __sort_by_losses_reversed(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name,reverse=True)
        sorted_by_losses = sorted(sorted_by_players,key=lambda result:result.rank)
        highlight = self.__highlight_column('losses')

        params = dict()
        params['week_state'] = self.week_state_string
        params['results'] = sorted_by_losses
        params['winner'] = winner_info
        params.update(highlight)

        content = render_to_string(self.__render_file,params)
        html_str = self.escape_string(content)
        return self.compress_html(html_str)

    def __sort_by_players(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name)
        highlight = self.__highlight_no_columns()

        params = dict()
        params['week_state'] = self.week_state_string
        params['results'] = sorted_by_players
        params['winner'] = winner_info
        params.update(highlight)

        content = render_to_string(self.__render_file,params)
        html_str = self.escape_string(content)
        return self.compress_html(html_str)

    def __sort_by_players_reversed(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name,reverse=True)
        highlight = self.__highlight_no_columns()

        params = dict()
        params['week_state'] = self.week_state_string
        params['results'] = sorted_by_players
        params['winner'] = winner_info
        params.update(highlight)

        content = render_to_string(self.__render_file,params)
        html_str = self.escape_string(content)
        return self.compress_html(html_str)

    def __sort_by_projected_wins(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name,reverse=False)
        sorted_by_wins = sorted(sorted_by_players,key=lambda result:result.projected_rank)
        self.__move_winner_to_top(sorted_by_wins,results,use_projected_rank=True)
        highlight = self.__highlight_column('projected_wins')

        params = dict()
        params['week_state'] = self.week_state_string
        params['results'] = sorted_by_wins
        params['winner'] = winner_info
        params['use_projected_rank'] = True
        params.update(highlight)

        content = render_to_string(self.__render_file,params)
        html_str = self.escape_string(content)
        return self.compress_html(html_str)

    def __sort_by_projected_wins_reversed(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name,reverse=True)
        sorted_by_wins = sorted(results,key=lambda result:result.projected_rank,reverse=True)
        self.__move_winner_to_bottom(sorted_by_wins,results,use_projected_rank=True)
        highlight = self.__highlight_column('projected_wins')

        params = dict()
        params['week_state'] = self.week_state_string
        params['results'] = sorted_by_wins
        params['winner'] = winner_info
        params['use_projected_rank'] = True
        params.update(highlight)

        content = render_to_string(self.__render_file,params)
        html_str = self.escape_string(content)
        return self.compress_html(html_str)

    def __sort_by_possible_wins(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name,reverse=False)
        sorted_by_wins = sorted(sorted_by_players,key=lambda result:result.possible_wins,reverse=True)
        highlight = self.__highlight_column('possible_wins')

        params = dict()
        params['week_state'] = self.week_state_string
        params['results'] = sorted_by_wins
        params['winner'] = winner_info
        params.update(highlight)

        content = render_to_string(self.__render_file,params)
        html_str = self.escape_string(content)
        return self.compress_html(html_str)

    def __sort_by_possible_wins_reversed(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name,reverse=True)
        sorted_by_wins = sorted(sorted_by_players,key=lambda result:result.possible_wins)
        highlight = self.__highlight_column('possible_wins')

        params = dict()
        params['week_state'] = self.week_state_string
        params['results'] = sorted_by_wins
        params['winner'] = winner_info
        params.update(highlight)

        content = render_to_string(self.__render_file,params)
        html_str = self.escape_string(content)
        return self.compress_html(html_str)

    def __highlight_no_columns(self):
        return self.__highlight_column(None)

    def __move_winner_to_top(self,sorted_data,results,use_projected_rank=False):
        for result in results:
            if use_projected_rank and result.projected_rank != 1:
                continue

            if use_projected_rank == False and result.rank != 1:
                continue

            if result.winner != None and result.winner != "":
                index = self.__find_player_id(result.player_id,sorted_data)
                item = sorted_data.pop(index)
                sorted_data.insert(0,item)

    def __move_winner_to_bottom(self,sorted_data,results,use_projected_rank=False):
        for result in results:
            if use_projected_rank and result.projected_rank != 1:
                continue

            if use_projected_rank == False and result.rank != 1:
                continue

            if result.winner != None and result.winner != "":
                index = self.__find_player_id(result.player_id,sorted_data)
                item = sorted_data.pop(index)
                sorted_data.append(item)

    def __bad_year_or_week_number(self,year,week_number):
        try:
            year_int = int(year)
            week_int = int(week_number)
            w = get_week(year_int,week_int)
        except Exception:
            return True
        return False

    def __highlight_column(self,name):
        d = dict()

        if name == "wins":
            d['wins_id'] = "highlight-content"
        else:
            d['wins_id'] = "content"

        if name == "losses":
            d['losses_id'] = "highlight-content"
        else:
            d['losses_id'] = "content"

        if name == "projected_wins":
            d['projected_id'] = "highlight-content"
        else:
            d['projected_id'] = "content"

        if name == "possible_wins":
            d['possible_id'] = "highlight-content"
        else:
            d['possible_id'] = "content"

        return d

    def __find_player_id(self,player_id,data):
        for i,item in enumerate(data):
            if player_id == item.player_id:
                return i
        raise AssertionError

    def escape_string(self,s):
        return string.replace(s,'"','\\\"')

    def compress_html(self,html):
        s1 = string.replace(html,'\n','')
        return re.sub(r'\s\s+',' ',s1)

    def __determine_private_access(self,access,use_private_names):
        force_public_private = use_private_names != None
        if force_public_private:
            return use_private_names

        return access.is_private_user()

    def __set_player_id(self,access,data):
        player = access.get_player()
        if player:
            data['player_id'] = player.id
            return
        data['player_id'] = 'null'
