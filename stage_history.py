import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collegefootballpick10.settings')

import django
django.setup()

from pick10.models import Team
from pick10.models import add_user, add_conference, add_team, add_game, add_week, add_pick
from pick10.models import get_user_by_username, get_team, get_game, get_week

from excel_history.excel.spreadsheet_test import get_player_years_dict

def populate_users():
    # Create a player translation dict
    player_username = {}
    player_username['Aaron, Chip'] = 'aaron_chip'
    player_username['Acevedo, Alfonso'] = 'acevedo_alfonso'
    player_username['Adams, Daniel O'] = 'adams_daniel'
    player_username['Allen, Landon Remote'] = 'allen_landon'
    player_username['Barker, Christopher A'] = 'barker_christopher'
    player_username['Barnes, Ike K'] = 'barnes_ike'
    player_username['Batchler, Wayne'] = 'batchler_wayne'
    player_username['Beasley, Tate'] = 'beasley_tate'
    player_username['Beckwith, Greg'] = 'beckwith_greg'
    player_username['Berger, Matthew A'] = 'berger_matthew'
    player_username['Bisbee, Curt'] = 'bisbee_curt'
    player_username['Blackmon, Vaughn'] = 'blackmon_vaughn'
    player_username['Bowers, Martin L'] = 'bowers_martin'
    player_username['Boyce, Jonathan E'] = 'boyce_jonathan'
    player_username['Boykin, Jerome W'] = 'boykin_jerome'
    player_username['Brokaw, Brantley A'] = 'brokaw_brantley'
    player_username['Brunt, DavidRemote'] = 'brunt_david'
    player_username['Carter, Chris'] = 'carter_chris'
    player_username['Chan, Simon'] = 'chan_simon'
    player_username['Christiansen, Amos H'] = 'christiansen_amos'
    player_username['Clark, William J'] = 'clark_william'
    player_username['Cochcroft, Art'] = 'cochcroft_art'
    player_username['Cogan, TimothyX J'] = 'cogan_timothy'
    player_username['Cook, Andrew S'] = 'cook_andrew'
    player_username['Corley, Ernie'] = 'corley_ernie'
    player_username['Crenshaw, Ed'] = 'crenshaw_ed'
    player_username['Desetto, Daniel'] = 'desetto_daniel'
    player_username['Desing, Scott M'] = 'desing_scott'
    player_username['Deuell, Russell A'] = 'deuell_russell'
    player_username['Duzan, Steve'] = 'duzan_steve'
    player_username['Edwards, Christopher S'] = 'edwards_christoper'
    player_username['Emptage, Nick'] = 'emptage_nick'
    player_username['Estrada, Carlos A'] = 'estradia_carlos'
    player_username['Eusebio, Ariel B'] = 'eusebio_ariel'
    player_username['Farren, Kevin M'] = 'farren_kevin'
    player_username['Farren, Leslie Remote'] = 'farren_leslie'
    player_username['Ferguson, Scott Remote'] = 'ferguson_scott'
    player_username['Fonville, Chris'] = 'fonville_chris'
    player_username['Fonville, Stephanie Remote'] = 'fonville_stephanie'
    player_username['Freedman, Scott Remote'] = 'freedman_scott'
    player_username['Gibson, Johnny J'] = 'gibson_johnny'
    player_username['Gilmer, Justin T'] = 'gilmer_justin'
    player_username['Gindlesperger, Jeffrey C'] = 'gindlesperger_jeffrey'
    player_username['Gore, Brandon'] = 'gore_brandon'
    player_username['Gregory, Adam J'] = 'gregory_adam'
    player_username['Gupta, Ashish O'] = 'gupta_ashish'
    player_username['Havens, Ryan C'] = 'havens_ryan'
    player_username['Hawk, Robert W'] = 'hawk_robert'
    player_username['Hendrick, Matt R'] = 'hendrick_matt'
    player_username['Holden, Brent'] = 'holden_brent'
    player_username['Holley, Jeremy Remote'] = 'holley_jeremy'
    player_username['Howell, David P'] = 'howell_david'
    player_username['Hucks, Jason'] = 'hucks_jason'
    player_username['Inabinet, Greg'] = 'inabinet_greg'
    player_username['James, Larry C'] = 'james_larry'
    player_username['Johnson, Robert J'] = 'johnson_robert'
    player_username['Kandela, Marwan'] = 'kandela_marwan'
    player_username['Kieselhorst, Larry'] = 'kieselhorst_larry'
    player_username['Knopf, Greg D'] = 'knopf_greg'
    player_username['Knotts, Brian'] = 'knotts_brian'
    player_username['Krooswyk, Steven K'] = 'krooswyk_steven'
    player_username['Locklear, Dave Remote'] = 'locklear_dave'
    player_username['Lovelace, Van'] = 'lovelace_van'
    player_username['Luck, Justin'] = 'luck_justin'
    player_username['Marsh, Alexander Remote'] = 'marsh_alexander'
    player_username['Martin, Douglas C'] = 'martin_douglas'
    player_username['McGee, Steve'] = 'mcgee_steve'
    player_username['McMahon, Pat'] = 'mcmahon_pat'
    player_username['McTeer, Libby'] = 'mcteer_libby'
    player_username['Mccall, Sean'] = 'mccall_sean'
    player_username['Mccoy, William M'] = 'mccoy_william'
    player_username['Mellitz, Elisha B'] = 'mellitz_elisha'
    player_username['Miller, James'] = 'miller_james'
    player_username['Miller, Robert J'] = 'miller_robert'
    player_username['Moore, Kevin B'] = 'moore_kevin'
    player_username['Moxley, Dave'] = 'moxley_dave'
    player_username['Murphy, William A'] = 'murphy_william'
    player_username['Nagorniak, Kristen M'] = 'nagorniak_kristen'
    player_username['Nance, Rob'] = 'nance_rob'
    player_username['Neeley, Amber Remote'] = 'neeley_amber'
    player_username['Neeley, Michael'] = 'neeley_michael'
    player_username['Neill, Charles H'] = 'neill_charles'
    player_username['Nguyen, Thai'] = 'nguyen_thai'
    player_username['Nye, Mike'] = 'nye_mike'
    player_username['Parcenka, ThomasX'] = 'parcenka_thomas'
    player_username['Parris, Brian W'] = 'parris_brian'
    player_username['Patterson, Kevin R'] = 'patterson_kevin'
    player_username['Peng, Aaron'] = 'peng_aaron'
    player_username['Penrose, Tim Remote'] = 'penrose_tim'
    player_username['Powell, LaMar'] = 'powell_lamar'
    player_username['Puga, Moises'] = 'puga_moises'
    player_username['Pytel, Steven G'] = 'pytel_steven'
    player_username['Reams, Byron L'] = 'reams_byron'
    player_username['Redalen, Andy'] = 'redalen_andy'
    player_username['Redys, Brittany'] = 'redys_brittany'
    player_username['Redys, David Remote'] = 'redys_david'
    player_username['Reiland, Doug'] = 'reiland_doug'
    player_username['Reiland, Will Remote'] = 'reiland_will'
    player_username['Robbins, Dale'] = 'robbins_dale'
    player_username['Robbins, Thomas D'] = 'robbins_thomas'
    player_username['Ruffin, Chris'] = 'ruffin_chris'
    player_username['Sams, David'] = 'sams_david'
    player_username['Sapp, Carl G'] = 'sapp_carl'
    player_username['Schelling, Todd'] = 'schelling_todd'
    player_username['Scrivener, Bo'] = 'scrivener_bo'
    player_username['Shuey, Jeffrey M'] = 'shuey_jeffrey'
    player_username['Smoak, Wilson'] = 'smoak_wilson'
    player_username['Staub, Kevin'] = 'staub_kevin'
    player_username['Steel, Van Remote'] = 'steel_van'
    player_username['Steele, David L'] = 'steele_david'
    player_username['Stonecypher, David'] = 'stonecypher_david'
    player_username['Straw, Adam D'] = 'straw_adam'
    player_username['Strom, Brooker'] = 'strom_brooker'
    player_username['Taylor, Adam'] = 'taylor_adam'
    player_username['Teasdell, Brian K'] = 'teasdell_brian'
    player_username['Tunnell, Justin S'] = 'tunnell_justin'
    player_username['Tyson, Ben'] = 'tyson_ben'
    player_username['Vang, Tong'] = 'vang_tong'
    player_username['Vo, Henry'] = 'vo_henry'
    player_username['Warren, Todd Remote'] = 'warren_todd'
    player_username['Wells, Jennifer'] = 'wells_jennifer'
    player_username['Wells, Seth Remote'] = 'wells_seth'
    player_username['White, Jarred'] = 'white_jarred'
    player_username['Wiant, Timothy J'] = 'wiant_timothy'
    player_username['Willingham, JosephX'] = 'willingham_joseph'
    player_username['Winburn, Steve A'] = 'winburn_steve'
    player_username['Young, Derick'] = 'young_derick'
    player_username['Young, Kenneth'] = 'young_kenneth'

    for ss_name, username in player_username.iteritems():
        last, first = username.split('_')
        email = '%s_%s@example.com' % (first, last,)
        add_user(username, email, first.capitalize(), last.capitalize())

def populate_conferences_teams():
    # American Athletic
    conf = add_conference('American Athletic')
    add_team('Cincinnati', 'Bearcats', conf)
    add_team('Connecticut', 'Huskies', conf)
    add_team('East Carolina', 'Pirates', conf)
    add_team('Houston', 'Cougars', conf)
    add_team('Memphis', 'Tigers', conf)
    add_team('South Florida', 'Bulls', conf)
    add_team('Southern Methodist', 'Mustangs', conf)
    add_team('Temple', 'Owls', conf)
    add_team('Tulane', 'Green Wave', conf)
    add_team('Tulsa', 'Golden Hurricane', conf)
    add_team('UCF', 'Knights', conf)

    # Atlantic Coast - Atlantic
    conf = add_conference('Atlantic Coast', 'Atlantic')
    add_team('Boston College', 'Eagles', conf)
    add_team('Clemson', 'Tigers', conf)
    add_team('Florida State', 'Seminoles', conf)
    add_team('Louisville', 'Cardinals', conf)
    add_team('NC State', 'Wolfpack', conf)
    add_team('Syracuse', 'Orange', conf)
    add_team('Wake Forest', 'Demon Deacons', conf)
    # Atlantic Coast - Coastal
    conf = add_conference('Atlantic Coast', 'Coastal')
    add_team('Duke', 'Blue Devils', conf)
    add_team('Georgia Tech', 'Yellow Jackets', conf)
    add_team('Miami (Fla.)', 'Hurricanes', conf)
    add_team('North Carolina', 'Tarheels', conf)
    add_team('Pittsburgh', 'Panthers', conf)
    add_team('Virginia', 'Cavaliers', conf)
    add_team('Virginia Tech', 'Hokies', conf)

    # Big Ten - East
    conf = add_conference('Big Ten', 'East')
    add_team('Indiana', 'Hoosiers', conf)
    add_team('Maryland', 'Terrapins', conf)
    add_team('Michigan', 'Wolverines', conf)
    add_team('Michigan State', 'Spartans', conf)
    add_team('Ohio State', 'Buckeyes', conf)
    add_team('Penn State', 'Nittany Lions', conf)
    add_team('Rutgers', 'Scarlet Knights', conf)
    # Big Ten - West
    conf = add_conference('Big Ten', 'West')
    add_team('Illinois', 'Illini', conf)
    add_team('Iowa', 'Hawkeyes', conf)
    add_team('Minnesota', 'Golden Gophers', conf)
    add_team('Nebraska', 'Cornhuskers', conf)
    add_team('Northwestern', 'Wildcats', conf)
    add_team('Purdue', 'Boilermakers', conf)
    add_team('Wisconsin', 'Badgers', conf)

    # Big 12
    conf = add_conference('Big 12')
    add_team('Baylor', 'Bears', conf)
    add_team('Iowa State', 'Cyclones', conf)
    add_team('Kansas', 'Jayhawks', conf)
    add_team('Kansas State', 'Wildcats', conf)
    add_team('Oklahoma', 'Sooners', conf)
    add_team('Oklahoma State', 'Cowboys', conf)
    add_team('TCU', 'Horned Frogs', conf)
    add_team('Texas', 'Longhorns', conf)
    add_team('Texas Tech', 'Red Raiders', conf)
    add_team('West Virginia', 'Mountaineers', conf)

    # Conference USA - East
    conf = add_conference('Conference USA', 'East')
    add_team('Florida Atlantic', 'Owls', conf)
    add_team('Florida International', 'Golden Panthers', conf)
    add_team('Marshall', 'Thundering Herd', conf)
    add_team('Middle Tennessee', 'Blue Raiders', conf)
    add_team('Old Dominion', 'Monarchs', conf)
    add_team('UAB', 'Blazers', conf)
    add_team('Western Kentucky', 'Hilltoppers', conf)
    # Conference USA - West
    conf = add_conference('Conference USA', 'West')
    add_team('Louisiana Tech', 'Bulldogs', conf)
    add_team('North Texas', 'Mean Green', conf)
    add_team('Rice', 'Owls', conf)
    add_team('Southern Mississippi', 'Golden Eagles', conf)
    add_team('Texas-El Paso', 'Miners', conf)
    add_team('Texas-San Antonio', 'Road Runners', conf)

    # Independents
    conf = add_conference('Independents')
    add_team('Army', 'Black Knights', conf)
    add_team('Brigham Young', 'Cougars', conf)
    add_team('Navy', 'Midshipmen', conf)
    add_team('Notre Dame', 'Fighting Irish', conf)

    # Mid American - East
    conf = add_conference('Mid American', 'East')
    add_team('Akron', 'Zips', conf)
    add_team('Bowling Green', 'Falcons', conf)
    add_team('Buffalo', 'Bulls', conf)
    add_team('Kent State', 'Golden Flashes', conf)
    add_team('Massachusetts', 'Minutemen', conf)
    add_team('Miami (Ohio)', 'Redhawks', conf)
    add_team('Ohio', 'Bobcats', conf)
    # Mid American - West
    conf = add_conference('Mid American', 'West')
    add_team('Ball State', 'Cardinals', conf)
    add_team('Central Michigan', 'Chippewas', conf)
    add_team('Eastern Michigan', 'Eagles', conf)
    add_team('Northern Illinois', 'Huskies', conf)
    add_team('Toledo', 'Rockets', conf)
    add_team('Western Michigan', 'Broncos', conf)

    # Mountain West - Mountain
    conf = add_conference('Mountain West', 'Mountain')
    add_team('Air Force', 'Falcons', conf)
    add_team('Boise State', 'Broncos', conf)
    add_team('Colorado State', 'Rams', conf)
    add_team('New Mexico', 'Lobos', conf)
    add_team('Utah State', 'Aggies', conf)
    add_team('Wyoming', 'Cowboys', conf)
    # Mountain West - West
    conf = add_conference('Mountain West', 'West')
    add_team('Fresno State', 'Bulldogs', conf)
    add_team('Hawaii', 'Rainbox Warriors', conf)
    add_team('Nevada', 'Wolf Pack', conf)
    add_team('San Diego State', 'Aztecs', conf)
    add_team('San Jose State', 'Spartans', conf)
    add_team('UNLV', 'Rebels', conf)

    # Pacific 12 - North
    conf = add_conference('Pacific 12', 'North')
    add_team('California', 'Golden Bears', conf)
    add_team('Oregon', 'Ducks', conf)
    add_team('Oregon State', 'Beavers', conf)
    add_team('Stanford', 'Cardinal', conf)
    add_team('Washington', 'Huskies', conf)
    add_team('Washington State', 'Cougars', conf)
    # Pacific 12 - South
    conf = add_conference('Pacific 12', 'South')
    add_team('Arizona', 'Wildcats', conf)
    add_team('Arizona State', 'Sun Devils', conf)
    add_team('Colorado', 'Buffaloes', conf)
    add_team('Southern California', 'Trojans', conf)
    add_team('UCLA', 'Bruins', conf)
    add_team('Utah', 'Utes', conf)

    # Southeastern - East
    conf = add_conference('Southeastern', 'East')
    add_team('Florida', 'Gators', conf)
    add_team('Georgia', 'Bulldogs', conf)
    add_team('Kentucky', 'Wildcats', conf)
    add_team('Missouri', 'Tigers', conf)
    add_team('South Carolina', 'Gamecocks', conf)
    add_team('Tennessee', 'Volunteers', conf)
    add_team('Vanderbilt', 'Commodores', conf)
    # Southeastern - West
    conf = add_conference('Southeastern', 'West')
    add_team('Alabama', 'Crimson Tide', conf)
    add_team('Arkansas', 'Razorbacks', conf)
    add_team('Auburn', 'Tigers', conf)
    add_team('LSU', 'Tigers', conf)
    add_team('Mississippi State', 'Bulldogs', conf)
    add_team('Ole Miss', 'Rebels', conf)
    add_team('Texas A&M', 'Aggies', conf)

    # Sun Belt
    conf = add_conference('Sun Belt')
    add_team('Appalachian State', 'Mountaineers', conf)
    add_team('Arkansas State', 'Red Wolves', conf)
    add_team('Georgia Southern', 'Eagle', conf)
    add_team('Georgia State', 'Panthers', conf)
    add_team('Idaho', 'Vandals', conf)
    add_team('Louisiana-Monroe', 'Warhawks', conf)
    add_team('New Mexico State', 'Aggies', conf)
    add_team('South Alabama', 'Jaguars', conf)
    add_team('Texas State', 'Bobcats', conf)
    add_team('Troy', 'Trojans', conf)
    add_team('UL Lafayette', 'Ragin Cajuns', conf)

def populate_games():
    year = 2014
    week = 1
    add_game(get_team('South Carolina'), get_team('Texas A&M'), year, week, 1)
    add_game(get_team('Boise State'), get_team('Ole Miss'), year, week, 2)
    add_game(get_team('Colorado State'), get_team('Colorado'), year, week, 3)
    add_game(get_team('Appalachian State'), get_team('Michigan'), year, week, 4)
    add_game(get_team('West Virginia'), get_team('Alabama'), year, week, 5)
    add_game(get_team('Ohio State'), get_team('Navy'), year, week, 6)
    add_game(get_team('Florida State'), get_team('Oklahoma State'), year, week, 7)
    add_game(get_team('Wisconsin'), get_team('LSU'), year, week, 8)
    add_game(get_team('Miami (Fla.)'), get_team('Louisville'), year, week, 9)
    add_game(get_team('Clemson'), get_team('Georgia'), year, week, 10)
    week = 2
    add_game(get_team('Pittsburgh'), get_team('Boston College'), year, week, 1)
    add_game(get_team('Michigan'), get_team('Notre Dame'), year, week, 2)
    add_game(get_team('Michigan State'), get_team('Oregon'), year, week, 3)
    add_game(get_team('East Carolina'), get_team('South Carolina'), year, week, 4)
    add_game(get_team('Brigham Young'), get_team('Texas'), year, week, 5)
    add_game(get_team('Virginia Tech'), get_team('Ohio State'), year, week, 6)
    add_game(get_team('Air Force'), get_team('Wyoming'), year, week, 7)
    add_game(get_team('Colorado State'), get_team('Boise State'), year, week, 8)
    add_game(get_team('Georgia Tech'), get_team('Tulane'), year, week, 9)
    add_game(get_team('Southern California'), get_team('Stanford'), year, week, 10)
    week = 3
    add_game(get_team('East Carolina'), get_team('Virginia Tech'), year, week, 1)
    add_game(get_team('Iowa State'), get_team('Iowa'), year, week, 2)
    add_game(get_team('West Virginia'), get_team('Maryland'), year, week, 3)
    add_game(get_team('Louisville'), get_team('Virginia'), year, week, 4)
    add_game(get_team('NC State'), get_team('South Florida'), year, week, 5)
    add_game(get_team('Arkansas'), get_team('Texas Tech'), year, week, 6)
    add_game(get_team('UCLA'), get_team('Texas'), year, week, 7)
    add_game(get_team('Penn State'), get_team('Rutgers'), year, week, 8)
    add_game(get_team('UCF'), get_team('Missouri'), year, week, 9)
    add_game(get_team('Georgia'), get_team('South Carolina'), year, week, 10)
    #week = 2
    #add_game(get_team('_team_'), get_team('_team_'), year, week, 1)
    #add_game(get_team('_team_'), get_team('_team_'), year, week, 2)
    #add_game(get_team('_team_'), get_team('_team_'), year, week, 3)
    #add_game(get_team('_team_'), get_team('_team_'), year, week, 4)
    #add_game(get_team('_team_'), get_team('_team_'), year, week, 5)
    #add_game(get_team('_team_'), get_team('_team_'), year, week, 6)
    #add_game(get_team('_team_'), get_team('_team_'), year, week, 7)
    #add_game(get_team('_team_'), get_team('_team_'), year, week, 8)
    #add_game(get_team('_team_'), get_team('_team_'), year, week, 9)
    #add_game(get_team('_team_'), get_team('_team_'), year, week, 10)

def populate_weeks():
    add_week(2014, 1)
    add_week(2014, 2)
    add_week(2014, 3)

def populate_picks():
    year = 2014
    week = 1
    user = 'aaa'
    add_pick(get_week(year, week), get_user_by_username(user), get_game(year, week, 1), game_winner=1)
    add_pick(get_week(year, week), get_user_by_username(user), get_game(year, week, 2), game_winner=1)
    add_pick(get_week(year, week), get_user_by_username(user), get_game(year, week, 3), game_winner=1)
    add_pick(get_week(year, week), get_user_by_username(user), get_game(year, week, 4), game_winner=1)
    add_pick(get_week(year, week), get_user_by_username(user), get_game(year, week, 5), game_winner=1)
    add_pick(get_week(year, week), get_user_by_username(user), get_game(year, week, 6), game_winner=1)
    add_pick(get_week(year, week), get_user_by_username(user), get_game(year, week, 7), game_winner=1)
    add_pick(get_week(year, week), get_user_by_username(user), get_game(year, week, 8), game_winner=1)
    add_pick(get_week(year, week), get_user_by_username(user), get_game(year, week, 9), game_winner=1)
    add_pick(get_week(year, week), get_user_by_username(user), get_game(year, week, 10), game_winner=1)

# Execution starts here
if __name__ == '__main__':
    print "Starting pick10 model population..."
    print "  Populating Users..."
    populate_users()
    print "  Populating Conferences and Teams..."
    populate_conferences_teams()
    print "  Populating Games..."
    populate_games()
    print "  Populating Weeks..."
    populate_weeks()
    print "  Populating Picks..."
    populate_picks()

