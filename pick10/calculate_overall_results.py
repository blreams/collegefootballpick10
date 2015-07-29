from calculator import *
from database import *

class CalculateOverallResults:

    def __init__(self,year,week_number,private_names=False):
        self.year = year
        self.week_number = week_number
        self.__use_private_names = private_names
        self.__calculate_overall_results()

    def get_results(self):
        return self.__results

    def __calculate_overall_results(self):
        self.__results = None
