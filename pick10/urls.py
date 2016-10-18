from django.conf.urls import patterns, url
from pick10 import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^commissioner$', views.commissioner, name='commissioner'),
    url(r'^commissioner/createweek$', views.create_week, name='create_week'),
    url(r'^commissioner/editweek$', views.edit_week_sel, name='edit_week_sel'),
    url(r'^commissioner/editweek/(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})$', views.edit_week, name='edit_week'),
    url(r'^commissioner/weekwinner/(?P<year_num>[0-9]{4})/week/(?P<week_num>[0-9]{1,2})$', views.set_week_winner, name='set_week_winner'),
    url(r'^(?P<year>[0-9]{4})/results$', views.overall_results, name='overall_results'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/results$', views.week_results, name='week_results'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/tiebreak$', views.tiebreak, name='tiebreak'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/games$', views.update_games, name='update_games'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/player/(?P<player_id>[0-9]+)/results$', views.player_results, name='player_results'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/player/(?P<player_id>[0-9]+)/picks$', views.enter_picks, name='enter_picks'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/update$', views.update_pages, name='update_pages'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/update/week$', views.update_week, name='update_week'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/update/tiebreak$', views.update_tiebreak, name='update_tiebreak'),
    url(r'^(?P<year>[0-9]{4})/update/overall$', views.update_overall, name='update_overall'),
)
