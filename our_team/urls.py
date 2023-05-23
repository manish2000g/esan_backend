from django.urls import path
from our_team.views import OurTeams,CreateOurTeam,UpdateOurTeam,DeleteOurTeam

urlpatterns = [
    path('ourteam-list/', OurTeams, name = 'ourteam_list'),
    path('create-team/', CreateOurTeam, name = 'create_team'),
    path('update-team/', UpdateOurTeam, name = 'update_team'),
    path('delete-team/', DeleteOurTeam, name = 'delete_team'),
]