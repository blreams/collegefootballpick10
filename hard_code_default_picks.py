# This script will update PlayerWeekStat and PlayerYearStat as needed
import os
import sys
import six
import argparse

# Apparently this stuff has to be done before you can do django app imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collegefootballpick10.settings')
import django
from django.conf import settings
django.setup()

from django.core.exceptions import ObjectDoesNotExist
from pick10.models import Pick, get_yearlist

from excel_history.excel.pool_spreadsheet import PoolSpreadsheet

SCRIPT_TEST = False
arguments = argparse.Namespace()

def parse_arguments(args):
    global arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true', default=False, help="Run in debug mode")
    parser.add_argument('--year', '-y', action='append', type=int, default=[], help="Choose year for query")
    parser.add_argument('--query', '-q', choices=['get_defaults',], default='get_defaults', help="Get default picks from DB, return list of tuples")
    #parser.add_argument('--update', '-u', choices=['update', 'all'], default='update', help="Perform an update")
    arguments = parser.parse_args(args)

def get_defaults():
    yearnums = set([y for y in get_yearlist() if y <= 2016]) # 2016 was last year we used spreadsheets
    if arguments.year:
        yearnums &= set(arguments.year)

    picks = Pick.objects.filter(game__week__year__yearnum__in=yearnums).filter(winner=0).order_by('player', 'game__week__year', 'game__week__weeknum', 'game__gamenum')

    pool_spreadsheets = {}
    for yearnum in yearnums:
        pool_spreadsheets[yearnum] = PoolSpreadsheet(yearnum)

    retval = []
    for pick in picks:
        player = pick.player.ss_name
        year = pick.game.week.year.yearnum
        week = pick.game.week.weeknum
        game = pick.game.gamenum
        picked_team = pool_spreadsheets[year].get_picks(week_number=week, playername=player, bypass_defaults=True)[game-1].winner
        winner = 0
        if picked_team == 'team1':
            winner = 1
        elif picked_team == 'team2':
            winner = 2
        retval.append((player, year, week, game, winner))
    return retval

def perform_action():
    if arguments.query == 'get_defaults':
        print('\n'.join(map(str, get_defaults())))

def main(args=''):
    global arguments
    if not args:
        args = ['--help']
    if isinstance(args, six.string_types):
        args = args.split()

    parse_arguments(args)
    perform_action()

if __name__ == "__main__":
    main(args=sys.argv[1:])

