from catalogs.views import GetUser

from django.urls import path

urlpatterns = [
    path('get-user/', GetUser.as_view(), name="Get user"),

]
