# This script sends an email reminder to players that haven't entered picks.

SCRIPT_TEST = False

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

class PlayerInfo:
    player = None
    player_id = None
    email = None
    timezone = None

players = []
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

def trigger_script(deadline):
    if SCRIPT_TEST:
        return True

    # this script is run once a day at the same time
    # trigger only when script run within 24 hours of the deadline
    current_time_utc = tz.now()
    if current_time_utc <= deadline:
        time_diff = deadline - current_time_utc
        return time_diff < datetime.timedelta(1)

    return False

def find_players_without_picks(data):
    calc = CalculateResults(data)

    for player_id in data.players:
        player = data.players[player_id]

        if calc.did_player_default(player):
            p = PlayerInfo()
            p.player = player
            p.player_id = player_id
            players.append(p)

def fill_in_player_email_and_timezone():
    for i in range(len(players)):
        profile = get_profile_by_player(players[i].player)
        if profile == None or profile.user.email == None:
            print "No email address found for %s" % (players[i].player.private_name)
            players[i].email = None
            players[i].timezone = 'US/Eastern'
            continue
        players[i].email = profile.user.email

        if profile.preferredtz == None:
            players[i].timezone = 'US/Eastern'
        else:
            players[i].timezone = profile.preferredtz

def deadline_as_string(deadline_utc,timezone):
    tz = pytz.timezone(timezone)
    deadline = deadline_utc.astimezone(tz)
    date_format = "%a %m/%d/%Y %I:%M %p %Z"
    return deadline.strftime(date_format)

def get_reminder_email_text(year,week,deadline,player):
    subject = "CollegeFootballPick10 %d Week %d Picks Reminder" % (year,week)

    deadline_str = deadline_as_string(deadline,player.timezone)

    message =  "The CollegeFootballPick10 site has detected that you have not entered any picks for %d week %d.\n" % (year,week)
    message += "This email is a reminder to enter picks before the deadline at %s.\n\n" % (deadline_str)
    message += "Link to Your Enter Picks Page:\n" 
    message += "http://collegefootballpick10.pythonanywhere.com/pick10/%d/week/%d/player/%d/picks\n" % (year,week,player.player_id)

    return subject,message

def send_pick_reminder_email(year,week,deadline,player):
    subject, message = get_reminder_email_text(year,week,deadline,player)
    try:
        send_mail(subject,message,cfp_settings.DEFAULT_FROM_EMAIL,[player.email])
    except:
        print "Failed to send an email to %s" % (player.email)

def send_admin_email(year,week,deadline):
    subject = "CollegeFootballPick10 %d Week %d Picks Reminder Notification" % (year,week)

    message  = "The script to send a pick reminder email has been run.\n\n"

    if len(players) <= 0:
        message += "The script detected that all players have entered their picks.\n\n"
    else:
        message += "The script detected the following players have not entered picks:\n"
        for player in players:
            name = player.player.private_name
            email = player.email if player.email != None else 'No email address available'
            message += '%s (%s)\n' % (name,email)
        message += '\n'

        message += 'The following is an example email that was sent:\n'
        example_subject, example_message = get_reminder_email_text(year,week,deadline,players[0])
        message += example_message
        message += "\n"

    if SCRIPT_TEST:
        print subject
        print message

    to_field = ["brent.l.holden@gmail.com","blreams@gmail.com"]

    try:
        send_mail(subject,message,cfp_settings.DEFAULT_FROM_EMAIL,to_field)
    except:
        print "Failed to send an email to %s" % (to_field)


if __name__ == "__main__":

    year,week = get_current_week()
    data = database.load_week_data(year,week)
    deadline = data.week.pick_deadline

    if trigger_script(deadline):

        print "Finding players with no picks for %d week %d" % (year,week)

        find_players_without_picks(data)
        fill_in_player_email_and_timezone()

        send_admin_email(year,week,deadline)

        if len(players) == 0:
            print "All players have entered their picks."
        else:
            for player in players:
                if player.email != None:
                    print "Sending reminder email to %s" % (player.email)
                    send_pick_reminder_email(year,week,deadline,player)
