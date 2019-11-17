#!/bin/bash

source virtualenvwrapper.sh
workon cdcpool
/home/collegefootballpick10/.virtualenvs/cdcpool_py3/bin/postactivate
workon cdcpool
python /home/collegefootballpick10/collegefootballpick10/email_players_with_no_picks.py

