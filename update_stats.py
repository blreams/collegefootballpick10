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
from pick10.models import Player, Week, PlayerWeekStat
from pick10.models import get_yearlist, get_weeklist, get_player_id_list_by_year, get_player_id_with_stats_list
from pick10.models import calc_player_week_points_picks_winner, get_last_week_with_winner, get_playeryears_by_id

SCRIPT_TEST = False
arguments = argparse.Namespace()

def parse_arguments(args):
    global arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true', default=False, help="Run in debug mode")
    parser.add_argument('--player', '-p', type=int, default=None, help="Player number, default is all players")
    parser.add_argument('--week', '-w', type=int, default=None, help="Week, default is all weeks")
    parser.add_argument('--year', '-y', type=int, default=None, help="Year, default is all years")
    parser.add_argument('--update', '-u', choices=['update', 'all'], default='update', help="Perform an update")
    arguments = parser.parse_args(args)

def update_database():
    latest_year = get_yearlist()[-1]
    latest_week = get_last_week_with_winner(latest_year)
    if latest_week == 0:
        return
    player_set = set(get_player_id_list_by_year(latest_year))
    player_with_stat_set = set(get_player_id_with_stats_list(latest_year, latest_week))
    player_update_set = player_set - player_with_stat_set
    update_list = []
    for player_id in player_update_set:
        try:
            player = Player.objects.get(id=player_id)
            week = Week.objects.get(year__yearnum=latest_year, weeknum=latest_week)
        except ObjectDoesNotExist:
            continue
        add_to_database(player, week)

def refresh_database():
    weeknums = set(range(1, 14))
    yearnums = set()
    player_ids = set([p.id for p in Player.objects.all()])
    if arguments.player:
        player_ids &= set([arguments.player])
    for player in player_ids:
        yearnums |= set(get_playeryears_by_id(player))
    if arguments.year:
        yearnums &= set([arguments.year])
    if arguments.week:
        weeknums &= set([arguments.week])

    for player_id in player_ids:
        try:
            player = Player.objects.get(id=player_id)
        except ObjectDoesNotExist:
            continue
        for yearnum in set(get_playeryears_by_id(player_id)) & yearnums:
            for weeknum in set(get_weeklist(yearnum, only_locked_scores=True)) & weeknums:
                try:
                    week = Week.objects.get(year__yearnum=yearnum, weeknum=weeknum)
                except ObjectDoesNotExist:
                    continue
                add_to_database(player, week)

def add_to_database(player, week):
    points, picks, winner = calc_player_week_points_picks_winner(player.id, week.year.yearnum, week.weeknum)
    if winner is None:
        print("WARNING: Year {} Week {} has no winner".format(week.year.yearnum, week.weeknum))
        return
    if not arguments.debug:
        pws, created = PlayerWeekStat.objects.get_or_create(player=player, week=week)
        pws.score = points
        pws.picks = picks
        pws.winner = winner
        print("Adding PlayerWeekStat({})".format(pws))
        pws.save()
    else:
        print("Adding PlayerWeekStat({})".format("{},{},{}".format(player.id, week.year.yearnum, week.weeknum)))

def perform_action():
    if arguments.update == 'update' and arguments.player is None and arguments.week is None and arguments.year is None:
        # This is a common update, where we are only interested in the most
        # recent completed week of the pool and whether or not it is present
        # in the PlayerWeekStats table.
        update_database()
    elif arguments.update == 'all':
        # This is a targeted refresh. The intention is to update as much as
        # possible within the bounds of what was specified as arguments.
        refresh_database()

def main(args=''):
    global arguments
    if not args:
        args = ['--help']
    if isinstance(args, six.string_types):
        args = args.split()

    parse_arguments(args)
    print("player={}, week={}, year={}, update={}".format(arguments.player, arguments.week, arguments.year, arguments.update))
    perform_action()

if __name__ == "__main__":
    main(args=sys.argv[1:])

