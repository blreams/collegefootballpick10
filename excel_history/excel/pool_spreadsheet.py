import os as _os
import re as _re
from xlrd import *
from player import *
from game import *
from pick import *
from team import *

class PoolSpreadsheet:

    def __init__(self,year):
        self.spreadsheet_name = self.get_spreadsheet_path_by_year(year)
        self.__wb = open_workbook(self.spreadsheet_name)
        self.year = year
        self.__players = None
        self.__week_games = dict()
        self.__week_picks = dict()
        self.__teams = None

    def get_spreadsheet_path_by_year(self, year):
        dirname = _os.getcwd() + '/excel_history/data/'
        RE_FILE_SS = _re.compile(r'^pool_(\d{4})_standings.xls')
        filelist = [f for f in _os.listdir(dirname) if RE_FILE_SS.match(f) and str(year) in f]

        if len(filelist) != 1:
            raise AssertionError, 'Unable to find matching spreadsheet for %d' % year
        return dirname + filelist[0]

    # depends on what sheets are present
    def get_week_numbers(self):
        weeks = []
        for week_number in range(1,14):
            if self.__get_weekly_sheet(week_number) != None:
                weeks.append(week_number)
        return weeks

    ##### Standings sheet
    def get_pool_winner(self):
        players = self.get_players()
        return [ player.name for player in players.values() if player.overall_rank == 1 ]

    def get_players(self):
        if self.__players != None:
            return self.__players

        first_player_row = 7 
 
        sheet = self.__get_sheet("Standings") 
 
        players = dict()
        for row in range(first_player_row,sheet.nrows): 
            player = self.__get_player_info(sheet,row)
            players[player.name] = player

        self.__players = players
        return players 

    def get_player_info(self,player_name):
        players = self.get_players()
        return players.get(player_name)

    def get_player_names(self):
        players = self.get_players()
        return sorted(players.keys())

    def get_player_overall_rank(self,player_name):
        player = self.get_player_info(player_name)
        if player is None:
            return None
        return player.overall_rank

    def get_player_overall_points(self,player_name):
        player = self.get_player_info(player_name)
        if player is None:
            return None
        return player.overall_points

    def get_player_week_points(self,player_name,week_number):
        player = self.get_player_info(player_name)
        if player is None:
            return None
        return player.week_points.get(week_number)

    ##### Week sheet
    def get_games(self,week_number):
        if week_number in self.__week_games:
            return self.__week_games[week_number]

        sheet = self.__get_weekly_sheet(week_number)
        games = dict()
        for game_number in range(1,11):
            games[game_number] = self.__get_game_info(sheet,game_number)

        self.__week_games[week_number] = games
        return games

    def get_picks(self,week_number):
        if week_number in self.__week_picks:
            return self.__week_picks[week_number]

        first_player_column = 10
        sheet = self.__get_weekly_sheet(week_number)

        picks = []
        for column in range(first_player_column,sheet.ncols):
            picks += self.__get_picks_info(sheet,column)

        self.__week_picks[week_number] = picks
        return picks

    def get_game_info(self,week_number,game_number):
        games = self.get_games(week_number)
        return games.get(game_number)

    def get_game_teams(self,week_number,game_number):
        games = self.get_games(week_number)
        game = games.get(game_number)
        if game is None:
            return None
        return [ game.team1, game.team2 ]

    def get_game_team1(self,week_number,game_number):
        games = self.get_games(week_number)
        game = games.get(game_number)
        if game is None:
            return None
        return game.team1

    def get_game_team2(self,week_number,game_number):
        games = self.get_games(week_number)
        game = games.get(game_number)
        if game is None:
            return None
        return game.team2

    def get_game_spread(self,week_number,game_number):
        games = self.get_games(week_number)
        game = games.get(game_number)
        if game is None:
            return None
        return game.spread

    def get_game_favored_team(self,week_number,game_number):
        games = self.get_games(week_number)
        game = games.get(game_number)
        if game is None:
            return None
        return game.favored

    def get_game_team1_score(self,week_number,game_number):
        games = self.get_games(week_number)
        game = games.get(game_number)
        if game is None:
            return None
        return game.team1_score

    def get_game_team2_score(self,week_number,game_number):
        games = self.get_games(week_number)
        game = games.get(game_number)
        if game is None:
            return None
        return game.team2_score

    def get_game_winner(self,week_number,game_number):
        games = self.get_games(week_number)
        game = games.get(game_number)
        if game is None:
            return None
        return game.winner

    def get_player_pick(self,player_name,week_number,game_number):
        picks = self.get_picks(week_number)
        for pick in picks:
            if pick.player_name == player_name and pick.game_number == game_number:
                return pick.winner
        return None

    def get_player_picks(self,player_name,week_number):
        picks = self.get_picks(week_number)
        return { pick.game_number:pick.winner for pick in picks if pick.player_name == player_name }

    def get_player_points(self,player_name,week_number):
        player_row = 1
        first_player_column = 10
        week_points_row = 24 

        if self.did_player_default(player_name,week_number):
            return 0

        sheet = self.__get_weekly_sheet(week_number)

        for column in range(first_player_column,sheet.ncols):
            column_player_name = str(sheet.cell(player_row,column).value) 
            if column_player_name == player_name:
                week_points = str(sheet.cell(week_points_row,column).value) 
                return int(float(week_points))
        return None

    def did_player_win_game(self,player_name,week_number,game_number):
        player_pick = self.get_player_pick(player_name,week_number,game_number)
        game_winner = self.get_game_winner(week_number,game_number)
        return game_winner == player_pick and (player_pick == "team1" or player_pick == "team2")

    def did_player_lose_game(self,player_name,week_number,game_number):
        player_pick = self.get_player_pick(player_name,week_number,game_number)
        game_winner = self.get_game_winner(week_number,game_number)
        return game_winner != None and (player_pick == None or game_winner != player_pick)

    # default = no tiebreak score
    def did_player_default(self,player_name,week_number):
        picks = self.get_picks(week_number)
        defaults = [ pick.default for pick in picks if pick.player_name == player_name ] 
        return all(defaults)

    def get_players_that_defaulted(self,week_number):
        picks = self.get_picks(week_number)
        defaulters = set([ pick.player_name for pick in picks if pick.default ])
        return sorted(list(defaulters))

    def get_players_that_defaulted_any_week(self):
        weeks = self.get_week_numbers()
        defaulters = []
        for week_number in weeks:
            defaulters += self.get_players_that_defaulted(week_number)
        return list(set(defaulters))

    def get_player_tiebreak_score(self,player_name,week_number):
        picks = self.get_picks(week_number)
        player_picks = { pick.game_number:pick for pick in picks if pick.player_name == player_name }
        game10_pick = player_picks.get(10)
        if game10_pick == None:
            return None
        return {'team1':game10_pick.team1_score,'team2':game10_pick.team2_score}

    def get_week_winner(self,week_number):
        player_row = 1
        first_player_column = 10
        winner_row = 27
        CELL_EMPTY = 0

        sheet = self.__get_weekly_sheet(week_number)

        for column in range(first_player_column,sheet.ncols):
            winner = str(sheet.cell(winner_row,column).value) 
            if sheet.cell_type(winner_row,column) == CELL_EMPTY or winner == "":
                continue

            if float(winner) == 1.0:
                player_name = str(sheet.cell(player_row,column).value) 
                return player_name

        return None

    ##### Conference sheet
    def get_teams(self):
        if self.__teams != None:
            return self.__teams

        row_after,conferences = self.__get_conferences()

        teams = []
        for conference in conferences:
            conference_teams = self.__get_conference_teams(row_after,conference)
            assert conference_teams != None,"Could not find conference %s" % (conference)

            for team_name in conference_teams:
                team = Team()
                team.name = team_name
                team.conference = conference
                teams.append(team)

        self.__teams = teams
        return teams

    def get_conferences(self):
        row_after,conferences = self.__get_conferences()
        return conferences

    def get_team_names(self):
        teams = self.get_teams()
        return [ team.name for team in teams ]

    def get_teams_in_conference(self,conference):
        teams = self.get_teams()
        names = [ team.name for team in teams if team.conference == conference ]
        if len(names) == 0:
            return None
        return names

    # TODO
    def check_for_errors(self):
        # default not True for all games in a week
        # no winner in a week
        # more than one winner in a week
        # conference and teams across years
        pass

    def __get_sheet(self,name):
        for sheet in self.__wb.sheets():
            if sheet.name == name:
                return sheet
        return None

    def __get_weekly_sheet(self,week_number):
        if week_number < 10:
            sheet_name = "Wk0%d" % (week_number)
        else:
            sheet_name = "Wk%d" % (week_number)
        return self.__get_sheet(sheet_name)

    def __get_player_info(self,sheet,row):
        name_column = 1 
        overall_rank_column = 0
        overall_points_column = 3 
        first_week_points_column = 10

        player = Player()
        player.name = str(sheet.cell(row,name_column).value) 
        player.overall_rank = int(sheet.cell(row,overall_rank_column).value)
        player.overall_points = int(sheet.cell(row,overall_points_column).value)
        player.week_points = dict()

        CELL_EMPTY = 0
        for week_number in range(1,14):
            column = first_week_points_column + week_number - 1
            if sheet.cell_type(row,column) == CELL_EMPTY:
                break
            week_points = str(sheet.cell(row,column).value) 
            if week_points == "":
                break
            player.week_points[week_number] = int(float(week_points))

        return player

    def __get_game_info(self,sheet,game_number):
        first_game_row = 2
        team_name_column = 1
        spread_column = 2
        score_column = 3
        win_column = 4

        top_row = first_game_row + (game_number-1) * 2
        bottom_row = top_row + 1

        team1 = str(sheet.cell(top_row,team_name_column).value) 
        team2 = str(sheet.cell(bottom_row,team_name_column).value) 
        team1_score = str(sheet.cell(top_row,score_column).value) 
        team2_score = str(sheet.cell(bottom_row,score_column).value) 
        top_spread = str(sheet.cell(top_row,spread_column).value)
        bottom_spread = str(sheet.cell(bottom_row,spread_column).value)
        top_win = str(sheet.cell(top_row,win_column).value)
        bottom_win = str(sheet.cell(bottom_row,win_column).value)

        game = Game()
        game.number = game_number
        game.team1 = team1
        game.team2 = team2
        game.favored,game.spread = self.__get_favored_and_spread(top_spread,bottom_spread)

        if team1_score == "" and team2_score == "":
            game.team1_score = None
            game.team2_score = None
            game.winner = None
            game.state = "not_started"
        elif top_win == "" and bottom_win == "":
            game.team1_score = int(float(team1_score))
            game.team2_score = int(float(team2_score))
            game.winner = None
            game.state = "in_progress"
        else:
            game.team1_score = int(float(team1_score))
            game.team2_score = int(float(team2_score))
            game.state = "final"

            team1_win = float(top_win) if top_win != "" else None
            team2_win = float(bottom_win) if bottom_win != "" else None

            if team1_win == 1.0 and team2_win == 0.0:
                game.winner = "team1"
            elif team1_win == 0.0 and team2_win == 1.0:
                game.winner = "team2"
            else:
                game.winner = None
                #raise AssertionError,"team1_win=%s,team2_win=%s" % (team1_win,team2_win)

        return game



    def __get_favored_and_spread(self,top_spread,bottom_spread):
        assert not(top_spread == "" and bottom_spread == "")

        if top_spread.strip() != "":
            favored = "team1"
            spread = float(top_spread)
        elif bottom_spread.strip() != "":
            favored = "team2"
            spread = float(bottom_spread)
        else:
            raise AssertionError,"Should not reach here"
        return favored,spread

    def __get_picks_info(self,sheet,column):
        player_row = 1
        first_game_row = 2
        game10_score_top_row = 22
        game10_score_bottom_row = 23
        CELL_EMPTY = 0
        
        player_name = str(sheet.cell(player_row,column).value) 
        if player_name == "":
            return []

        picks = []
        for game_number in range(1,11):
            top_row = first_game_row + (game_number-1) * 2
            bottom_row = top_row + 1

            team1_picked = sheet.cell_type(top_row,column) != CELL_EMPTY
            team2_picked = sheet.cell_type(bottom_row,column) != CELL_EMPTY
            assert (team1_picked and team2_picked) == False

            pick = Pick()
            pick.player_name = player_name
            pick.game_number = game_number
            pick.team1_score = None
            pick.team2_score = None
            pick.default = False

            if team1_picked:
                pick.winner = "team1"
            elif team2_picked:
                pick.winner = "team2"
            else:
                pick.winner = None

            picks.append(pick)

        team1_score = str(sheet.cell(game10_score_top_row,column).value) 
        team2_score = str(sheet.cell(game10_score_bottom_row,column).value) 
        default = team1_score == '' and team2_score == ''

        if default:
            for i in range(len(picks)):
                picks[i].winner = None
                picks[i].default = True
        else:
            for i in range(len(picks)):
                if picks[i].game_number == 10:
                    picks[i].team1_score = 0 if team1_score == '' else int(float(team1_score))
                    picks[i].team2_score = 0 if team2_score == '' else int(float(team2_score))

        return picks

    def __get_conferences(self):
        conference_first_row = 0
        conference_column = 0

        sheet = self.__get_sheet("Conference")
        while True:
            row = conference_first_row
            col = conference_column
            conference = str(sheet.cell(row,col).value)
            if conference:
                break
            conference_first_row += 1


        row = conference_first_row
        conferences = []
        while True:
            conference = str(sheet.cell(row,conference_column).value)
            row += 1
            if conference == "":
                break
            conferences.append(conference)
        return row,conferences

    def __get_conference_teams(self,row_to_start_from,conference):
        name_column = 0

        sheet = self.__get_sheet("Conference")

        # find the conference
        conference_row = None
        for row in range(row_to_start_from,sheet.nrows): 
            conference_cell = str(sheet.cell(row,name_column).value)
            if conference_cell == conference:
                conference_row = row
                break
        if conference_row == None:
            return None

        # get the teams
        teams = []
        for row in range(conference_row+1,sheet.nrows): 
            team_cell = str(sheet.cell(row,name_column).value)
            if team_cell == "":
                break
            teams.append(team_cell)
        return teams
