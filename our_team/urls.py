from django.urls import path
from our_team.views import OurTeams,CreateOurTeam,UpdateOurTeam,DeleteOurTeam

urlpatterns = [
    path('ourteam-list/', OurTeams, name = 'ourteam_list'),
    path('create-ourteam/', CreateOurTeam, name = 'create_our_team'),
    path('update-ourteam/', UpdateOurTeam, name = 'update_ourteam'),
    path('delete-ourteam/', DeleteOurTeam, name = 'delete_ourteam'),
]