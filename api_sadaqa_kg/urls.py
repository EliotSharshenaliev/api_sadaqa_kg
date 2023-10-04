from django.contrib import admin
from django.urls import path, include

import api_sadaqa_kg.settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/catalogs/', include("catalogs.urls")),
    path('api/v1/documents/', include("documents.urls")),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),

]
