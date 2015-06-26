from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Conference, Team, Game, Week, Pick, UserProfile

class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('conf_name', 'div_name', 'created', 'updated')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'mascot', 'created', 'updated')

def show_game_year_week_num(obj):
    return 'Year=%d, Week=%d, Game=%d' % (obj.game_year, obj.game_week, obj.game_num,)

class GameAdmin(admin.ModelAdmin):
    list_display = (show_game_year_week_num, 'team1', 'team2', 'favored', 'spread', 'kickoff', 'created', 'updated')

class WeekAdmin(admin.ModelAdmin):
    list_display = ('week_year', 'week_num', 'lock_picks', 'lock_scores', 'created', 'updated')

class PickAdmin(admin.ModelAdmin):
    list_display = ('pick_week', 'pick_user', 'pick_game', 'created', 'updated')

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Week, WeekAdmin)
admin.site.register(Pick, PickAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

