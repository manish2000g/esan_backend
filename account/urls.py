from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
     path('change-password/', views.ChangePasswordView.as_view(),name='change-password'),
     path("create-user-profile/",views.CreateUserProfile, name="create_user_profile"),
     path("verify-user-profile/",views.VerifyUserProfile, name="verify_user_profile"),
     path("get-user-profile/",views.GetUserProfile, name="get_user_profile"),
     path("get-user-profile-detail/",views.GetUserProfileDetail, name="get_user_profile_detail"),
     path("get-user-lists/",views.GetUsers, name="get_users"),
     path("get-user-detail/",views.GetUserDetail, name="get_user_detail"),
     path("update-user-detail/",views.UpdateUserDetail, name="update_user_detail"),
     path('games/', views.game_list, name='game_list'),
     path('organization-players/', views.organization_players, name='organization_players'),
     path('all-players/', views.all_players, name='all_players'),
     path('request-player/', views.request_player, name='request_player'),
     path('my-requests/', views.my_requests, name='my_requests'),
     path('accept-request/', views.accept_request, name='accept_request'),
     path('delete-request/', views.delete_request, name='delete_request'),
     path('reject-request/', views.reject_request, name='reject_request'),
]
