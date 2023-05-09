from django.urls import path
from .views import submit_testimonial

urlpatterns = [
    path('testimonials/', submit_testimonial, name='submit_testimonial')
]
