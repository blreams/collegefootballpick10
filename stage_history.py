from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

import os
from collections import Counter
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collegefootballpick10.settings')
#from datetime import datetime, date, time
from django.utils import timezone

import django
django.setup()

from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache

from pick10.models import Year, Player, PlayerYear, Conference, Team, Game, Pick, Week
from pick10.models import get_yearlist, get_weeklist, get_player_by_private_name
from pick10.overall_results_view import OverallResultsView
from pick10.week_results_view import WeekResultsView
from pick10.tiebreak_view import TiebreakView

from excel_history.excel.spreadsheet_test import player_username, get_player_years_dict, team_mascot_conference_division
from excel_history.excel.pool_spreadsheet import PoolSpreadsheet

beginyear = 1997
endyear = 2015
poolspreadsheets = {}

def get_poolspreadsheet(year):
    global poolspreadsheets
    if poolspreadsheets.get(year) is None:
        poolspreadsheets[year] = PoolSpreadsheet(year)
    return poolspreadsheets[year]

def get_player_duplicates():
    private_players = [player.private_name for player in Player.objects.all()]
    c = Counter(private_players)
    for private_player in c:
        if c[private_player] > 1:
            for index in range(c[private_player]):
                player = get_player_by_private_name(private_player, index)
                print(str(player))

def get_playernames_with_years(yearnums=0, debug=False):
    playerdict = {}
    if isinstance(yearnums, list):
        yearnumlist = yearnums
    if yearnums == 0:
        yearnumlist = get_yearlist()

    for yearnum in yearnumlist:
        if debug: print("Parsing %d spreadsheet..." % yearnum)
        ss = get_poolspreadsheet(yearnum)
        for playername in ss.get_player_names():
            if playerdict.get(playername) is None:
                playerdict[playername] = [str(yearnum)]
            else:
                playerdict[playername].append(str(yearnum))

    outlines = []
    for playername in sorted(playerdict):
        years_string = ','.join(playerdict[playername])
        outline = "%s: %s" % (playername, years_string)
        if debug: print(outline)
        outlines.append(outline)

    return '\n'.join(outlines)

def picks_change_players(from_ssname, to_ssname, debug=False):
    fromplayer = Player.objects.get(ss_name=from_ssname)
    toplayer = Player.objects.get(ss_name=to_ssname)
    print("From Player = %s" % str(fromplayer))
    print("To   Player = %s" % str(toplayer))
    picks = Pick.objects.filter(player=fromplayer)
    topicks = Pick.objects.filter(player=toplayer)
    print("-----------------BEFORE--------------------")
    print("Found %d Picks for From Player %s" % (len(picks), str(fromplayer)))
    print("Found %d Picks for To   Player %s" % (len(topicks), str(toplayer)))
    playeryears = PlayerYear.objects.filter(player=fromplayer)
    toplayeryears = PlayerYear.objects.filter(player=toplayer)
    print("Found %d PlayerYears for From Player %s" % (len(playeryears), str(fromplayer)))
    print("Found %d PlayerYears for To   Player %s" % (len(toplayeryears), str(toplayer)))
    print("-------------------------------------------")
    for pick in picks:
        pick.player = toplayer
        if not debug: pick.save()
    for playeryear in playeryears:
        playeryear.player = toplayer
        if not debug: playeryear.save()
    picks = Pick.objects.filter(player=fromplayer)
    topicks = Pick.objects.filter(player=toplayer)
    print("-----------------AFTER---------------------")
    print("Found %d Picks for From Player %s" % (len(picks), str(fromplayer)))
    print("Found %d Picks for To   Player %s" % (len(topicks), str(toplayer)))
    playeryears = PlayerYear.objects.filter(player=fromplayer)
    toplayeryears = PlayerYear.objects.filter(player=toplayer)
    print("Found %d PlayerYears for From Player %s" % (len(playeryears), str(fromplayer)))
    print("Found %d PlayerYears for To   Player %s" % (len(toplayeryears), str(toplayer)))
    print("-------------------------------------------")

def flush_cache(yearnums=0, weeknum=0, skipweek=False, skiptiebreak=False, skipoverall=False, debug=False):
    """Delete memcache contents based on arguments.
    """
    yearnumlist = [yearnums]
    if isinstance(yearnums, list):
        yearnumlist = yearnums
    if yearnums == 0:
        yearnumlist = get_yearlist()

    weeknumdict = {}
    for yearnum in yearnumlist:
        if weeknum == 0:
            weeknumdict[yearnum] = get_weeklist(yearnum)
        else:
            weeknumdict[yearnum] = [weeknum]

    for yearnum in weeknumdict:
        for weeknum in weeknumdict[yearnum]:
            if not skipweek:
                print("Flushing memcache week results      year %d, week %d." % (yearnum, weeknum))
                for keytype in ('private', 'public'):
                    body_key = 'week_%s_%d_%d' % (keytype, yearnum, weeknum)
                    if cache.get(body_key) is not None:
                        print("  Flushing entry %s." % (body_key,))
                        if not debug: cache.delete(body_key)
            if not skiptiebreak:
                print("Flushing memcache tiebreaks         year %d, week %d." % (yearnum, weeknum))
                for keytype in ('private', 'public'):
                    body_key = 'tiebreak_%s_%d_%d' % (keytype, yearnum, weeknum)
                    if cache.get(body_key) is not None:
                        print("  Flushing entry %s." % (body_key,))
                        if not debug: cache.delete(body_key)
        if not skipoverall:
            print("Flushing memcache overall results   year %d." % (yearnum))
            for keytype in ('private', 'public'):
                body_key = 'overall_%s_%d' % (keytype, yearnum)
                if cache.get(body_key) is not None:
                    print("  Flushing entry %s." % (body_key,))
                    if not debug: cache.delete(body_key)

def update_cache(yearnums=0, weeknum=0, skipweek=False, skiptiebreak=False, skipoverall=False, debug=False):
    yearnumlist = [yearnums]
    if isinstance(yearnums, list):
        yearnumlist = yearnums
    if yearnums == 0:
        yearnumlist = get_yearlist()

    weeknumdict = {}
    for yearnum in yearnumlist:
        if weeknum == 0:
            weeknumdict[yearnum] = get_weeklist(yearnum)
        else:
            weeknumdict[yearnum] = [weeknum]

    for yearnum in weeknumdict:
        for weeknum in weeknumdict[yearnum]:
            if not skipweek:
                print("Updating memcache week results      year %d, week %d." % (yearnum, weeknum))
                if not debug: update_memcache_week_results(yearnum, weeknum)
            if not skiptiebreak:
                print("Updating memcache tiebreaks         year %d, week %d." % (yearnum, weeknum))
                if not debug: update_memcache_tiebreak(yearnum, weeknum)
        if not skipoverall:
            print("Updating memcache overall results   year %d." % (yearnum))
            if not debug: update_memcache_overall_results(yearnum)

def delete_year_from_db(yearnum):
    picks = Pick.objects.filter(game__week__year__yearnum=yearnum)
    if len(picks) > 0:
        print("Deleting %d picks for year %d..." % (len(picks), yearnum,))
        picks.delete()
    games = Game.objects.filter(week__year__yearnum=yearnum)
    if len(games) > 0:
        print("Deleting %d games for year %d..." % (len(games), yearnum,))
        games.delete()
    weeks = Week.objects.filter(year__yearnum=yearnum)
    if len(weeks) > 0:
        print("Deleting %d weeks for year %d..." % (len(weeks), yearnum,))
        weeks.delete()
    playeryears = PlayerYear.objects.filter(year__yearnum=yearnum)
    if len(playeryears) > 0:
        print("Deleting %d playeryears for year %d..." % (len(playeryears), yearnum,))
        playeryears.delete()
    players = []
    for player in Player.objects.all():
        playeryears = PlayerYear.objects.filter(player=player)
        if len(playeryears) == 0:
            players.append(player)
    if len(players) > 0:
        print("Deleting %d players for year %d..." % (len(players), yearnum,))
        for player in players:
            player.delete()
    years = Year.objects.filter(yearnum=yearnum)
    if len(years) > 0:
        print("Deleting year %d..." % (yearnum,))
        years.delete()

def delete_year_week_from_db(yearnum, weeknum):
    picks = Pick.objects.filter(game__week__year__yearnum=yearnum, game__week__weeknum=weeknum)
    if len(picks) > 0:
        print("Deleting %d picks for year %d week %d..." % (len(picks), yearnum, weeknum))
        picks.delete()
    games = Game.objects.filter(week__year__yearnum=yearnum, week__weeknum=weeknum)
    if len(games) > 0:
        print("Deleting %d games for year %d week %d..." % (len(games), yearnum, weeknum))
        games.delete()
    weeks = Week.objects.filter(year__yearnum=yearnum, weeknum=weeknum)
    if len(weeks) > 0:
        print("Deleting %d weeks for year %d week %d..." % (len(weeks), yearnum, weeknum))
        weeks.delete()

def populate_year(yearnum, verbose=False):
    yearobj, created = Year.objects.get_or_create(yearnum=yearnum)
    return yearobj

def convert_to_private_name(ssplayername):
    username = player_username.get(ssplayername)
    if username != None:
        lastname, firstname = username.split('_')
    else:
        tokens = ssplayername.split(',')
        lastname = tokens[0]
        firstname = tokens[1].split()[0]
    firstname = firstname.capitalize()
    lastname = lastname.capitalize()
    return ' '.join([firstname, lastname])


def convert_to_public_name(ssplayername):
    username = player_username.get(ssplayername)
    if username != None:
        lastname, firstname = username.split('_')
    else:
        tokens = ssplayername.split(',')
        lastname = tokens[0]
        firstname = tokens[1].split()[0]
    firstname = firstname.capitalize()
    lastname = lastname.capitalize()
    public_name = firstname
    existing_players = Player.objects.filter(public_name=public_name)
    while len(existing_players) > 0:
        letter = lastname[0]
        lastname = lastname[1:]
        public_name += letter
        existing_players = Player.objects.filter(public_name=public_name)
    return public_name

def populate_player_year(yearnum, ssplayername):
    yearobj = Year.objects.get(yearnum=yearnum)
    playerobj, created = Player.objects.get_or_create(ss_name=ssplayername)
    if created:
        playerobj.private_name = convert_to_private_name(ssplayername)
        playerobj.public_name = convert_to_public_name(ssplayername)
        playerobj.save()
    playeryearobj, created = PlayerYear.objects.get_or_create(player=playerobj, year=yearobj)

def populate_player_count(yearnum, verbose=False):
    yearobj = Year.objects.get(yearnum=yearnum)
    poolspreadsheet = get_poolspreadsheet(yearnum)
    ss_names = poolspreadsheet.get_player_names()
    for ss_name in ss_names:
        if verbose: print("populate_player_year(%d, %s)" % (yearnum, ss_name,))
        populate_player_year(yearnum, ss_name)

def populate_week(yearnum, weeknum, verbose=False):
    yearobj = Year.objects.get(yearnum=yearnum)
    weekobj, created = Week.objects.get_or_create(year=yearobj, weeknum=weeknum)
    if created:
        poolspreadsheet = get_poolspreadsheet(yearnum)
        winner_ss_name = poolspreadsheet.get_week_winner(weeknum)
        if winner_ss_name == None or poolspreadsheet.has_multiple_winners(weeknum):
            weekobj.winner = None
        else:
            populate_player_year(yearnum, winner_ss_name)
            playerobj = Player.objects.get(ss_name=winner_ss_name)
            weekobj.winner = playerobj
        if verbose: print("Week(%d, %d).save()" % (yearnum, weeknum,))
        weekobj.save()

def populate_all_teams():
    for teamname in team_mascot_conference_division:
        populate_team(teamname)

def populate_team(teamname):
    mascot, conference, division = team_mascot_conference_division[teamname].split(':')
    confobj, create = Conference.objects.get_or_create(conf_name=conference, div_name=division)
    teamobj, create = Team.objects.get_or_create(team_name=teamname, mascot=mascot, conference=confobj)
    return teamobj

def populate_games_for_year_week(yearnum, weeknum, verbose=False):
    yearobj = Year.objects.get(yearnum=yearnum)
    weekobj = Week.objects.get(year=yearobj, weeknum=weeknum)
    poolspreadsheet = get_poolspreadsheet(yearnum)
    games_dict = poolspreadsheet.get_games(weeknum)
    if len(games_dict) == 10:
        weekobj.pick_deadline = timezone.now()
        weekobj.lock_picks = False
        weekobj.save()
    num_final = 0
    for gamenum in games_dict:
        team1obj = populate_team(games_dict[gamenum].team1)
        team2obj = populate_team(games_dict[gamenum].team2)
        team1actualpoints = poolspreadsheet.get_game_team1_score(weeknum, gamenum)
        team2actualpoints = poolspreadsheet.get_game_team2_score(weeknum, gamenum)
        favored = 1 if poolspreadsheet.get_game_favored_team(weeknum, gamenum) == 'team1' else 2
        spread = poolspreadsheet.get_game_spread(weeknum, gamenum)

        score_entered = team1actualpoints != None and team2actualpoints != None
        if score_entered:
            winner = 1
            if (favored == 1 and (team1actualpoints - team2actualpoints) < spread) or (favored == 2 and (team2actualpoints - team1actualpoints) > spread):
                winner = 2
            game_state = 3  # FINAL
            num_final += 1
        else:
            team1actualpoints = -1
            team2actualpoints = -1
            winner = 0
            game_state = 1 # NOT_STARTED
        if verbose: print("Game(%d, %d, %d).save()" % (yearnum, weeknum, gamenum,))
        gameobj = Game.objects.get_or_create(week=weekobj, gamenum=gamenum, team1=team1obj, team2=team2obj, team1_actual_points=team1actualpoints, team2_actual_points=team2actualpoints, favored=favored, spread=spread, winner=winner,game_state=game_state)
    if num_final == 10:
        weekobj.lock_scores = True
        weekobj.save()

def populate_picks_for_year_week(yearnum, weeknum, verbose=False):
    yearobj = Year.objects.get(yearnum=yearnum)
    weekobj = Week.objects.get(year=yearobj, weeknum=weeknum)
    poolspreadsheet = get_poolspreadsheet(yearnum)
    picks = poolspreadsheet.get_picks(weeknum)
    playeryearobjs = PlayerYear.objects.filter(year=yearobj)
    ss_names_player_dict = {py.player.ss_name: py.player for py in playeryearobjs}
    for pick in picks:
        if pick.player_name not in ss_names_player_dict:
            continue
        playerobj = ss_names_player_dict[pick.player_name]
        gameobj = Game.objects.get(week=weekobj, gamenum=pick.game_number)

        if poolspreadsheet.did_player_default(pick.player_name,weeknum):
            winner = 0
        else:
            winner = 1 if pick.winner == 'team1' else 2

        pickobj, created = Pick.objects.get_or_create(player=playerobj, game=gameobj)
        if created:
            pickobj.winner = winner
            if pick.team1_score is not None:
                pickobj.team1_predicted_points = pick.team1_score
                pickobj.team2_predicted_points = pick.team2_score
            if verbose: print("Pick(%s, %d, %d, %d).save()" % (pick.player_name, yearnum, weeknum, pick.game_number,))
            pickobj.save()

def update_memcache_week_results(yearnum,weeknum):
    WeekResultsView().get(None,yearnum,weeknum,use_private_names=False)
    WeekResultsView().get(None,yearnum,weeknum,use_private_names=True)

def update_memcache_tiebreak(yearnum,weeknum):
    TiebreakView().get(None,yearnum,weeknum,use_private_names=False)
    TiebreakView().get(None,yearnum,weeknum,use_private_names=True)

def update_memcache_overall_results(yearnum):
    OverallResultsView().get(None,yearnum,use_private_names=False)
    OverallResultsView().get(None,yearnum,use_private_names=True)

def main(years=None, weeks=None, verbose=False, load_memcache=True):
    if years is None:
        years = range(beginyear, endyear + 1)
    elif isinstance(years, six.integer_types):
        years = [years]

    print("populate_all_teams()")
    populate_all_teams()

    for yearnum in years:
        poolspreadsheet = get_poolspreadsheet(yearnum)
        print("populate_year(%d)" % (yearnum,))
        populate_year(yearnum, verbose)
        print("populate_player_count(%d)" % (yearnum,))
        populate_player_count(yearnum, verbose)

        if weeks is None:
            weeks = poolspreadsheet.get_week_numbers()
        elif isinstance(weeks, six.integer_types):
            weeks = [weeks]
        print("Found %d weeks in spreadsheet..." % (len(weeks),))

        for weeknum in weeks:
            print("populate_week(%d, %d)" % (yearnum, weeknum,))
            populate_week(yearnum, weeknum, verbose)
            print("populate_games_for_year_week(%d, %d)" % (yearnum, weeknum,))
            populate_games_for_year_week(yearnum, weeknum, verbose)
            print("populate_picks_for_year_week(%d, %d)" % (yearnum, weeknum,))
            populate_picks_for_year_week(yearnum, weeknum, verbose)

            if load_memcache:
                print("update_memcache_week_results(%d, %d)" % (yearnum, weeknum,))
                update_memcache_week_results(yearnum, weeknum)
                print("update_memcache_tiebreak(%d, %d)" % (yearnum, weeknum,))
                update_memcache_tiebreak(yearnum, weeknum)

        if load_memcache:
            print("update_memcache_overall_results(%d)" % (yearnum))
            update_memcache_overall_results(yearnum)


# Execution starts here
if __name__ == '__main__':
    main()

