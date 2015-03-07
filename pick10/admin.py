from django.contrib import admin
from pick10.models import Conference, Team, Game, Week, Pick

class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('conf_name', 'div_name')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'mascot')

class GameAdmin(admin.ModelAdmin):
    list_display = ('game_year', 'game_week', 'game_num', 'team1', 'team2')

class WeekAdmin(admin.ModelAdmin):
    list_display = ('week_year', 'week_num', 'lock_picks', 'lock_scores')

class PickAdmin(admin.ModelAdmin):
    list_display = ('pick_week', 'pick_user', 'pick_game')

admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Week, WeekAdmin)
admin.site.register(Pick, PickAdmin)

