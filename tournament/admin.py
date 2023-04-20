from django.contrib import admin

from tournament.models import BannerImage, DuelMatch, FFAMatch, FFAScore, Result, Game, PrizePool, Registration, Schedule, Tournament, Announcement, LivePage, Sponsor, Post, Participant, Match, TournamentBracket

# Register your models here.
class SponsorInline(admin.StackedInline):
    model = Sponsor

class BannerImageInline(admin.StackedInline):
    model = BannerImage
    
class PrizeInline(admin.StackedInline):
    model = PrizePool

class ScheduleInline(admin.StackedInline):
    model = Schedule
    
class MatchInline(admin.StackedInline):
    model = Match

class DuelMatchInline(admin.StackedInline):
    model = DuelMatch

class FFAMatchInline(admin.StackedInline):
    model = FFAMatch

class FFAScoreInline(admin.TabularInline):
    model = FFAScore

class FFAMatchAdmin(admin.ModelAdmin):
    inlines = [
        FFAScoreInline,
    ]    
 
class MatchAdmin(admin.ModelAdmin):
    inlines = [
        DuelMatchInline, FFAMatchInline
    ]
    list_display = ['game', 'match_type', 'is_completed']
    list_filter = ['game', 'match_type']
    search_fields = ['game__name', 'match_type']
    actions = ['complete_match']

class GameAdmin(admin.ModelAdmin):
    inlines = [MatchInline]

class TournamentAdmin(admin.ModelAdmin):
    inlines = [SponsorInline, BannerImageInline, ScheduleInline, PrizeInline]
    list_display = ('name', 'start_date', 'end_date', 'organizer')
    search_fields = ('name', 'description', 'organizer__name')
    list_filter = ('start_date', 'end_date')
    date_hierarchy = 'start_date'
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'match', 'start_time', 'end_time')
    list_filter = ('tournament',)
    search_fields = ('tournament__name', 'match__player_1__name', 'match__player_2__name')

admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Registration)
admin.site.register(Match, MatchAdmin)
admin.site.register(FFAMatch, FFAMatchAdmin)  
admin.site.register(DuelMatch)
admin.site.register(Announcement)
admin.site.register(LivePage)
admin.site.register(Sponsor)
admin.site.register(Post)
admin.site.register(Participant)
admin.site.register(TournamentBracket)
admin.site.register(Game, GameAdmin)
admin.site.register(Result)
