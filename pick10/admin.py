from django.contrib import admin
from pick10.models import Conference, Team

class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('conf_name', 'div_name')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'mascot')

admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Team, TeamAdmin)

