from django.contrib import admin
from .models import Testimonial


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('full_name', 'email')

admin.site.register(Testimonial, TestimonialAdmin)