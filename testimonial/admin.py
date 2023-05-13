from django.contrib import admin
from .models import Testimonial


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'description','rating','is_verified')
    search_fields = ('rating', 'is_verified')

admin.site.register(Testimonial, TestimonialAdmin)