from .import views
from django.urls import path

urlpatterns = [
    path('create_testimonials/', views.submit_testimonial, name='create_testimonial'),
    path('testimonials/', views.get_testimonials, name='testimonials'),
    path('testimonials/<int:pk>/', views.get_testimonial, name='testimonial'),
    path('testimonials/<int:pk>/edit/', views.edit_testimonial, name='edit_testimonial'),
    path('testimonials/<int:pk>/delete/', views.delete_testimonial, name='delete_testimonial'),
]
