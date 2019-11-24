#!/bin/bash

source virtualenvwrapper.sh
workon cdcpool
/home/collegefootballpick10/.virtualenvs/cdcpool/bin/postactivate
workon cdcpool
python /home/collegefootballpick10/collegefootballpick10/email_players_with_no_picks.py

