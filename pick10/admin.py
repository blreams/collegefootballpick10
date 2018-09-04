from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext_lazy
from pick10.models import get_profile_by_player

from .models import Year, Player, PlayerYear, Conference, Team, Game, Week, Pick, UserProfile
from .forms import UserProfileForm

site_text = 'College Football Pick10'
# Text to put at the end of each page's <title>
admin.site.site_title = ugettext_lazy(site_text + ' site admin')
# Text to put in each page's <h1> (and above login form).
admin.site.site_header = ugettext_lazy(site_text + ' administration')
# Text to put at the top of the admin index page.
admin.site.index_title = ugettext_lazy(site_text + ' administration')

class YearAdmin(admin.ModelAdmin):
    list_display = ('yearnum', 'entry_fee', 'payout_week', 'payout_first', 'payout_second', 'payout_third')

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('public_name', 'private_name', 'ss_name')

class PlayerYearAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'player', 'year')
    list_filter = ('year', 'player')
    ordering = ('-year', 'player') # Default ordering is reverse year, then player

    # Create a user_name entry for PlayerYear table
    def user_name(self, instance):
        rv = ''
        profile = get_profile_by_player(instance.player)
        if profile is not None:
            rv = profile.user.username
        return rv
    # Set the ordering for user_name
    user_name.admin_order_field = 'player__userprofile__user__username'

    # Create a user_email entry for PlayerYear table
    def user_email(self, instance):
        rv = ''
        profile = get_profile_by_player(instance.player)
        if profile is not None:
            rv = profile.user.email
        return rv
    # Set the ordering for user_email
    user_email.admin_order_field = 'player__userprofile__user__email'

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
    list_display = ('player', 'game', 'winner', 'created', 'updated')
    list_filter = ('game__week__year', 'game__week__weeknum', 'game__gamenum', 'player')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'player', 'company', 'preferredtz', 'favorite_team')
    list_filter = ('company', 'favorite_team', 'preferredtz')

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    ordering = ('username',)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'player')

    def player(self, obj):
        try:
            player = obj.userprofile.player.ss_name
            return player
        except:
            return ""

    player.short_description = 'Player'
    player.admin_order_field = 'last_name'

admin.site.register(Year, YearAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerYear, PlayerYearAdmin)
admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Week, WeekAdmin)
admin.site.register(Pick, PickAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

