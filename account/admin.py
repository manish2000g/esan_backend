from django.contrib import admin

from .models import Player, BlogWriter, Organization, Organizer

# Register your models here.
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'phone_number')
admin.site.register(Player)

admin.site.register(BlogWriter)
admin.site.register(Organizer)
admin.site.register(Organization)