# This class sets up a database that can be used for unit testing.  
# The class creates a central location for setting up a database 
# so each unit test doesn't have to reinvent the wheel every time.
from pick10.models import *

class UnitTestDatabase:

    def setup_simple_week(self,year=2014,week_number=1):
        week = add_week(year,week_number)
        conf = add_conference('ACC')
        team1 = add_team('Georgia Tech','Buzz',conf)
        team2 = add_team('Clemson','Tigers',conf)
        add_game(week,team1,team2,game_num=1,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=2,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=3,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=4,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=5,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=6,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=7,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=8,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=9,favored=1,spread=0.5)
        add_game(week,team1,team2,game_num=10,favored=1,spread=0.5)
