from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Year, Player, PlayerYear, Conference, Team, Game, Week, Pick, UserProfile

class YearAdmin(admin.ModelAdmin):
    list_display = ('yearnum', 'entry_fee', 'payout_week', 'payout_first', 'payout_second', 'payout_third')

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('public_name', 'private_name', 'ss_name')

class PlayerYearAdmin(admin.ModelAdmin):
    list_display = ('player', 'year')
    list_filter = ('year', 'player')

class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('conf_name', 'div_name', 'created', 'updated')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'mascot', 'created', 'updated')
    list_filter = ('conference',)

def show_year_week_game(obj):
    return 'Year=%d, Week=%d, Game=%d' % (obj.week.year.yearnum, obj.week.weeknum, obj.gamenum,)

class GameAdmin(admin.ModelAdmin):
    list_display = (show_year_week_game, 'team1', 'team2', 'favored', 'spread', 'winner', 'kickoff', 'created', 'updated')
    list_filter = ('week__year', 'week__weeknum')

class WeekAdmin(admin.ModelAdmin):
    list_display = ('year', 'weeknum', 'lock_picks', 'lock_scores', 'created', 'updated')
    list_filter = ('year',)

class PickAdmin(admin.ModelAdmin):
    list_display = ('player', 'game', 'created', 'updated')
    list_filter = ('game__week__year', 'game__week__weeknum', 'player')

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

admin.site.register(Year, YearAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerYear, PlayerYearAdmin)
admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Week, WeekAdmin)
admin.site.register(Pick, PickAdmin)
admin.site.register(UserProfile)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

