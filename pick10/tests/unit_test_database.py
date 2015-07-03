# This class sets up a database that can be used for unit testing.  
# The class creates a central location for setting up a database 
# so each unit test doesn't have to reinvent the wheel every time.
from pick10.models import *
from stage_history import populate_conferences_teams, populate_players, populate_games_for_year, populate_picks_for_year_week, populate_picks

class UnitTestDatabase:

    def __init__(self):
        populate_conferences_teams()

    def setup_simple_week(self,year=2014,week_number=1):
        week = self.setup_week(year,week_number)
        self.setup_game(week,1,"Georgia Tech","Clemson",favored=1,spread=0.5)
        self.setup_game(week,2,"Duke","North Carolina",favored=2,spread=1.5)
        self.setup_game(week,3,"Virginia","Virginia Tech",favored=1,spread=7.5)
        self.setup_game(week,4,"Indiana","Maryland",favored=2,spread=3.5)
        self.setup_game(week,5,"South Carolina","Georgia",favored=1,spread=9.5)
        self.setup_game(week,6,"Tennessee","Vanderbilt",favored=2,spread=11.5)
        self.setup_game(week,7,"Auburn","Alabama",favored=1,spread=1.5)
        self.setup_game(week,8,"Southern Cal","UCLA",favored=2,spread=4.5)
        self.setup_game(week,9,"Army","Navy",favored=2,spread=5.5)
        self.setup_game(week,10,"Notre Dame","Florida State",favored=1,spread=0.5)
        self.setup_player(year,'Brent','BrentH')
        self.setup_player(year,'John','JohnH')

    def load_historical_data_for_year(self,year=2014):
        populate_players([year])
        populate_games_for_year(year)
        populate_picks([year])
        self.fail('Need to change Users/Players (move to init?)')

    def load_historical_data_for_week(self,year=2014,week_number=1):
        populate_players([year])
        populate_games_for_year(year)
        populate_picks_for_year_week(year,week_number)
        self.fail('Need to change Users/Players (move to init?)')
        self.fail('Need to change populate_games to only games in a week')

    def setup_week(self,year,week_number):
        (year_model,created) = Year.objects.get_or_create(yearnum=year)
        week = add_week(year,week_number)
        return week

    def setup_game(self,week,game_number,team1_name,team2_name,favored,spread):
        team1 = get_team(team1_name)
        team2 = get_team(team2_name)
        game = add_game(week,team1,team2,gamenum=game_number,favored=favored,spread=spread)
        return game

    def setup_player(self,year,public_name,private_name=''):
        player = add_player(public_name,private_name)
        year_model = Year.objects.get_or_create(yearnum=year)[0]
        player_year = PlayerYear.objects.create(player=player,year=year_model)
        return player
