from pick10.database import *
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

        week_results = PageLink()
        week_results.name = "Week Results"
        week_results.link = reverse('week_results',args=(self.year,self.week_number,))
        week_results.active = True if self.page == "week_results" else False
        page_links.append(week_results)

        return page_links

    # pages: overall, week results, player results, enter picks 
