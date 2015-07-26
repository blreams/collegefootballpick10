from django.shortcuts import render
from django.template.loader import render_to_string
from pick10.models import *
from pick10.calculate_week_results import *

class WeekResultsView:

    def get(self,request,year,week_number):

        if self.__bad_year_or_week_number(year,week_number):
            data={'year':year,'week_number':week_number}
            return render(request,"pick10/bad_week.html",data)

        year = int(year)
        week_number = int(week_number)

        cwr = CalculateWeekResults(year,week_number)
        results = cwr.get_results()
        week_state = cwr.get_week_state()
        winner_info = cwr.get_winner_info()

        if week_state == FINAL:
            self.__render_file = "pick10/week_final_results.html"
        elif week_state == IN_PROGRESS:
            self.__render_file = "pick10/week_in_progress_results.html"
        elif week_state == NOT_STARTED:
            self.__render_file = "pick10/week_not_started_results.html"
        else:
            raise AssertionError,"Invalid week state %s" % (week_state)

        params = dict()
        params['year'] = year
        params['week_number'] = week_number
        #params['weeks_in_year'] = weeks_in_year
        params['content'] = self.__initial_content(results,winner_info)
        #params['sorted_by_wins'] = self.__sort_by_wins(results,winner_info)
        #params['sorted_by_wins_reversed'] = self.__sort_by_wins_reversed(results,winner_info)
        #params['sorted_by_losses'] = self.__sort_by_losses(results,winner_info)
        #params['sorted_by_losses_reversed'] = self.__sort_by_losses_reversed(results,winner_info)
        #params['sorted_by_players'] = self.__sort_by_players(results,winner_info)
        #params['sorted_by_players_reversed'] = self.__sort_by_players_reversed(results,winner_info)

        #if week_state == "in_progress":
            #params['sorted_by_projected_wins'] = self.__sort_by_projected_wins(results,winner_info)
            #params['sorted_by_projected_wins_reversed'] = self.__sort_by_projected_wins_reversed(results,winner_info)
            #params['sorted_by_possible_wins'] = self.__sort_by_possible_wins(results,winner_info)
            #params['sorted_by_possible_wins_reversed'] = self.__sort_by_possible_wins_reversed(results,winner_info)
        #elif week_state == "not_started":
            #params['sorted_by_possible_wins'] = self.__sort_by_possible_wins(results,winner_info)
            #params['sorted_by_possible_wins_reversed'] = self.__sort_by_possible_wins_reversed(results,winner_info)

        return render(request,"pick10/week_results.html",params)

    def __initial_content(self,results,winner_info):
        return self.__sort_by_wins(results,winner_info,escape=False)

    def __sort_by_wins(self,results,winner_info,escape=True):
        sorted_by_players = sorted(results,key=lambda result:result.player_name)
        sorted_by_wins = sorted(sorted_by_players,key=lambda result:result.rank)
        self.__move_winner_to_top(sorted_by_wins,results)
        highlight = self.__highlight_column('wins')

        params = dict()
        params['results'] = sorted_by_wins
        params['winner'] = winner_info
        params.update(highlight)

        content = render_to_string(self.__render_file,params)
        import pdb; pdb.set_trace()
        if escape:
            html_str = self.escape_string(content)
            return self.compress_html(html_str)
        return content

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
