from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path("api-token-auth/",views.CustomAuthToken.as_view(), name="login_api_token_auth"),
     path("create-user-profile/",views.CreateUserProfile, name="create_user_profile"),
     path('teams/', views.team_list),
     path('teams/<int:pk>/', views.team_detail),
     path('games/', views.game_list, name='game_list'),
]
