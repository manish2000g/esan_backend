from django.contrib import admin

from tournament.models import BannerImage, Event, Result, Group, Game, PrizePool, Registration, Round, Schedule, Team, Tournament, Announcement, LivePage, Sponsor, Participant, Match, TournamentBracket

# Register your models here.
class SponsorInline(admin.StackedInline):
    model = Sponsor

class AnnouncementInline(admin.StackedInline):
    model = Announcement

class TournamentInline(admin.StackedInline):
    model = Tournament

class BannerImageInline(admin.StackedInline):
    model = BannerImage
    
class PrizeInline(admin.StackedInline):
    model = PrizePool

class ScheduleInline(admin.StackedInline):
    model = Schedule
    
class MatchInline(admin.StackedInline):
    model = Match

class RoundInline(admin.TabularInline):
    model = Round

class GroupInline(admin.TabularInline):
    model = Group

class EventAdmin(admin.ModelAdmin):
    inlines = [TournamentInline]

class TournamentBracketAdmin(admin.ModelAdmin):
    inlines = [RoundInline, GroupInline]  

class GameAdmin(admin.ModelAdmin):
    inlines = [MatchInline]

class EventAdmin(admin.ModelAdmin):
    inlines = [AnnouncementInline]

class TournamentAdmin(admin.ModelAdmin):
    inlines = [SponsorInline, BannerImageInline, ScheduleInline, PrizeInline]
    search_fields = ('name', 'description', 'organizer__name')
    list_filter = ('start_date', 'end_date')
    date_hierarchy = 'start_date'

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'match', 'start_time', 'end_time')
    list_filter = ('tournament', 'match')
    search_fields = ('tournament__name', 'match__team_1__name', 'match__team_2__name')

admin.site.register(Team)
admin.site.register(Event, EventAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Registration)
admin.site.register(Match)
admin.site.register(Announcement)
admin.site.register(LivePage)
admin.site.register(Sponsor)
admin.site.register(Participant)
admin.site.register(TournamentBracket, TournamentBracketAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Result)
