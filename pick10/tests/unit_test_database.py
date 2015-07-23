# This class sets up a database that can be used for unit testing.  
# The class creates a central location for setting up a database 
# so each unit test doesn't have to reinvent the wheel every time.
from pick10.models import *
from stage_history import main, populate_picks_for_year_week, populate_games_for_year_week, populate_year, populate_player_count
from stage_models import populate_conferences_teams
import random

TEAM1 = 1
TEAM2 = 2
NOT_STARTED = 1
IN_PROGRESS = 2
FINAL = 3

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

    def setup_week_not_started(self,year=1978,week_number=6):
        week = self.setup_week(year,week_number)
        games = [None]*10
        games[0] = self.setup_game(week,1,"Georgia Tech","Clemson",state=NOT_STARTED)
        games[1] = self.setup_game(week,2,"Duke","North Carolina",state=NOT_STARTED)
        games[2] = self.setup_game(week,3,"Virginia","Virginia Tech",state=NOT_STARTED)
        games[3] = self.setup_game(week,4,"Indiana","Maryland",state=NOT_STARTED)
        games[4] = self.setup_game(week,5,"South Carolina","Georgia",state=NOT_STARTED)
        games[5] = self.setup_game(week,6,"Tennessee","Vanderbilt",state=NOT_STARTED)
        games[6] = self.setup_game(week,7,"Auburn","Alabama",state=NOT_STARTED)
        games[7] = self.setup_game(week,8,"Southern California","UCLA",state=NOT_STARTED)
        games[8] = self.setup_game(week,9,"Army","Navy",state=NOT_STARTED)
        games[9] = self.setup_game(week,10,"Notre Dame","Florida State",state=NOT_STARTED)
        brent = self.setup_player(year,'Brent')
        byron = self.setup_player(year,'Byron')
        alice = self.setup_player(year,'Alice')
        joan = self.setup_player(year,'Joan')
        bill = self.setup_player(year,'Bill')
        david = self.setup_player(year,'David')
        amy = self.setup_player(year,'Amy')
        annie = self.setup_player(year,'Annie')
        kevin = self.setup_player(year,'Kevin')
        john = self.setup_player(year,'John')
        for game in games:
            self.setup_pick(brent,game,winner=TEAM1)
            self.setup_pick(byron,game,winner=TEAM1)
            self.setup_pick(alice,game,winner=TEAM1)
            self.setup_pick(joan,game,winner=TEAM1)
            self.setup_pick(bill,game,winner=TEAM1)
            self.setup_pick(david,game,winner=TEAM1)
            self.setup_pick(amy,game,winner=TEAM1)
            self.setup_pick(annie,game,winner=TEAM1)
            self.setup_pick(kevin,game,winner=TEAM1)
            self.setup_pick(john,game,winner=TEAM1)

    def setup_week_not_started_with_defaulters(self,year=1978,week_number=7):
        week = self.setup_week(year,week_number)
        games = [None]*10
        games[0] = self.setup_game(week,1,"Georgia Tech","Clemson",state=NOT_STARTED)
        games[1] = self.setup_game(week,2,"Duke","North Carolina",state=NOT_STARTED)
        games[2] = self.setup_game(week,3,"Virginia","Virginia Tech",state=NOT_STARTED)
        games[3] = self.setup_game(week,4,"Indiana","Maryland",state=NOT_STARTED)
        games[4] = self.setup_game(week,5,"South Carolina","Georgia",state=NOT_STARTED)
        games[5] = self.setup_game(week,6,"Tennessee","Vanderbilt",state=NOT_STARTED)
        games[6] = self.setup_game(week,7,"Auburn","Alabama",state=NOT_STARTED)
        games[7] = self.setup_game(week,8,"Southern California","UCLA",state=NOT_STARTED)
        games[8] = self.setup_game(week,9,"Army","Navy",state=NOT_STARTED)
        games[9] = self.setup_game(week,10,"Notre Dame","Florida State",state=NOT_STARTED)
        brent = self.setup_player(year,'Brent')
        byron = self.setup_player(year,'Byron')
        alice = self.setup_player(year,'Alice')
        joan = self.setup_player(year,'Joan')
        bill = self.setup_player(year,'Bill')
        david = self.setup_player(year,'David')
        amy = self.setup_player(year,'Amy')
        annie = self.setup_player(year,'Annie')
        kevin = self.setup_player(year,'Kevin')
        john = self.setup_player(year,'John')
        for game in games:
            self.setup_pick(brent,game,winner=TEAM1)
            self.setup_pick(byron,game,winner=TEAM1)
            self.setup_pick(alice,game,winner=TEAM1)
            self.setup_pick(joan,game,winner=TEAM1)
            self.setup_pick(bill,game,winner=TEAM1)
            self.setup_pick(david,game,winner=TEAM1)
            self.setup_pick(amy,game,winner=TEAM1)
            self.setup_pick(annie,game,winner=TEAM1)
        for game in games:
            self.setup_pick(kevin,game,winner=0)
            self.setup_pick(john,game,winner=0)

    def setup_week(self,year,week_number):
        year_model = populate_year(year)
        week = add_week(year,week_number)
        return week

    def setup_game(self,week,game_number,team1_name,team2_name,favored=2,spread=0.5,state=FINAL,team1_score=-1,team2_score=-1):
        team1 = get_team(team1_name)
        team2 = get_team(team2_name)
        game = add_game(week,team1,team2,gamenum=game_number,favored=favored,spread=spread)
        game.game_state = state
        game.team1_actual_points = team1_score
        game.team2_actual_points = team2_score
        game.save()
        return game

    def setup_player(self,year,public_name,private_name=None,ss_name=None):
        private = public_name if private_name == None else private_name
        ss = public_name if ss_name == None else ss_name
        player = Player.objects.get_or_create(public_name=public_name, private_name=private, ss_name=ss)[0]
        year_model = Year.objects.get_or_create(yearnum=year)[0]
        player_year = PlayerYear.objects.get_or_create(player=player,year=year_model)[0]
        return player

    def setup_pick(self,player,game,winner):
        pick = add_pick(player,game,winner)
        return pick

    def setup_random_pick(self,player,game):
        winner = random.randint(1,2)

        if game.gamenum == 10:
            team1_points = random.randint(0,50)
            team2_points = random.randint(0,50)
            pick = add_pick(player,game,winner,team1_points,team2_points)
        else:
            pick = add_pick(player,game,winner)

        return pick

    def setup_player_with_random_picks(self,year,player_name,games):
        player = self.setup_player(year,player_name,player_name)
        for game in games:
            self.setup_random_pick(player,game)

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
