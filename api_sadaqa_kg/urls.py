import django.conf
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from api_sadaqa_kg.drf_yasg import urlpatterns as yasg_urlpatterns
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/webhooks/', include("webhooks.urls")),
    path('api/v1/auth/', include("accounts.urls")),
    path('api/v1/catalogs/', include("catalogs.urls")),
    path('api/v1/documents/', include("documents.urls")),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
]

urlpatterns += yasg_urlpatterns if django.conf.settings.DEBUG else []

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)