from django.urls import path
from .views import Create_Event, Delete_Event, EventList, Update_Event,CreateTeam

urlpatterns = [
    path('create_event/', Create_Event, name='create_event'),
    path('update-event/<int:pk>/', Update_Event, name='update_event'),
    path('events/', EventList, name='events'),
    path('delete-event/<int:pk>/', Delete_Event, name='delete_event'),
    path('create-team/', CreateTeam, name='create_team'),
]
