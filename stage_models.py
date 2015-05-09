import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collegefootballpick10.settings')

import django
django.setup()

from pick10.models import Team
from pick10.models import add_user, add_conference, add_team, add_game, add_week, add_pick
from pick10.models import get_user_by_username, get_team, get_game, get_week

def populate_users():
    add_user('aaa', 'aaa@aaa.com', 'aaa', 'aaa')

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

