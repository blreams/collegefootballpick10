import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collegefootballpick10.settings')

import django
django.setup()

from django.core.exceptions import ObjectDoesNotExist

from pick10.models import Year, Player, PlayerYear, Conference, Team, Game, Pick, Week
from pick10.models import add_player, add_conference, add_team, add_game, add_week, add_pick
from pick10.models import get_user_by_username, get_team, get_game, get_week
from pick10.models import get_player_by_public_name, get_player_by_private_name
from pick10.models import update_game

from excel_history.excel.spreadsheet_test import player_username, get_player_years_dict, team_mascot_conference_division
from excel_history.excel.pool_spreadsheet import PoolSpreadsheet

beginyear = 1997
endyear = 2014
poolspreadsheets = {}

def get_poolspreadsheet(year):
    global poolspreadsheets
    if poolspreadsheets.get(year) is None:
        poolspreadsheets[year] = PoolSpreadsheet(year)
    return poolspreadsheets[year]

def populate_years(yearlist):
    for year in yearlist:
        try:
            y = Year.objects.get(yearnum=year)
            continue
        except ObjectDoesNotExist:
            pass
        except:
            raise

        y = Year()
        y.yearnum = year
        y.save()

def populate_players(yearlist, playercnt=0):
    global poolspreadsheets
    for year in yearlist:
        # First test to see if any playeryears exist for the year.
        playeryears = PlayerYear.objects.filter(year__yearnum=year)
        if len(playeryears) > 0:
            print "    Skipping populate_players(%d)"%(year,)
            continue

        yearobject = Year.objects.get(yearnum=year)
        poolspreadsheet = get_poolspreadsheets(year)
        public_names = poolspreadsheet.get_player_names()
        if playercnt > 0:
            public_name_set = set(public_names)
            public_names = [public_name_set.pop() for i in range(playercnt)]
        for public_name in public_names:
            try:
                player = Player.objects.get(public_name=public_name)
            except ObjectDoesNotExist:
                player = add_player(public_name=public_name, private_name=player_username[public_name])
            except:
                raise

            playeryear = PlayerYear()
            playeryear.player = player
            playeryear.year = yearobject
            playeryear.save()

def populate_conferences_teams(yearlist):
    for year in yearlist:
        poolspreadsheet = get_poolspreadsheet(year)
        teamnames = poolspreadsheet.get_team_names()
        for teamname in teamnames:
            mascot, conference, division = team_mascot_conference_division[teamname].split(':')
            confobj, created = Conference.objects.get_or_create(conf_name=conference, div_name=division)
            teamobj, created = Team.objects.get_or_create(team_name=teamname, mascot=mascot, conference=confobj)

def populate_games_for_year(yearnum):
    poolspreadsheet = get_poolspreadsheet(yearnum)
    for weeknum in poolspreadsheet.get_week_numbers():
        print "      Populating games for week %d..." % (weeknum,)
        games = poolspreadsheet.get_games(weeknum)
        week = add_week(yearnum, weeknum)
        for game in games:
            favored = 1 if poolspreadsheet.get_game_favored_team(weeknum, game) == 'team1' else 2
            spread = poolspreadsheet.get_game_spread(weeknum, game)
            add_game(week, get_team(games[game].team1), get_team(games[game].team2), game, favored=favored, spread=spread)
            team1_actual_points = poolspreadsheet.get_game_team1_score(weeknum, game)
            team2_actual_points = poolspreadsheet.get_game_team2_score(weeknum, game)
            update_game(yearnum, weeknum, game, team1_actual_points, team2_actual_points, 3)

def populate_games(yearlist):
    for yearnum in yearlist:
        if len(Game.objects.filter(week__year__yearnum=yearnum)) != 130:
            print "    Populating games for year %d..." % (yearnum,)
            populate_games_for_year(yearnum)
        else:
            print "    Games for year %d already populated, skipping..." % (yearnum,)

    for yearnum in yearlist:
        for weeknum in range(1, 14):
            if len(Game.objects.filter(week__year__yearnum=yearnum, week__weeknum=weeknum)) != 10:
                print "WARN: Year=%d, Week=%d, Did not find 10 games." % (yearnum, weeknum,)

def populate_picks_for_year_week(yearnum, weeknum, poolspreadsheet=None):
    try:
        numpicks = len(Pick.objects.filter(game__week__year__yearnum=yearnum, game__week__weeknum=weeknum))
        if numpicks > 10:
            print "        Picks for week %d already populated, skipping..." % (weeknum,)
            return
    except:
        pass

    if poolspreadsheet is None:
        poolspreadsheet = get_poolspreadsheet(yearnum)
    picks = poolspreadsheet.get_picks(weeknum)
    for pick in picks:
        game = get_game(yearnum, weeknum, pick.game_number)
        player = get_player_by_public_name(pick.player_name)
        winner = 1 if pick.winner == 'team1' else 2
        if pick.team1_score:
            add_pick(player=player, game=game, winner=winner, team1_predicted_points=pick.team1_score, team2_predicted_points=pick.team2_score)
        else:
            add_pick(player=player, game=game, winner=winner)

def populate_picks_for_year(yearnum):
    poolspreadsheet = get_poolspreadsheet(yearnum)
    for weeknum in poolspreadsheet.get_week_numbers():
        print "      Populating picks for week %d..." % (weeknum,)
        populate_picks_for_year_week(yearnum, weeknum, poolspreadsheet)

def populate_picks(yearlist):
    for yearnum in yearlist:
        try:
            numpicks = len(Pick.objects.filter(game__week__year__yearnum=yearnum))
            if numpicks > 10:
                print "    Picks for year %d already populated, skipping..." % (yearnum,)
                continue
        except:
            pass

        print "    Populating picks for year %s..." % (yearnum,)
        populate_picks_for_year(yearnum)

def delete_picks_for_year(yearnum):
    print "Deleting picks for year %d..." % (yearnum,)
    Pick.objects.filter(game__week__year__yearnum=yearnum).delete()

def delete_year_from_db(yearnum):
    picks = Pick.objects.filter(game__week__year__yearnum=yearnum)
    if len(picks) > 0:
        print "Deleting %d picks for year %d..." % (len(picks), yearnum,)
        picks.delete()
    games = Game.objects.filter(week__year__yearnum=yearnum)
    if len(games) > 0:
        print "Deleting %d games for year %d..." % (len(games), yearnum,)
        games.delete()
    weeks = Week.objects.filter(year__yearnum=yearnum)
    if len(weeks) > 0:
        print "Deleting %d weeks for year %d..." % (len(weeks), yearnum,)
        weeks.delete()


def populate_year(yearnum):
    yearobj, created = Year.objects.get_or_create(yearnum=yearnum)
    return yearobj

def convert_to_private_name(ssplayername):
    username = player_username[ssplayername]
    lastname, firstname = username.split('_')
    firstname = firstname.capitalize()
    lastname = lastname.capitalize()
    return ' '.join([firstname, lastname])

def convert_to_public_name(ssplayername):
    username = player_username[ssplayername]
    lastname, firstname = username.split('_')
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

def populate_player_count(yearnum, playersperyear):
    yearobj = Year.objects.get(yearnum=yearnum)
    poolspreadsheet = get_poolspreadsheet(yearnum)
    ss_names = poolspreadsheet.get_player_names()
    if playersperyear > 0:
        ss_name_set = set(ss_names)
        ss_names = [ss_name_set.pop() for i in range(playersperyear)]
    for ss_name in ss_names:
        populate_player_year(yearnum, ss_name)

def populate_week(yearnum, weeknum):
    yearobj = Year.objects.get(yearnum)
    weekobj, created = Week.objects.get_or_create(year=yearobj, weeknum=weeknum)
    if created:
        # Need to figure out the winner and make sure that player, playeryear is populated
        poolspreadsheet = get_poolspreadsheet(yearnum)
        winner_ss_name = poolspreadsheet.get_week_winner(weeknum)
        populate_player_year(yearnum, winner_ss_name)

def populate_games_for_week_year(yearnum, weeknum):
    poolspreadsheet = get_poolspreadsheet(yearnum)
    games_dict = poolspreadsheet.get_games(weeknum)

def newmain(years=None, playersperyear=0, weeks=None):
    # Figure out years
    if years is None:
        years = range(beginyear, endyear + 1)
    elif isinstance(years, (int, long)):
        years = [years]

    for yearnum in years:
        poolspreadsheet = get_poolspreadsheet(yearnum)
        populate_year(yearnum)
        populate_player_count(yearnum, playersperyear)

        if weeks is None:
            weeks = poolspreadsheet.get_week_numbers()
        elif isinstance(weeks, (int, long)):
            weeks = [weeks]

        for weeknum in weeks:
            populate_week(yearnum, weeknum)
            populate_games_for_year_week(yearnum, weeknum)

def main(years=None, games=False, picks=False, playercnt=0):
    if years is None:
        years = range(1997, 2015)
    elif isinstance(years, basestring):
        years = [int(years)]
    elif isinstance(years, (int, long)):
        years = [years]
    if picks:
        games = True
    print "Starting pick10 model population..."
    print "  Populating Year(s)..."
    populate_years(years)
    print "  Populating Players..."
    populate_players(years, playercnt)
    print "  Populating Conferences and Teams..."
    populate_conferences_teams()
    if games:
        print "  Populating Games..."
        populate_games(years)
    if picks:
        print "  Populating Picks..."
        populate_picks(years)

# Execution starts here
if __name__ == '__main__':
    main()

