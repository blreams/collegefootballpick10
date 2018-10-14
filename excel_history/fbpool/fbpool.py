ROOT_PATH = '../../.'
import sys
sys.path.append(ROOT_PATH)

from scripts.api.fbpool_api import *
from fbpool_args import *
from fbpool_load import *
from fbpool_delete import *
from fbpool_list import *
from fbpool_update import *
from fbpool_cache import *
from fbpool_verify import *

# Enhancements:
# * finer grain:  load week picks, load week games, load week, load specific player week picks (?)

if __name__ == "__main__":

    fbpool_args = FBPoolArgs()
    url = fbpool_args.get_url()
    args = fbpool_args.get_args()
    action = fbpool_args.get_action()


    if action == "load_teams_most_recent_year":
        most_recent_year,excel_file = fbpool_args.get_latest_pool_file_and_year()
        fbpool = FBPoolLoad(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file,quiet=args.quiet)
        fbpool.load_teams(most_recent_year)

    elif action == "load_teams_in_year":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPoolLoad(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file,quiet=args.quiet)
        fbpool.load_teams(args.year)

    elif action == "load_players_in_year":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPoolLoad(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file,quiet=args.quiet)
        fbpool.load_players(args.year)

    elif action == "load_players_all_years":
        excel_files = fbpool_args.get_excel_files()
        for year in excel_files:
            fbpool = FBPoolLoad(url=url,excel_dir=args.excel_dir,excel_workbook=excel_files[year],quiet=args.quiet)
            fbpool.load_players(year)

    elif action == "load_week":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPoolLoad(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file,quiet=args.quiet)
        fbpool.load_week(args.year,args.week)

    elif action == "load_year":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPoolLoad(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file,quiet=args.quiet)
        fbpool.load_year(args.year)

    elif action == "update_week":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPoolUpdate(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file,quiet=args.quiet)
        fbpool.update_week(args.year,args.week)

    elif action == "delete_year":
        fbpool = FBPoolDelete(url=url,quiet=args.quiet)
        fbpool.delete_year(args.year)

    elif action == "delete_week":
        fbpool = FBPoolDelete(url=url,quiet=args.quiet)
        fbpool.delete_week(args.year,args.week)

    elif action == "delete_all":
        fbpool = FBPoolDelete(url=url,quiet=args.quiet)
        fbpool.delete_all()

    elif action == "delete_all_players":
        fbpool = FBPoolDelete(url=url,quiet=args.quiet)
        fbpool.delete_players()

    elif action == "delete_players_from_year":
        fbpool = FBPoolDelete(url=url,quiet=args.quiet)
        fbpool.delete_players_from_year(args.year)

    elif action == "delete_teams":
        fbpool = FBPoolDelete(url=url,quiet=args.quiet)
        fbpool.delete_teams()

    elif action == "flush_memcache":
        fbpool = FBPoolCache(url=url,quiet=args.quiet)
        fbpool.flush_memcache()

    elif action == "load_memcache":
        fbpool = FBPoolCache(url=url,quiet=args.quiet)
        fbpool.load_memcache()

    elif action == "load_memcache_for_year":
        fbpool = FBPoolCache(url=url,quiet=args.quiet)
        fbpool.load_memcache_for_year(args.year)

    elif action == "load_memcache_for_week":
        fbpool = FBPoolCache(url=url,quiet=args.quiet)
        fbpool.load_memcache_for_year(args.year,args.week)

    elif action == "cleanup_api":
        fbpool = FBPoolCache(url=url,quiet=args.quiet)
        fbpool.cleanup_api()

    elif action == "list_teams":
        fbpool = FBPoolList(url=url,quiet=args.quiet)
        fbpool.list_all_teams()

    elif action == "list_players":
        fbpool = FBPoolList(url=url,quiet=args.quiet)
        fbpool.list_all_players()

    elif action == "list_weeks":
        fbpool = FBPoolList(url=url,quiet=args.quiet)
        fbpool.list_all_weeks()

    elif action == "list_player_picks":
        fbpool = FBPoolList(url=url,quiet=args.quiet)
        fbpool.list_player_picks(args.year,args.week,args.player)

    elif action == "list_week_games":
        fbpool = FBPoolList(url=url,quiet=args.quiet)
        fbpool.list_week_games(args.year,args.week)

    else:
        print("")
        print("**ERROR** :  unrecognized command line arguments")
        print("")
        sys.exit(1)
