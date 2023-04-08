from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path("api-token-auth/",views.CustomAuthToken.as_view(), name="login_api_token_auth"),
]
