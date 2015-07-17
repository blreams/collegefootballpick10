# This class sets up a database that can be used for unit testing.  
# The class creates a central location for setting up a database 
# so each unit test doesn't have to reinvent the wheel every time.
from pick10.models import *
from stage_history import main, populate_picks_for_year_week, populate_games_for_year_week, populate_year, populate_player_count
from stage_models import populate_conferences_teams

TEAM1 = 1
TEAM2 = 2

class UnitTestDatabase:

    def __init__(self):
        populate_conferences_teams()

    def setup_simple_week(self,year=2014,week_number=1):
        week = self.setup_week(year,week_number)
        game1 = self.setup_game(week,1,"Georgia Tech","Clemson",favored=1,spread=0.5)
        game2 = self.setup_game(week,2,"Duke","North Carolina",favored=2,spread=1.5)
        game3 = self.setup_game(week,3,"Virginia","Virginia Tech",favored=1,spread=7.5)
        game4 = self.setup_game(week,4,"Indiana","Maryland",favored=2,spread=3.5)
        game5 = self.setup_game(week,5,"South Carolina","Georgia",favored=1,spread=9.5)
        game6 = self.setup_game(week,6,"Tennessee","Vanderbilt",favored=2,spread=11.5)
        game7 = self.setup_game(week,7,"Auburn","Alabama",favored=1,spread=1.5)
        game8 = self.setup_game(week,8,"Southern California","UCLA",favored=2,spread=4.5)
        game9 = self.setup_game(week,9,"Army","Navy",favored=2,spread=5.5)
        game10 = self.setup_game(week,10,"Notre Dame","Florida State",favored=1,spread=0.5)
        brent = self.setup_player(year,'Brent','BrentH')
        add_pick(brent,game1,TEAM1)
        add_pick(brent,game2,TEAM2)
        add_pick(brent,game3,TEAM1)
        add_pick(brent,game4,TEAM2)
        add_pick(brent,game5,TEAM1)
        add_pick(brent,game6,TEAM2)
        add_pick(brent,game7,TEAM1)
        add_pick(brent,game8,TEAM2)
        add_pick(brent,game9,TEAM1)
        add_pick(brent,game10,TEAM2,17,10)
        john = self.setup_player(year,'John','JohnH')
        add_pick(john,game1,TEAM1)
        add_pick(john,game2,TEAM2)
        add_pick(john,game3,TEAM2)
        add_pick(john,game4,TEAM2)
        add_pick(john,game5,TEAM1)
        add_pick(john,game6,TEAM1)
        add_pick(john,game7,TEAM1)
        add_pick(john,game8,TEAM2)
        add_pick(john,game9,TEAM2)
        add_pick(john,game10,TEAM2,7,21)

    def load_historical_data_for_year(self,year=2014):
        main(years=[year])

    def load_historical_data_for_week(self,year=2014,week_number=1):
        main(years=[year],weeks=[week_number])

    def setup_week(self,year,week_number):
        year_model = populate_year(year)
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

    def delete_database(self):
        Year.objects.all().delete()
        Team.objects.all().delete()
        Player.objects.all().delete()
        PlayerYear.objects.all().delete()
        Conference.objects.all().delete()
        Week.objects.all().delete()
        Game.objects.all().delete()
        Pick.objects.all().delete()

    # TODO
    # week with no games started
    # week with some games in progress
    # week with mixture of not_started, in_progress, final
    # week with all games final
    # player with no picks
    # player with 0 wins
    # player with 10 wins
    # player with mix of wins/losses
