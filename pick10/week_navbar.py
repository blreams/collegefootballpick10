#from pick10.database import *
#from pick10.calculator import *
from pick10.database import Database
from pick10.calculator import NOT_STARTED
from django.core.urlresolvers import reverse

class PageLink:
    name = None
    link = None
    active = False

# This class creates the data used by the
# week_navbar.html template to display the
# links for different week numbers and pages
class WeekNavbar:

    def __init__(self,year,week,page,user):
        self.year = year
        self.week_number = week
        self.page = page
        self.user = user
        self.__determine_player_id()
        self.__calculate_parameters()

    def add_parameters(self,params):
        for name in self.params:
            if name not in params:
                params[name] = self.params[name]

    def __calculate_parameters(self):
        params = dict()
        params['year'] = self.year
        params['week_number'] = self.week_number
        params['weeks_in_year'] = Database().get_week_numbers(self.year)
        params['navbar_pages'] = self.__get_page_links()
        self.params = params

    def __get_page_links(self):
        page_links = []

        overall = PageLink()
        overall.name = "Overall"
        overall.link = reverse('overall_results',args=(self.year,))
        overall.active = True if self.page == "overall" else False
        page_links.append(overall)

        if self.__show_week_results():
            week_results = PageLink()
            week_results.name = "Week Results"
            week_results.link = reverse('week_results',args=(self.year,self.week_number,))
            week_results.active = True if self.page == "week_results" else False
            page_links.append(week_results)

        if self.__show_player_results():
            player_results = PageLink()
            player_results.name = "Player Results"
            player_results.link = reverse('player_results',args=(self.year,self.week_number,self.player_id,))
            player_results.active = True if self.page == "player_results" else False
            page_links.append(player_results)

        if self.__show_enter_picks():
            enter_picks = PageLink()
            enter_picks.name = "Enter Picks"
            enter_picks.link = reverse('enter_picks',args=(self.year,self.week_number,self.player_id,))
            enter_picks.active = True if self.page == "enter_picks" else False
            page_links.append(enter_picks)

        if self.__show_update_games():
            update_games = PageLink()
            update_games.name = "Game Scores"
            update_games.link = reverse('update_games',args=(self.year,self.week_number,))
            update_games.active = True if self.page == "update_games" else False
            page_links.append(update_games)

        return page_links

    def __get_user_profile(self):
        try:
            profile = UserProfile.objects.get(user=self.user)
            return profile
        except:
            return None

    def __is_player_in_year(self,player_id,year):
        d = Database()
        players_in_year = d.load_players(year)
        return player_id in players_in_year

    def __determine_player_id(self):
        profile = self.__get_user_profile()

        profile_linked_to_player = profile != None and profile.player != None

        if profile_linked_to_player and\
           self.__is_player_in_year(profile.player.id,self.year):
            self.player_id = profile.player.id
            return

        self.player_id = None

    def __show_player_results(self):
        return self.player_id != None

    def __show_week_results(self):
        # show week results once the pool has started
        d = Database()
        pool_state = d.get_pool_state(self.year)
        if pool_state == "invalid" or pool_state == "not_started":
            return False

        return True

    def __show_enter_picks(self):
        user_not_linked_to_player = self.player_id == None
        if user_not_linked_to_player:
            return False

        d = Database()
        pool_state = d.get_pool_state(self.year)
        if pool_state == "invalid" or pool_state == "not_started" or pool_state == "week_setup":
            return False

        week_state = Database().get_week_state(self.year,self.week_number)
        if week_state == NOT_STARTED:
            return True

        # enter picks page link still shows up if pick deadline has expired
        # this is so that the user can know that the deadline has expired

        return False

    def __show_update_games(self):
        d = Database()

        if self.user.is_superuser:
            return True

        user_not_linked_to_player = self.player_id == None

        if user_not_linked_to_player:
            return False

        if d.before_pick_deadline(self.year,self.week_number):
            return False

        if d.is_week_scores_locked(self.year,self.week_number):
            return False

        if d.is_week_being_setup(self.year,self.week_number):
            return False

        return True
