from django.shortcuts import render
from django.template.loader import render_to_string
from pick10.models import *
from pick10.database import *
from pick10.calculate_overall_results import *
import string
import re
from django.core.cache import *
from django.http import HttpResponse, HttpResponseNotFound
from pick10.week_navbar import *
from pick10.user_access import *

class OverallResultsView:

    def get(self,request,year,use_private_names=None,use_memcache=True):

        year = int(year)
        loading_memcache = request == None
        d = Database()

        if not(d.is_year_valid(year)):
            assert not loading_memcache,"When loading memcache, year needs to be valid "
            data={'year':year}
            return render(request,"pick10/bad_year.html",data,status=400)

        if loading_memcache:
            access = None
        else:
            access = UserAccess(request.user)

        use_private_names = self.__determine_private_access(access,use_private_names)

        # setup memcache parameters
        cache = get_cache('default')
        if use_private_names:
            body_key = "overall_private_%d" % (year)
        else:
            body_key = "overall_public_%d" % (year)

        pool_state = d.get_pool_state(year)

        weeks_in_year = d.get_week_numbers(year)
        last_week_number = weeks_in_year[-1]

        years_in_pool = sorted(d.get_years(),reverse=True)
        sidebar = render_to_string("pick10/year_sidebar.html",{'years_in_pool':years_in_pool,'year':year})

        if pool_state == "week_setup":    # use last weeks results
            weeks_in_year.remove(last_week_number)
            last_week_number = last_week_number - 1

        # What if we need to go back a year?
        if last_week_number == 0:
            year -= 1
            pool_state = d.get_pool_state(year)
            weeks_in_year = d.get_week_numbers(year)
            last_week_number = weeks_in_year[-1]

        # look for hit in the memcache
        if not loading_memcache and use_memcache:
            body = cache.get(body_key)
            memcache_hit = body != None
            if memcache_hit:
                data = {'body_content':body,'side_block_content':sidebar,'year':year,'weeks_in_year':weeks_in_year }
                self.__set_player_id(access,data)
                WeekNavbar(year,last_week_number,'overall',request.user).add_parameters(data)
                return render(request,"pick10/overall_results.html",data)

        years_in_pool = sorted(d.get_years(),reverse=True)

        if pool_state == "not_started":
            players = d.load_players(year)

            data={'year':year, 'num_players':len(players)}
            body = render_to_string("pick10/overall_not_started.html",data)
            cache.set(body_key,body)

            if loading_memcache:
                return

            data = {'body_content':body,'side_block_content':sidebar,'year':year }
            WeekNavbar(year,last_week_number,'overall',request.user).add_parameters(data)
            return render(request,"pick10/overall_results.html",data)

        results = CalculateOverallResults(year,use_private_names,use_weeks=weeks_in_year).get_results()

        content_params = dict()
        content_params['year'] = year
        content_params['weeks_in_year'] = weeks_in_year
        content_params['pool_state'] = pool_state
        content_params['results'] = results
        content_params['last_week_number'] = last_week_number

        if pool_state == "week_setup":
            self.__render_file = "pick10/overall_week_final_results.html"
        elif pool_state == "enter_picks":
            self.__render_file = "pick10/overall_enter_picks_results.html"
        elif pool_state == "week_not_started":
            self.__render_file = "pick10/overall_week_not_started_results.html"
        elif pool_state == "week_in_progress":
            self.__render_file = "pick10/overall_week_in_progress_results.html"
        elif pool_state == "week_final":
            self.__render_file = "pick10/overall_week_final_results.html"
        elif pool_state == "end_of_year":
            self.__render_file = "pick10/overall_final_results.html"

        params = dict()
        params['year'] = year
        params['weeks_in_year'] = weeks_in_year
        params['years_in_pool'] = years_in_pool
        params['last_week_number'] = weeks_in_year[-1]
        params['pool_state'] = pool_state
        params['results'] = results
        params['content'] = self.__initial_content(content_params)
        params['sorted_by_overall'] = self.__sort_by_overall(content_params)
        params['sorted_by_overall_reversed'] = self.__sort_by_overall_reversed(content_params)
        params['sorted_by_players'] = self.__sort_by_players(content_params)
        params['sorted_by_players_reversed'] = self.__sort_by_players_reversed(content_params)

        if pool_state == "week_not_started":
            params['sorted_by_projected'] = ""
            params['sorted_by_projected_reversed'] = ""
            params['sorted_by_possible'] = self.__sort_by_overall_possible(content_params)
            params['sorted_by_possible_reversed'] = self.__sort_by_overall_possible_reversed(content_params)
        elif pool_state == "week_final":
            params['sorted_by_projected'] = ""
            params['sorted_by_projected_reversed'] = ""
            params['sorted_by_possible'] = self.__sort_by_overall_possible(content_params)
            params['sorted_by_possible_reversed'] = self.__sort_by_overall_possible_reversed(content_params)
        elif pool_state == "week_in_progress":
            params['sorted_by_projected'] = self.__sort_by_overall_projected(content_params)
            params['sorted_by_projected_reversed'] = self.__sort_by_overall_projected_reversed(content_params)
            params['sorted_by_possible'] = self.__sort_by_overall_possible(content_params)
            params['sorted_by_possible_reversed'] = self.__sort_by_overall_possible_reversed(content_params)
        else:
            params['sorted_by_projected'] = ""
            params['sorted_by_projected_reversed'] = ""
            params['sorted_by_possible'] = ""
            params['sorted_by_possible_reversed'] = ""

        body = render_to_string("pick10/overall_results_body.html",params)
        cache.set(body_key,body)

        if loading_memcache:
            return

        data = {'body_content':body,'side_block_content':sidebar,'year':year,'weeks_in_year':weeks_in_year }
        self.__set_player_id(access,data)
        WeekNavbar(year,last_week_number,'overall',request.user).add_parameters(data)
        return render(request,"pick10/overall_results.html",data)

    def __initial_content(self,content_params):
        return self.__sort_by_overall(content_params,escape=False)

    def __sort_by_overall(self,content_params,escape=True):
        sorted_by_overall = sorted(content_params['results'],key=lambda result:result.rank)

        params = dict()
        params['year'] = content_params['year']
        params['weeks_in_year'] = content_params['weeks_in_year']
        params['last_week_number'] = content_params['last_week_number']
        params['pool_state'] = content_params['pool_state']
        params['results'] = sorted_by_overall

        self.__highlight_column('overall',params)

        content = render_to_string(self.__render_file,params)

        if escape:
            html_str = self.escape_string(content)
            return self.compress_html(html_str)
        return content

    def __sort_by_overall_reversed(self,content_params):
        sorted_by_overall_reversed = sorted(content_params['results'],key=lambda result:result.rank,reverse=True)

        params = dict()
        params['year'] = content_params['year']
        params['weeks_in_year'] = content_params['weeks_in_year']
        params['last_week_number'] = content_params['last_week_number']
        params['pool_state'] = content_params['pool_state']
        params['results'] = sorted_by_overall_reversed

        self.__highlight_column('overall',params)

        content = render_to_string(self.__render_file,params)
        html_str = self.escape_string(content)
        return self.compress_html(html_str)


    def __sort_by_players(self,content_params):
        sorted_by_players = sorted(content_params['results'],key=lambda result:result.player_name)

        params = dict()
        params['year'] = content_params['year']
        params['weeks_in_year'] = content_params['weeks_in_year']
        params['last_week_number'] = content_params['last_week_number']
        params['pool_state'] = content_params['pool_state']
        params['results'] = sorted_by_players

        self.__highlight_no_columns(params)

        content = render_to_string(self.__render_file,params)
        html_str = self.escape_string(content)
        return self.compress_html(html_str)


    def __sort_by_players_reversed(self,content_params):
        sorted_by_players_reversed = sorted(content_params['results'],key=lambda result:result.player_name,reverse=True)

        params = dict()
        params['year'] = content_params['year']
        params['weeks_in_year'] = content_params['weeks_in_year']
        params['last_week_number'] = content_params['last_week_number']
        params['pool_state'] = content_params['pool_state']
        params['results'] = sorted_by_players_reversed

        self.__highlight_no_columns(params)

        content = render_to_string(self.__render_file,params)
        html_str = self.escape_string(content)
        return self.compress_html(html_str)

    def __sort_by_overall_projected(self,content_params,escape=True):
        sorted_by_overall_projected = sorted(content_params['results'],key=lambda result:result.projected_rank)

        params = dict()
        params['year'] = content_params['year']
        params['weeks_in_year'] = content_params['weeks_in_year']
        params['last_week_number'] = content_params['last_week_number']
        params['pool_state'] = content_params['pool_state']
        params['results'] = sorted_by_overall_projected
        params['rank'] = "projected"

        self.__highlight_column('projected',params)

        content = render_to_string(self.__render_file,params)

        if escape:
            html_str = self.escape_string(content)
            return self.compress_html(html_str)
        return content

    def __sort_by_overall_projected_reversed(self,content_params):
        sorted_by_overall_projected_reversed = sorted(content_params['results'],key=lambda result:result.projected_rank,reverse=True)

        params = dict()
        params['year'] = content_params['year']
        params['weeks_in_year'] = content_params['weeks_in_year']
        params['last_week_number'] = content_params['last_week_number']
        params['pool_state'] = content_params['pool_state']
        params['results'] = sorted_by_overall_projected_reversed
        params['rank'] = "projected"

        self.__highlight_column('projected',params)

        content = render_to_string(self.__render_file,params)
        html_str = self.escape_string(content)
        return self.compress_html(html_str)

    def __sort_by_overall_possible(self,content_params,escape=True):
        sorted_by_overall_possible = sorted(content_params['results'],key=lambda result:result.possible,reverse=True)

        params = dict()
        params['year'] = content_params['year']
        params['weeks_in_year'] = content_params['weeks_in_year']
        params['last_week_number'] = content_params['last_week_number']
        params['pool_state'] = content_params['pool_state']
        params['results'] = sorted_by_overall_possible

        self.__highlight_column('possible',params)

        content = render_to_string(self.__render_file,params)

        if escape:
            html_str = self.escape_string(content)
            return self.compress_html(html_str)
        return content

    def __sort_by_overall_possible_reversed(self,content_params):
        sorted_by_overall_possible_reversed = sorted(content_params['results'],key=lambda result:result.possible)

        params = dict()
        params['year'] = content_params['year']
        params['weeks_in_year'] = content_params['weeks_in_year']
        params['last_week_number'] = content_params['last_week_number']
        params['pool_state'] = content_params['pool_state']
        params['results'] = sorted_by_overall_possible_reversed

        self.__highlight_column('possible',params)

        content = render_to_string(self.__render_file,params)
        html_str = self.escape_string(content)
        return self.compress_html(html_str)

    def __highlight_no_columns(self,params):
        return self.__highlight_column(None,params)

    def __highlight_column(self,name,params):
        if name == "overall":
            params['overall_id'] = "highlight-content"
        else:
            params['overall_id'] = "content"

        if name == "projected":
            params['projected_id'] = "highlight-content"
        else:
            params['projected_id'] = "content"

        if name == "possible":
            params['possible_id'] = "highlight-content"
        else:
            params['possible_id'] = "content"

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
