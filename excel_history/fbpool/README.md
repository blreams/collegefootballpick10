FBPOOL Script
============= 

The purpose of the script fbpool.py is for database management.<br>
The main purpose of this script is to load historical pool data into the database.
<br>
It can be used to:
* load data into the database
* manipulate the memcache
* query data in the database

### Step 1.  Specify the database URL and port number

When running the fbpool.py script, the database URL and port number need to be specified.
Specify the options in one of the following ways:


```
    python -p 10090 <.. more options>
    python --port 10090 <.. more options>
```

This will use the url http://localhost:10090 as the base URL.
The default URL is http://localhost.


```
    python -u http://cdcpool.appspot.com <.. more options>
    python --url http://cdcpool.appspot.com <.. more options>
```

This will use the url http://cdcpool.appspot.com as the base URL with no port number.
This is intended for loading the production database.

### Step 2.  How to load historical pool data into the database

The following commands can be used to load historical data into the database.

#### load a year

```
    python -p 10090 --load year -y 2013  
    python --port 10090 --load year --year 2013  
```

This will load all of the data for the year 2013.
The key argument here is "--load year" which indicates a year should be loaded.

Note that if no teams have been loaded yet, then the teams for year 2013 will be loaded. 
If teams in a prior year have been loaded (say 2012), then the team names and conferences
in the 2013 sheet will not overwrite the values from 2012.  

#### load a week

```
    python -p 10090 --load week -y 2013 -w 1
    python --port 10090 --load week --year 2013 --week 1
```

This will load all of the data for 2013 week 1.
The key argument here is "--load week" which indicates a week should be loaded.

### Step 3.  Deleting data

The following commands can be used to delete data from the database.  A typical use case
could be to delete a week from the database and then reload it (for debug purposes).

#### delete a year

```
    python -p 10090 --delete year -y 2013
    python --port 10090 --delete year --year 2013
```

#### delete a week

```
    python -p 10090 --delete week -y 2013 -w 1
    python --port 10090 --delete week --year 2013 --week 1
```

### Step 4.  Updating a week

The following command is intended to be used to update a week after it is already in the database.
The use case for this is when a week is loaded but has not started yet.  Once all of the games
have completed for a week, then this command can be used to update the game scores and winner.

```
    python -p 10090 --update week -y 2013 -w 1
    python --port 10090 --update week --year 2013 --week 1
```

### Examples
```
# note:  in these examples, the target is http://localhost:10090

# load the teams the most recent year
python -p 10090 --load teams

# load the teams for a particular year
python -p 10090 --load teams --year 2010

# load the players for every year
python -p 10090 --load players

# load the players for a particular year
python -p 10090 --load players --year 2009

# load the data for a specific week
python -p 10090 --load week --year 2013 --week 4

# load the data for each week in a year
python -p 10090 --load week --year 2013

# update the game scores and winner for a week
python -p 10090 --update week --year 2013 --week 4

# delete the week data for a year
python -p 10090 --delete year --year 2013

# delete the week data for a specific week
python -p 10090 --delete year --year 2013 --week 5

# delete the entire database
python -p 10090 --delete all

# delete the players in a year
python -p 10090 --delete players --year 2012

# delete all the players in the database
python -p 10090 --delete players

# delete all the teams
python -p 10090 --delete teams

# flush the memcache
python -p 10090 --delete cache

# reload the entire memcache
python -p 10090 --load cache

# reload year data into the memcache
python -p 10090 --load cache --year 2010

# reload a specific week's data into the memcache
python -p 10090 --load cache --year 2011 --week 3

# delete a week and reload it
python -p 10090 --delete week --year 2013 --week 2
python -p 10090 --load week --year 2013 --week 2

# delete a year and reload it
python -p 10090 --delete year --year 2013
python -p 10090 --load year --year 2013

# load a year in multiple steps
python -p 10090 --load teams
python -p 10090 --load players --year 2013
python -p 10090 --load week --year 2013 --week 1
python -p 10090 --load week --year 2013 --week 2
python -p 10090 --load week --year 2013 --week 3
python -p 10090 --load week --year 2013 --week 4
python -p 10090 --load week --year 2013 --week 5
python -p 10090 --load week --year 2013 --week 6
python -p 10090 --load week --year 2013 --week 7
python -p 10090 --load week --year 2013 --week 8
python -p 10090 --load week --year 2013 --week 9
python -p 10090 --load week --year 2013 --week 10 
python -p 10090 --load week --year 2013 --week 11
python -p 10090 --load week --year 2013 --week 12
python -p 10090 --load week --year 2013 --week 13

# load a week at cdcpool.appspot.com
python --url http://cdcpool.appspot.com --load week --year 2013 --week 1

# API calls store some data in the memcache to speed up other API calls
# this call will cleanup that data from the memcache
python -p 10090 --clean api

```

List examples
```
# list all teams in database
python -p 10090 --list teams

# list all players in database
python -p 10090 --list players

# list all weeks in database
python -p 10090 --list weeks

# list a particular player picks for a week
python -p 10090 --list picks --year 2013 --week 1 --player "Brent H."

# list the games in a given week
python -p 10090 --list games --year 2013 --week 1
```

### Implementation Details

`/scripts/fbpool`<br>
this directory contains the fbpool.py script as described in this document

`/scripts/api`<br>
the fbpool.py script uses HTTP API calls to perform actions

`/scripts/excel`<br>
the fbpool.py script uses the excel directory to read the data from the excel files

`/scripts/data`<br>
this directory contains the excel files
