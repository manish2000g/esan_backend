from django.contrib import admin

from tournament.models import Tournament, Announcement, LivePage, Match, Sponsor, Schedule, Post, Participant

# Register your models here.
admin.site.register(Tournament)
admin.site.register(Announcement)
admin.site.register(LivePage)
admin.site.register(Match)
admin.site.register(Sponsor)
admin.site.register(Schedule)
admin.site.register(Post)
admin.site.register(Participant)