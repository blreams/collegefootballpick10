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
from pick10.models import PlayerYear

arguments = argparse.Namespace()

winner_tuples = [
    ("David Redys",2012,False,False,True),
    ("Jeffrey Shuey",2012,True,False,False),
    ("Adam Straw",2012,False,True,False),
    ("Douglas Martin",2011,True,True,True),
    ("Tim Penrose",2011,True,True,True),
    ("Byron Reams",2011,True,True,True),
    ("Chip Aaron",2010,True,True,False),
    ("Ike Barnes",2010,False,False,True),
    ("Jason Hucks",2010,False,False,True),
    ("Douglas Martin",2010,False,False,True),
    ("Van Steel",2010,True,True,False),
    ("Timothy Cogan",2009,True,False,False),
    ("Matt Hendrick",2009,False,False,True),
    ("Adam Straw",2009,False,True,False),
    ("Larry James",2008,True,True,False),
    ("Byron Reams",2008,False,False,True),
    ("Brooker Strom",2008,True,True,False),
    ("Kevin Farren",2007,False,False,True),
    ("Thai Nguyen",2007,True,False,False),
    ("Thomas Robbins",2007,False,True,False),
    ("Chip Aaron",2006,False,True,True),
    ("Robert Johnson",2006,False,True,True),
    ("Dale Robbins",2006,True,False,False),
    ("Robert Hawk",2005,False,True,False),
    ("Larry James",2005,False,False,True),
    ("Adam Straw",2005,True,False,False),
    ("Matthew Berger",2004,False,False,True),
    ("Daniel Desetto",2004,False,False,True),
    ("Thai Nguyen",2004,False,True,False),
    ("Kevin Staub",2004,True,False,False),
    ("Chip Aaron",2003,False,False,True),
    ("Simon Chan",2003,True,False,False),
    ("Moises Puga",2003,False,True,False),
    ("Daniel Adams",2002,False,False,True),
    ("Brent Holden",2002,False,True,False),
    ("William Murphy",2002,True,False,False),
    ("Larry James",2001,True,False,False),
    ("Thai Nguyen",2001,False,True,True),
    ("David Redys",2001,False,True,True),
    ("Brooker Strom",2001,False,True,True),
    ("William Murphy",2000,False,False,True),
    ("Dale Robbins",2000,True,False,False),
    ("Jeffrey Shuey",2000,False,True,False),
    ("Chip Aaron",1999,True,False,False),
    ("Brian Knotts",1998,True,False,False),
    ("Thai Nguyen",1997,True,False,False),
    ("Chris Fonville",2014,False,True,True),
    ("Adam Straw",2014,False,True,True),
    ("Kenneth Young",2014,True,False,False),
    ("Alexander Marsh",2013,False,True,False),
    ("Michael Neeley",2013,True,False,False),
    ("Dale Robbins",2013,False,False,True),
    ("Chris Carter",2015,False,False,True),
    ("Simon Chan",2015,False,False,True),
    ("Nick Emptage",2015,True,False,False),
    ("Alexander Marsh",2015,False,False,True),
    ("William Murphy",2015,False,True,False),
    ("Wilmaison Paul",2015,False,False,True),
    ("Jeremy Holley",2016,True,False,False),
    ("Amber Neeley",2016,False,True,True),
    ("Todd Warren",2016,False,True,True),
    ("Chris Ruffin",2017,False,False,True),
    ("Alexander Marsh",2017,True,True,False),
    ("David Stonecypher",2017,True,True,False),
    ("William Murphy",2017,False,False,True),
    ("Michael Neeley",2017,False,False,True),
    ("Alexander Marsh",2018,False,True,False),
    ("Johanna Montanez",2018,True,False,False),
    ("Douglas Martin",2018,False,False,True),
    ("Dave Locklear",2019,False,False,True),
    ("Thai Nguyen",2019,False,False,True),
    ("Matthew Berger",2019,True,False,False),
    ("David Stonecypher",2019,False,True,False),
]

def parse_arguments(args):
    global arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true', default=False, help="Run in debug mode")
    parser.add_argument('--set_winners', action='store_true', default=False, help="Without this, script does a dry run")
    arguments = parser.parse_args(args)

def set_winners():
    for private_name, year, first_place, second_place, third_place in winner_tuples:
        playeryear = PlayerYear.objects.get(player__private_name=private_name, year__yearnum=year)
        if not playeryear:
            print("ERROR: unable to get PlayerYear object for {}, {}".format(private_name, year))
        action_string = "{}:{} -".format(year, private_name)
        if first_place:
            action_string += " 1st"
            playeryear.first_place = True
        if second_place:
            action_string += " 2nd"
            playeryear.second_place = True
        if third_place:
            action_string += " 3rd"
            playeryear.third_place = True

        print(action_string)
        if not arguments.debug:
            playeryear.save()

def perform_action():
    if arguments.set_winners:
        set_winners()

def main(args=''):
    global arguments
    if not args:
        args =['--help']
    if isinstance(args, six.string_types):
        args = args.split()

    parse_arguments(args)
    perform_action()

if __name__ == "__main__":
    main(args=sys.argv[1:])

