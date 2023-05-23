from django.urls import path
from .views import create_event, create_team, delete_event, event_list, update_event 

urlpatterns = [
    path('create_event/', create_event, name='create_event'),
    path('update-event/', update_event, name='update_event'),
    path('events/', event_list, name='events'),
    path('delete-event/', delete_event, name='delete_event'),
    path('create-team/', create_team, name='create_team'),
]
