from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView
from accounts import views


urlpatterns = [
    path("register/", views.UserRegistrationAPIView.as_view(), name="create-user"),
    path("login/", views.UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]