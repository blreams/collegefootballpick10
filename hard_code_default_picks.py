# This script will update PlayerWeekStat and PlayerYearStat as needed
import os
import sys
import six
import argparse
from collections import namedtuple

# Apparently this stuff has to be done before you can do django app imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collegefootballpick10.settings')
import django
from django.conf import settings
django.setup()

from django.core.exceptions import ObjectDoesNotExist
from pick10.models import Pick, Week, get_yearlist, get_player_by_private_name

from excel_history.excel.pool_spreadsheet import PoolSpreadsheet

SCRIPT_TEST = False
arguments = argparse.Namespace()

PickTuple = namedtuple('PickTuple', ['ss_name', 'year', 'week', 'game', 'winner',])
WeekTuple = namedtuple('WeekTuple', ['year', 'week', 'winner',])
query_choices = [
        'get_defaults',
        'update_nonzero_defaults',
        'get_winners',
        ]

def parse_arguments(args):
    global arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true', default=False, help="Run in debug mode")
    parser.add_argument('--year', '-y', action='append', type=int, default=[], help="Choose year for query")
    parser.add_argument('--player', '-p', action='append', default=[], help="Choose player (private_name, use underscore to separate first_last) for query")
    parser.add_argument('--query', '-q', choices=query_choices, default='get_defaults', help="Get default picks from DB, return list of tuples")
    arguments = parser.parse_args(args)

def process_arguments():
    global arguments
    arguments.yearnums = set([y for y in get_yearlist() if y <= 2016]) # 2016 was last year we used spreadsheets
    if arguments.year:
        arguments.yearnums &= set(arguments.year)

    arguments.player_ids = [get_player_by_private_name(private_name.replace('_', ' ')).id for private_name in arguments.player]

def get_defaults():
    if not arguments.player_ids:
        picks = Pick.objects.filter(game__week__year__yearnum__in=arguments.yearnums).filter(winner=0).order_by('player', 'game__week__year', 'game__week__weeknum', 'game__gamenum')
    else:
        picks = Pick.objects.filter(
            game__week__year__yearnum__in=arguments.yearnums,
            player__id__in=arguments.player_ids,
            ).filter(winner=0).order_by('player', 'game__week__year', 'game__week__weeknum', 'game__gamenum')

    pool_spreadsheets = {}
    for yearnum in arguments.yearnums:
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
        retval.append(PickTuple(player, year, week, game, winner))
    return retval

def update_nonzero_defaults(pick_tuples):
    print("Updating {} picks...".format(len(pick_tuples)))
    for i, pick_tuple in enumerate(pick_tuples):
        if i % 100 == 99:
            print("Updated {} picks...".format(i+1))
        pick = Pick.objects.get(
            player__ss_name=pick_tuple.ss_name,
            game__week__year__yearnum=pick_tuple.year,
            game__week__weeknum=pick_tuple.week,
            game__gamenum=pick_tuple.game
            )
        pick.winner = pick_tuple.winner
        if not arguments.debug:
            pick.save()
        else:
            print("Saving Pick({})...".format(pick_tuple))

def get_winners():
    weeks = Week.objects.filter(year__yearnum__in=arguments.yearnums).order_by('year', 'weeknum')

    retval = []
    for week in weeks:
        winner = week.winner.private_name
        year = week.year.yearnum
        week = week.weeknum
        retval.append(WeekTuple(year, week, winner))
    return retval

def perform_action():
    if arguments.query == 'get_defaults':
        print('\n'.join(map(str, get_defaults())))
    elif arguments.query == 'update_nonzero_defaults':
        pick_tuples = get_defaults()
        update_nonzero_defaults(pick_tuples)
    elif arguments.query == 'get_winners':
        print('\n'.join(map(str, get_winners())))

def main(args=''):
    global arguments
    if not args:
        args = ['--help']
    if isinstance(args, six.string_types):
        args = args.split()

    parse_arguments(args)
    process_arguments()
    perform_action()

if __name__ == "__main__":
    main(args=sys.argv[1:])

