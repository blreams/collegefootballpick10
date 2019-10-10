from django.conf.urls import url
from .views import index
from .views import profile
from .views import commissioner
from .views import create_week
from .views import edit_week_sel
from .views import edit_week
from .views import set_week_winner
from .views import overall_results
from .views import week_results
from .views import tiebreak
from .views import update_games
from .views import player_results
from .views import player_stats
from .views import enter_picks
from .views import update_pages
from .views import update_week
from .views import update_tiebreak
from .views import update_overall

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^profile$', profile, name='profile'),
    url(r'^commissioner$', commissioner, name='commissioner'),
    url(r'^commissioner/createweek$', create_week, name='create_week'),
    url(r'^commissioner/editweek$', edit_week_sel, name='edit_week_sel'),
    url(r'^commissioner/editweek/(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})$', edit_week, name='edit_week'),
    url(r'^commissioner/weekwinner/(?P<year_num>[0-9]{4})/week/(?P<week_num>[0-9]{1,2})$', set_week_winner, name='set_week_winner'),
    url(r'^(?P<year>[0-9]{4})/results$', overall_results, name='overall_results'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/results$', week_results, name='week_results'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/tiebreak$', tiebreak, name='tiebreak'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/games$', update_games, name='update_games'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/player/(?P<player_id>[0-9]+)/results$', player_results, name='player_results'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/player/(?P<player_id>[0-9]+)/picks$', enter_picks, name='enter_picks'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/update$', update_pages, name='update_pages'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/update/week$', update_week, name='update_week'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/update/tiebreak$', update_tiebreak, name='update_tiebreak'),
    url(r'^(?P<year>[0-9]{4})/update/overall$', update_overall, name='update_overall'),
    url(r'^stats/player/(?P<player_id>[0-9]+)/all$', player_stats, name='player_stats'),
]

