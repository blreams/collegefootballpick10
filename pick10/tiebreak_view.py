from django.shortcuts import render
from django.template.loader import render_to_string
from pick10.calculate_tiebreak import *
from calculator import *
from django.core.cache import *
from django.http import HttpResponse

class TiebreakView:

    def get(self,request,year,week_number,use_private_names=False,use_memcache=True):

        if self.__bad_year_or_week_number(year,week_number):
            data={'year':year,'week_number':week_number}
            return render(request,"pick10/bad_week.html",data,status=400)

        year = int(year)
        week_number = int(week_number)

        # setup memcache parameters
        cache = get_cache('default')
        if use_private_names:
            body_key = "tiebreak_private_%d_%d" % (year,week_number)
        else:
            body_key = "tiebreak_public_%d_%d" % (year,week_number)
        sidebar_key = "tiebreak_year_sidebar"

        # look for hit in the memcache
        if use_memcache:
            body = cache.get(body_key)
            sidebar = cache.get(sidebar_key)
            memcache_hit = body != None and sidebar != None
            if memcache_hit:
                data = {'body_content':body,'side_block_content':sidebar }
                return render(request,"pick10/tiebreak.html",data)

        d = Database()
        weeks_in_year = d.get_week_numbers(year)
        years_in_pool = sorted(d.get_years(),reverse=True)

        tiebreak = CalculateTiebreak(year,week_number,use_private_names)

        params = dict()
        params['year'] = year
        params['week_number'] = week_number
        params['weeks_in_year'] = weeks_in_year
        params['years_in_pool'] = years_in_pool
        params['winner_valid'] = tiebreak.was_able_to_determine_winner()
        params['featured_game_state'] = tiebreak.get_featured_game_state()
        params['summary'] = tiebreak.get_tiebreaker_summary()
        params['tiebreaker0_details'] = tiebreak.get_tiebreaker0_details()
        params['tiebreaker1_details'] = tiebreak.get_tiebreaker1_details()
        params['tiebreaker2_details'] = tiebreak.get_tiebreaker2_details()
        params['tiebreaker3_details'] = tiebreak.get_tiebreaker3_details()
        params['tiebreaker1_summary'] = tiebreak.get_tiebreaker1_summary()
        params['tiebreaker2_summary'] = tiebreak.get_tiebreaker2_summary()
        params['tiebreaker3_summary'] = tiebreak.get_tiebreaker3_summary()
        params['tiebreaker_required'] = params['summary'] != None and len(params['summary']) > 1
        params['tiebreaker0_valid'] = params['tiebreaker0_details'] != None and len(params['tiebreaker0_details']) > 0
        params['tiebreaker1_valid'] = params['tiebreaker1_details'] != None and len(params['tiebreaker1_details']) > 0
        params['tiebreaker2_valid'] = params['tiebreaker2_details'] != None and len(params['tiebreaker2_details']) > 0
        params['tiebreaker3_valid'] = params['tiebreaker3_details'] != None and len(params['tiebreaker3_details']) > 0
        params['NOT_STARTED'] = NOT_STARTED
        params['IN_PROGRESS'] = IN_PROGRESS
        params['FINAL'] = FINAL

        body = render_to_string("pick10/tiebreak_body.html",params)
        sidebar = render_to_string("pick10/year_sidebar.html",params)

        cache.set(body_key,body)
        cache.set(sidebar_key,sidebar)

        data = {'body_content':body,'side_block_content':sidebar }
        return render(request,"pick10/tiebreak.html",data)

    def __bad_year_or_week_number(self,year,week_number):
        try:
            year_int = int(year)
            week_int = int(week_number)
            w = get_week(year_int,week_int)
        except Exception:
            return True
        return False
