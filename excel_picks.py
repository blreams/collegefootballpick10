import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collegefootballpick10.settings')

import django
django.setup()

import sys
from pick10.database import *
from pick10.models import *
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
    print "Players (%d)" % (len(players))
    print "-------------------"
    for player in players:
        print player.ss_name
    print ""

def print_player_picks(player_id,data):
    player = data.players[player_id]
    picks = { pick.game.gamenum:pick for pick in data.player_picks[player_id] }

    print "%s Picks" % (player.ss_name)
    print "----------------------------"

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

        print "Game %d: %s" % (game_number,pick_string)
    print ""

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

def create_picks_sheet(year,week_number,data):
    player_names = sorted([ p.ss_name for p in data.players.values() ])
    games = get_games_column(data)
    picks_df = pd.DataFrame(columns=player_names,index=games)

    for player_id in data.players:
        player = data.players[player_id]
        column_data = get_picks_column(player_id,data)
        if len(column_data) < 22:
            column_data = ['' for i in range(22)]
        picks_df[player.ss_name] = column_data

    filename = 'picks_%d_%d.xls' % (year,week_number)
    sheet = 'week_%d' % (week_number)
    picks_df.to_excel(filename,sheet)

if __name__ == '__main__':
    # get input arguments and verify they are valid
    if len(sys.argv) != 3:
        print "usage:  python excel_picks.py <year> <week number>"
        sys.exit(1)

    year = sys.argv[1]
    week_number = sys.argv[2]

    if bad_year_or_week_number(year,week_number):
        print "invalid year or week number"
        sys.exit(1)

    year = int(sys.argv[1])
    week_number = int(sys.argv[2])

    # load the week data
    data = load_week_data(year,week_number)
    create_picks_sheet(year,week_number,data)
