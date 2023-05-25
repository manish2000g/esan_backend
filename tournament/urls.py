from django.urls import path
from .views import create_event, create_team, delete_event, event_list, delete_team,retrieve_team,update_event,get_my_team,update_team,create_team_initials

urlpatterns = [
    path('create_event/', create_event, name='create_event'),
    path('update-event/', update_event, name='update_event'),
    path('events/', event_list, name='events'),
    path('delete-event/', delete_event, name='delete_event'),
    path('get-my-team/', get_my_team, name='get_my_team'),
    path('create-team-initials/', create_team_initials, name='create_team_initials'),
    path('retrive-team-detail/', retrieve_team, name='retrieve_team'),
    path('create-team/', create_team, name='create_team'),
    path('update-team/', update_team, name='create_team'),
    path('delete-team/', delete_team, name='delete_team'),
]
