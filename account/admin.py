from django.contrib import admin
from .models import Player, BlogWriter, Organization, Organizer,UserProfile, Team

# Register your models here.
class TeamInline(admin.StackedInline):
    model = Team

class OrganizationAdmin(admin.ModelAdmin):
    inlines = [TeamInline]

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'phone_number')

admin.site.register(Player)
admin.site.register(UserProfile)
admin.site.register(BlogWriter)
admin.site.register(Organizer)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Team)
