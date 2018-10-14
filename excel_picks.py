import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collegefootballpick10.settings')

import django
django.setup()

import sys
#from pick10.database import *
#from pick10.models import *
from pick10.database import Database
from pick10.models import get_week
import pandas as pd

def bad_year_or_week_number(year,week_number):
    try:
        year_int = int(year)
        week_int = int(week_number)
        w = get_week(year_int,week_int)
    except Exception:
        return True
    return False

def load_week_data(year,week_number):
    d = Database()
    data = d.load_week_data(year,week_number)
    return data

def print_player_names(data):
    players = sorted(data.players.values(),key=lambda player:player.ss_name)
    print("Players (%d)" % (len(players)))
    print("-------------------")
    for player in players:
        print(player.ss_name)
    print("")

def print_player_picks(player_id,data):
    player = data.players[player_id]
    picks = { pick.game.gamenum:pick for pick in data.player_picks[player_id] }

    print("%s Picks" % (player.ss_name))
    print("----------------------------")

    for game_number in range(1,11):
        pick = picks[game_number]

        if pick.winner == 0:
            pick_string = "default"
        elif pick.winner == 1:
            pick_string = "team1"
        elif pick.winner == 2:
            pick_string = "team2"
        else:
            pick_string = "ERROR: winner=%s" % (pick.winner)

        print("Game %d: %s" % (game_number,pick_string))
    print("")

def print_all_player_picks(data):
    # sort player id's by their ss_name
    players = sorted(data.players.values(),key=lambda player:player.ss_name)
    player_ids = [ p.id for p in players ]

    for player_id in player_ids:
        print_player_picks(player_id,data)

def get_picks_column(player_id,data):
    player = data.players[player_id]

    no_picks = player.id not in data.player_picks
    if no_picks:
        column = [''] * 12
        return column

    picks = { pick.game.gamenum:pick for pick in data.player_picks[player_id] }

    column = []

    for game_number in range(1,11):
        pick = picks[game_number]

        if pick.winner == 0:
            column.append('')
            column.append('')
        elif pick.winner == 1:
            column.append('x')
            column.append('')
        elif pick.winner == 2:
            column.append('')
            column.append('x')
        else:
            raise AssertionError,"invalid winner value"

        if game_number == 10:
            if pick.winner == 0:
                column.append('')
                column.append('')
            else:
                column.append(pick.team1_predicted_points)
                column.append(pick.team2_predicted_points)

    return column

def get_games_column(data):
    column = []
    for game_number in range(1,11):
        game = data.games[game_number]
        column.append(game.team1.team_name)
        column.append(game.team2.team_name)

        if game_number == 10:
            column.append("%s - score" % (game.team1.team_name))
            column.append("%s - score" % (game.team2.team_name))
    return column

def get_game_row(data,df,game_number,team_number,game10_score_row=False):
    assert team_number == 1 or team_number == 2,"Unexpected team number"
    assert game_number in [1,2,3,4,5,6,7,8,9,10],"Unexpected game number"

    game = data.games[game_number]
    if team_number == 1:
        team_name = game.team1.team_name
    elif team_number == 2:
        team_name = game.team2.team_name

    if game_number == 10 and game10_score_row:
        row_name = '%s - score' % (team_name)
    else:
        row_name = team_name

    assert row_name in df.index,"Could not find game row in dataframe"

    return row_name


def create_picks_sheet(year,week_number,data):
    favorite_column = 'Favorite by:'
    score_column = 'Actual Score'

    player_names = sorted([ p.ss_name for p in data.players.values() ])
    games = get_games_column(data)
    columns = [favorite_column,score_column] + player_names
    picks_df = pd.DataFrame(columns=columns,index=games)

    # add the player picks
    for player_id in data.players:
        player = data.players[player_id]
        column_data = get_picks_column(player_id,data)
        if len(column_data) < 22:
            column_data = ['' for i in range(22)]
        picks_df[player.ss_name] = column_data

    # add the game favored/spread and team scores
    game_numbers = [ number for number in data.games.keys() ]
    assert game_numbers == [1,2,3,4,5,6,7,8,9,10], "Games 1 thru 10 not found in data"

    for game_num in range(1,11):
        game = data.games[game_num]

        team1_row = get_game_row(data,picks_df,game_num,team_number=1)
        team2_row = get_game_row(data,picks_df,game_num,team_number=2)

        # fill in the favored team
        if game.favored == 1:
            picks_df[favorite_column][team1_row] = game.spread
        elif game.favored == 2:
            picks_df[favorite_column][team2_row] = game.spread
        else:
            print("Favored info not available")

        # fill in the scores if available
        score_not_entered = game.team1_actual_points < 0 and game.team2_actual_points < 0
        score_entered = game.team1_actual_points >= 0 and game.team2_actual_points >= 0
        assert score_not_entered or score_entered, "Team score for game %d in inconsistent state" % (game_num)

        if score_entered:
            picks_df[score_column][team1_row] = game.team1_actual_points
            picks_df[score_column][team2_row] = game.team2_actual_points

            if game_num == 10:  # game 10 requires score filled in on 2 rows
                team1_score_row = get_game_row(data,picks_df,game_num,team_number=1,game10_score_row=True)
                team2_score_row = get_game_row(data,picks_df,game_num,team_number=2,game10_score_row=True)
                picks_df[score_column][team1_score_row] = game.team1_actual_points
                picks_df[score_column][team2_score_row] = game.team2_actual_points

    filefolder = r'excel_history/picks'
    filename = os.path.join(filefolder, 'picks_%d_%d.xls' % (year,week_number))
    sheet = 'week_%d' % (week_number)
    picks_df.to_excel(filename,sheet)

if __name__ == '__main__':
    # get input arguments and verify they are valid
    if len(sys.argv) != 3:
        print("usage:  python excel_picks.py <year> <week number>")
        sys.exit(1)

    year = sys.argv[1]
    week_number = sys.argv[2]

    if bad_year_or_week_number(year,week_number):
        print("invalid year or week number")
        sys.exit(1)

    year = int(sys.argv[1])
    week_number = int(sys.argv[2])

    # load the week data
    data = load_week_data(year,week_number)
    create_picks_sheet(year,week_number,data)
