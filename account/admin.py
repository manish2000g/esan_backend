from django.contrib import admin
from .models import Player, BlogWriter, Organization, Organizer,UserProfile

# Register your models here.


# class OrganizationAdmin(admin.ModelAdmin):
#     inlines = [TeamInline]

admin.site.register(Player)
admin.site.register(UserProfile)
admin.site.register(BlogWriter)
admin.site.register(Organizer)
admin.site.register(Organization)
# admin.site.register(Team)
