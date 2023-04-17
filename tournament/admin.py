from django.contrib import admin

from tournament.models import BannerImage, Game, PrizePool, Registration, Tournament, Announcement, LivePage, Sponsor, Post, Participant, Match, TournamentBracket

# Register your models here.
class SponsorInline(admin.StackedInline):
    model = Sponsor

class BannerImageInline(admin.StackedInline):
    model = BannerImage
    
class PrizeInline(admin.StackedInline):
    model = PrizePool

class MatchInline(admin.TabularInline):
    model = Match

class GameAdmin(admin.ModelAdmin):
    inlines = [MatchInline]

class TournamentAdmin(admin.ModelAdmin):
    inlines = [SponsorInline, BannerImageInline, PrizeInline]
    list_display = ('name', 'start_date', 'end_date', 'organizer')
    search_fields = ('name', 'description', 'organizer__name')
    list_filter = ('start_date', 'end_date')
    date_hierarchy = 'start_date'


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Registration)
admin.site.register(Announcement)
admin.site.register(LivePage)
admin.site.register(Match)
admin.site.register(Sponsor)
admin.site.register(Post)
admin.site.register(Participant)
admin.site.register(TournamentBracket)
admin.site.register(Game, GameAdmin)