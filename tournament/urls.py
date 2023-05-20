from django.urls import path

from tournament.views import Create_Event, Delete_Event, EventList, Update_Event

urlpatterns = [
    path('create_event/', Create_Event, name='create_event'),
    path('update_event/<int:pk>/', Update_Event, name='update_event'),
    path('events/', EventList, name='events'),
    path('delete_event/<int:pk>/', Delete_Event, name='delete_event')  
]
