from django.contrib import admin

from faq.models import FAQ

# Register your models here.

class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'heading')
    search_fields = ['heading']

admin.site.register(FAQ, FAQAdmin)