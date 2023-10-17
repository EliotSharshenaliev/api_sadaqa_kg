from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Ваш API",
        default_version='v1',
        description="Описание вашего API",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Ваша лицензия"),
    ),
    public=True,
)

urlpatterns = [
    path('api/v1/auth/', include("accounts.urls")),
    path('api/v1/catalogs/', include("catalogs.urls")),
    path('api/v1/documents/', include("documents.urls")),
    path("api/v1/stripe/", include("djstripe.urls", namespace="djstripe")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('webhooks/', include("stripe_gateway.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
