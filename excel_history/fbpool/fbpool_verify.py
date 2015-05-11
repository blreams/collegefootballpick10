ROOT_PATH = '../../.'
import sys
sys.path.append(ROOT_PATH)

from scripts.api.fbpool_api import *
from scripts.api.fbpool_api_exception import *
from scripts.excel.pool_spreadsheet import *
from fbpool_player_name import *
from fbpool_error import *
from fbpool_verbose import *
import string

# Enhancements:
# * search for unassociated data
# * conflicts:  teams, player names
# * check if players in year loaded or not?  teams in year?

class FBPoolVerify:

    def __init__(self,url,quiet=False):
        self.url = url
        self.__verbose = FBPoolVerbose(quiet)

    def verify_player_exists(self,player_name,year):
        try:
            fbpool_api = FBPoolAPI(url=self.url)
            player = fbpool_api.getPlayer(player_name)
        except FBAPIException as e:
            player_does_not_exist = e.http_code == 404 and e.errmsg == "could not find the player"
            if player_does_not_exist:
                return False

            FBPoolError.exit_with_error("getting player",e)

        if year in player['years']:
            return True
        return False

    def verify_team_exists(self,team_name):
        try:
            fbpool_api = FBPoolAPI(url=self.url)
            team = fbpool_api.getTeam(team_name)
        except FBAPIException as e:
            team_does_not_exist = e.http_code == 404 and e.errmsg == "could not find the team"
            if team_does_not_exist:
                return False

            FBPoolError.exit_with_error("getting team",e)

        return True

    def check_for_missing_weeks_and_years(self):
        self.__verbose.start("checking for missing weeks...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            weeks = fbpool_api.getAllWeeks()
        except FBAPIException as e:
            FBPoolError.exit_with_error("getting all weeks",e)

        years = sorted(set([week['year'] for week in weeks ]))

        # check for missing years
        first_year = min(years)
        last_year = max(years)
        missing_years = []
        for year in range(first_year,last_year+1):
            if year not in years:
                missing_years.append(year)

        # check for missing weeks
        week_numbers = dict()
        for year in years:
            numbers = sorted([ week['number'] for week in weeks if week['year'] == year])
            week_numbers[year] = numbers

        missing = dict()
        for year in years:
            if year != last_year:
                for number in range(1,14):
                    if number not in week_numbers[year]:
                        if year not in missing:
                            missing[year] = [number]
                        else:
                            missing[year].append(number)
        
        last_week = max(week_numbers[last_year])
        for number in range(1,last_week+1):
            if number not in week_numbers[last_year]:
                if last_year not in missing:
                    missing[last_year] = [number]
                else:
                    missing[last_year].append(number)

        duplicates = dict()
        for year in years:
            first = min(week_numbers[year])
            last = max(week_numbers[year])
            for number in range(first,last+1):
                count = 0
                for current_number in week_numbers[year]:
                    if number == current_number:
                        count += 1
                if count > 1:
                    if year not in duplicates:
                        duplicates[year] = [number]
                    else:
                        duplicates[year].append(number)

        extras = dict()
        for year in years:
            for number in week_numbers[year]:
                if number < 1 or number > 13:
                    if year not in extras:
                        extras[year] = [number]
                    else:
                        extras[year].append(number)

        print ""
        if len(missing_years) == 0:
            print "Missing Years   :  None"
        else:
            print "Missing Years   : %s" % (self.__array_str(missing_years))

        if len(missing) == 0:
            print "Missing Weeks   :  None"
        else:
            print "Missing Weeks   :"
            for year in missing:
                print "           %s : %s" % (year,self.__array_str(missing[year]))

        if len(duplicates) == 0:
            print "Duplicate Weeks :  None"
        else:
            print "Duplicate Weeks :  "
            for year in duplicates:
                print "           %s : %s" % (year,self.__array_str(duplicates[year]))

        if len(extra) == 0:
            print "Extra Weeks     :  None"
        else:
            print "Extra Weeks     :  "
            for year in extra:
                print "           %s : %s" % (year,self.__array_str(extra[year]))

        print ""

    def __array_str(self,a):
        s = ""
        last = len(a)-1
        for i in range(last+1):
            if i == last:
                s += str(a[i])
            else:
                s += "%s, " % (a[i])
        return s

