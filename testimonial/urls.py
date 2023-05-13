from .import views
from django.urls import path
from .views import all_testimonials, submit_testimonial,verify_testimonial,update_testimonial,testimonials

urlpatterns = [
    path('submit-testimonial/', submit_testimonial, name='submit_testimonial'),
    path('verify-testimonial/', verify_testimonial, name='verify_testimonial'),
    path('update-testimonial/', update_testimonial, name='update_testimonial'),
    path('testimonials/', testimonials, name='testimonials'),
    path('all-testimonials/', all_testimonials, name='testimonials'),
]
