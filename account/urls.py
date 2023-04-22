from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from .views import CustomTokenObtainPairView



urlpatterns = [
     path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
     path("create-user-profile/",views.CreateUserProfile, name="create_user_profile"),
     path("get-user-profile/",views.GetUserProfile, name="get_user_profile"),
     path('teams/', views.team_list),
     path('teams/<int:pk>/', views.team_detail),
     path('games/', views.game_list, name='game_list'),
]
