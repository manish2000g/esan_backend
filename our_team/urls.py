from django.urls import path
from our_team.views import create_our_team, delete_our_team, our_teams, update_our_team 

urlpatterns = [
    path('ourteam-list/', our_teams, name = 'ourteam_list'),
    path('create-team/', create_our_team, name = 'create_team'),
    path('update-team/', update_our_team, name = 'update_team'),
    path('delete-team/', delete_our_team, name = 'delete_team'),

]