# This class sets up a database that can be used for unit testing.  
# The class creates a central location for setting up a database 
# so each unit test doesn't have to reinvent the wheel every time.
from pick10.models import *
from pick10.calculator import *
from stage_history import main, populate_picks_for_year_week, populate_games_for_year_week, populate_year, populate_player_count
from stage_models import populate_conferences_teams
import random

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

    def setup_week_in_progress(self,year=1978,week_number=8):
        week = self.setup_week(year,week_number)
        games = [None]*10
        games[0] = self.setup_game_with_winner(week,1,"Georgia Tech","Clemson",state=FINAL,winner=TEAM1)
        games[1] = self.setup_game_with_winner(week,2,"Duke","North Carolina",state=FINAL,winner=TEAM1)
        games[2] = self.setup_game_with_winner(week,3,"Virginia","Virginia Tech",state=FINAL,winner=TEAM1)
        games[3] = self.setup_game_with_winner(week,4,"Indiana","Maryland",state=FINAL,winner=TEAM2)
        games[4] = self.setup_game_with_winner(week,5,"South Carolina","Georgia",state=FINAL,winner=TEAM2)
        games[5] = self.setup_game_with_winner(week,6,"Tennessee","Vanderbilt",state=FINAL,winner=TEAM2)
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
        self.setup_player_picks(brent,games,number_of_wins=6)
        self.setup_player_picks(byron,games,number_of_wins=6)
        self.setup_player_picks(alice,games,number_of_wins=5)
        self.setup_player_picks(joan,games,number_of_wins=5)
        self.setup_player_picks(bill,games,number_of_wins=4)
        self.setup_player_picks(david,games,number_of_wins=4)
        self.setup_player_picks(amy,games,number_of_wins=3)
        self.setup_player_picks(annie,games,number_of_wins=3)
        self.setup_player_picks(kevin,games,number_of_wins=1)
        self.setup_player_default(john,games)

    def setup_week_in_progress_games_in_progress(self,year=1978,week_number=9):
        week = self.setup_week(year,week_number)
        games = [None]*10
        games[0] = self.setup_game_with_winner(week,1,"Georgia Tech","Clemson",state=FINAL,winner=TEAM1)
        games[1] = self.setup_game_with_winner(week,2,"Duke","North Carolina",state=FINAL,winner=TEAM1)
        games[2] = self.setup_game_with_winner(week,3,"Virginia","Virginia Tech",state=FINAL,winner=TEAM1)
        games[3] = self.setup_game_with_winner(week,4,"Indiana","Maryland",state=FINAL,winner=TEAM2)
        games[4] = self.setup_game_with_winner(week,5,"South Carolina","Georgia",state=FINAL,winner=TEAM2)
        games[5] = self.setup_game_with_winner(week,6,"Tennessee","Vanderbilt",state=FINAL,winner=TEAM2)
        games[6] = self.setup_game_with_winner(week,7,"Auburn","Alabama",state=IN_PROGRESS,winner=TEAM1)
        games[7] = self.setup_game_with_winner(week,8,"Southern California","UCLA",state=IN_PROGRESS,winner=TEAM2)
        games[8] = self.setup_game_with_winner(week,9,"Army","Navy",state=IN_PROGRESS,winner=TEAM1)
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
        self.setup_player_picks_projected(brent,games,wins=6,projected=9)
        self.setup_player_picks_projected(byron,games,wins=6,projected=8)
        self.setup_player_picks_projected(alice,games,wins=5,projected=8)
        self.setup_player_picks_projected(joan,games,wins=5,projected=6)
        self.setup_player_picks_projected(bill,games,wins=4,projected=7)
        self.setup_player_picks_projected(david,games,wins=4,projected=5)
        self.setup_player_picks_projected(amy,games,wins=3,projected=5)
        self.setup_player_picks_projected(annie,games,wins=3,projected=4)
        self.setup_player_picks_projected(kevin,games,wins=1,projected=2)
        self.setup_player_default(john,games)

    def setup_week_final(self,year=1978,week_number=10):
        week = self.setup_week(year,week_number)
        games = [None]*10
        games[0] = self.setup_game_with_winner(week,1,"Georgia Tech","Clemson",state=FINAL,winner=TEAM1)
        games[1] = self.setup_game_with_winner(week,2,"Duke","North Carolina",state=FINAL,winner=TEAM2)
        games[2] = self.setup_game_with_winner(week,3,"Virginia","Virginia Tech",state=FINAL,winner=TEAM1)
        games[3] = self.setup_game_with_winner(week,4,"Indiana","Maryland",state=FINAL,winner=TEAM2)
        games[4] = self.setup_game_with_winner(week,5,"South Carolina","Georgia",state=FINAL,winner=TEAM1)
        games[5] = self.setup_game_with_winner(week,6,"Tennessee","Vanderbilt",state=FINAL,winner=TEAM2)
        games[6] = self.setup_game_with_winner(week,7,"Auburn","Alabama",state=FINAL,winner=TEAM1)
        games[7] = self.setup_game_with_winner(week,8,"Southern California","UCLA",state=FINAL,winner=TEAM2)
        games[8] = self.setup_game_with_winner(week,9,"Army","Navy",state=FINAL,winner=TEAM1)
        games[9] = self.setup_game_with_winner(week,10,"Notre Dame","Florida State",state=FINAL,winner=TEAM2)
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

    # pool not started has no games yet
    def setup_pool_not_started(self,year=1975):
        week = self.setup_week(year,week_number=1)
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

    def setup_week(self,year,week_number):
        year_model = populate_year(year)
        week, created = Week.objects.get_or_create(year=year_model, weeknum=week_number)
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

    def setup_game_with_winner(self,week,game_number,team1_name,team2_name,winner,state=FINAL):
        assert state == IN_PROGRESS or state == FINAL,"game state should be in progress or final"
        favored,spread,team1_score,team2_score = self.__compute_game_winner(winner)
        game = self.setup_game(week,game_number,team1_name,team2_name,favored,spread,state,team1_score,team2_score)
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

    def setup_player_default(self,player,games):
        for game in games:
            self.setup_pick(player,game,winner=0)

    def setup_player_picks_projected(self,player,games,wins=0,projected=0):
        not_started = sum([ 1 for g in games if g.game_state == NOT_STARTED ])
        ahead = projected - wins - not_started
        self.setup_player_picks(player,games,number_of_wins=wins,number_ahead=ahead)

    def setup_player_picks(self,player,games,number_of_wins=0,number_ahead=0):
        wins_left = number_of_wins
        ahead_left = number_ahead
        for game in games:

            if game.game_state == FINAL:
                make_pick_win = wins_left > 0
                game_winner = self.__determine_game_winner(game)
                assert game_winner == TEAM1 or game_winner == TEAM2

                if make_pick_win:
                    self.setup_pick(player,game,winner=game_winner)
                    wins_left -= 1
                else:
                    game_loser = TEAM1 if game_winner == TEAM2 else TEAM2
                    self.setup_pick(player,game,winner=game_loser)

            elif game.game_state == IN_PROGRESS:
                make_pick_ahead = ahead_left > 0
                ahead = self.__determine_game_team_ahead(game)
                assert ahead == TEAM1 or ahead == TEAM2

                if make_pick_ahead:
                    self.setup_pick(player,game,winner=ahead)
                    ahead_left -= 1
                else:
                    behind = TEAM1 if ahead == TEAM2 else TEAM2
                    self.setup_pick(player,game,winner=behind)

            elif game.game_state == NOT_STARTED:
                self.setup_pick(player,game,winner=TEAM1)

        assert wins_left == 0,'number of wins constraint not satisfied'
        assert ahead_left == 0,'number ahead constraint not satisfied'

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

    def __compute_game_winner(self,winner):
        favored = winner
        spread = 0.5
        if winner == TEAM1:
            team1_score = 25
            team2_score = 20
        else:
            team1_score = 15
            team2_score = 30
        return favored,spread,team1_score,team2_score

    def __determine_game_winner(self,game):
        calc = CalculateResults(None)
        return calc.get_pool_game_winner(game)

    def __determine_game_team_ahead(self,game):
        calc = CalculateResults(None)
        return calc.get_team_winning_pool_game(game)

    # TODO
    # week with no games started
    # week with some games in progress
    # week with mixture of not_started, in_progress, final
    # week with all games final
    # player with no picks
    # player with 0 wins
    # player with 10 wins
    # player with mix of wins/losses
