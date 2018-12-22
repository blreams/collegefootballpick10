from pick10.models import *
from pick10.tests.unit_test_database import UnitTestDatabase
from pick10.calculator import CalculateResults, FINAL
from pick10.database import Database
from pick10.calculate_tiebreak import CalculateTiebreak
from pick10.week_winner import WeekWinner

yearnum = 1978
weeknum = 1
playerid = 1
test_db = UnitTestDatabase()
test_db.setup_week_final(yearnum, weeknum)
test_db.setup_week_no_picks(yearnum, weeknum+1, FINAL)
database = Database()
week_data = database.load_week_data(yearnum, weeknum)
calc = CalculateResults(week_data)
player = week_data.players[playerid]
week = week_data.week
game = calc.get_featured_game()
winners = WeekWinner(yearnum, weeknum)

calc.get_player_submit_time(player, week)
ctb = CalculateTiebreak(yearnum, weeknum)

