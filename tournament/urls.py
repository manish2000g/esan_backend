from django.urls import path
from .views import (
    create_tournament,
    delete_tournament,
    sponsor_list,
    sponsor_detail,
    tournament_detail,
    create_registration,
    tournament_list,
    update_registration,
    delete_registration,
    schedule_detail,
    create_participant,
    delete_participant,
    match_detail,
    create_match,
    update_match,
    delete_match,
    livepage_detail,
    update_livepage,
    announcement_detail,
    create_announcement,
)

urlpatterns = [
    path('sponsors/', sponsor_list, name='sponsor_list'),
    path('sponsors/<int:pk>/', sponsor_detail, name='sponsor_detail'),
    path('tournaments/', create_tournament, name = 'create_tournament'),
    path('tournaments/<int:pk>/delete/', delete_tournament, name='delete_tournament'),
    path('tournament_list/', tournament_list, name='tournament_list'),
    path('tournaments/<int:pk>/', tournament_detail, name='tournament_detail'),
    path('registrations/', create_registration, name='create_registration'),
    path('registrations/<int:pk>/', update_registration, name='update_registration'),
    path('registrations/<int:pk>/delete/', delete_registration, name='delete_registration'),
    path('schedules/<int:pk>/', schedule_detail, name='schedule_detail'),
    path('participants/', create_participant, name='create_participant'),
    path('participants/<int:pk>/delete/', delete_participant, name='delete_participant'),
    path('matches/<int:pk>/', match_detail, name='match_detail'),
    path('matches/', create_match, name='create_match'),
    path('matches/<int:pk>/update/', update_match, name='update_match'),
    path('matches/<int:pk>/delete/', delete_match, name='delete_match'),
    path('livepages/<int:pk>/', livepage_detail, name='livepage_detail'),
    path('livepages/<int:pk>/update/', update_livepage, name='update_livepage'),
    path('announcements/<int:pk>/', announcement_detail, name='announcement_detail'),
    path('announcements/', create_announcement, name='create_announcement'),
]
