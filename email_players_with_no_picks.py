# This script sends an email reminder to players that haven't entered picks.

SCRIPT_TEST = True

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collegefootballpick10.settings')

import django
django.setup()

from django.core.mail import send_mail

from pick10.database import *
from pick10.calculator import *
from pick10.models import *
import django.utils.timezone as tz
import datetime
import collegefootballpick10.settings as cfp_settings


database = Database()

def get_current_week():
    weeks_and_years = database.load_weeks_and_years()
    assert weeks_and_years != None

    years = weeks_and_years.keys()
    assert years != None and len(years) > 0

    current_year = max(weeks_and_years.keys())

    weeks = weeks_and_years[current_year]
    assert weeks != None and len(weeks) > 0

    current_week = max(weeks_and_years[current_year])

    return current_year,current_week

def trigger_script(data):
    if SCRIPT_TEST:
        return True

    # this script is run once a day at the same time
    # trigger only when script run within 24 hours of the deadline
    current_time_utc = tz.now()
    if current_time_utc <= data.week.pick_deadline:
        time_diff = data.week.pick_deadline - current_time_utc
        return time_diff < datetime.timedelta(1)

    return False

def get_players_without_picks(data):
    calc = CalculateResults(data)

    players = []
    for player_id in data.players:
        player = data.players[player_id]

        if calc.did_player_default(player):
            players.append(player)
    return players

def get_email_addresses(players):
    addresses = []
    for player in players:
        profile = get_profile_by_player(player)
        if profile == None:
            print "No email address found for %s" % (player.private_name)
            continue
        addresses.append(profile.user.email)
    return addresses

def deadline_as_string(deadline_utc):
    tz = pytz.timezone('US/Eastern')
    deadline_est = deadline_utc.astimezone(tz)
    date_format = "%a %m/%d/%Y %I:%M %p %Z"
    return deadline_est.strftime(date_format)

def send_email(year,week,deadline,addresses):
    subject = "CollegeFootballPick10 %d Week %d Picks Reminder" % (year,week)

    message = "The CollegeFootballPick10 site has detected that you have not entered any picks for %d week %d.\n" % (year,week) +\
              "This email is a reminder to enter picks before the deadline at %s." % (deadline_as_string(deadline))

    send_mail(subject,message,cfp_settings.DEFAULT_FROM_EMAIL,addresses)

def script_test_email(year,week,deadline,addresses):
    subject = "CollegeFootballPick10 %d Week %d Picks Reminder TEST" % (year,week)

    message = "This is a test email for the Picks Reminder Email Script\n\n"
    message += "The following players have not entered picks yet:\n"

    for addr in email_addresses:
        message += "%s\n" % (addr)

    to_field = ["brent.l.holden@gmail.com","blreams@gmail.com"]

    send_mail(subject,message,cfp_settings.DEFAULT_FROM_EMAIL,to_field)


# if an error occurs, just let the script fail with an exception
if __name__ == "__main__":
    year,week = get_current_week()
    print "Finding players with no picks for %d week %d" % (year,week)

    data = database.load_week_data(year,week)
   
    if trigger_script(data):

        players = get_players_without_picks(data)
        email_addresses = get_email_addresses(players)

        if SCRIPT_TEST:
            script_test_email(year,week,data.week.pick_deadline,email_addresses)
        else:
            send_email(year,week,data.week.pick_deadline,email_addresses)

