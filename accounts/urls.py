from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView
)
from accounts import views


urlpatterns = [
    path("register/", views.UserRegistrationAPIView.as_view(), name="create-user"),
    path('user/', views.UserAPIView.as_view(), name="user"),
    path("login/", TokenObtainPairView.as_view(), name="login"),

    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),

]