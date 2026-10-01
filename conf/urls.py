"""Root URL configuration with the standard deployment health endpoint."""

from django.urls import include, path

# BEGIN BU-ISCIII APPLICATION: django-url-imports
from django.contrib import admin
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.permissions import AllowAny

API_V1_URLS = ("core.api.v1.urls", "pathocore_api")


class PublicSpectacularAPIView(SpectacularAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]


class PublicSpectacularSwaggerView(SpectacularSwaggerView):
    authentication_classes = []
    permission_classes = [AllowAny]


class PublicSpectacularRedocView(SpectacularRedocView):
    authentication_classes = []
    permission_classes = [AllowAny]
# END BU-ISCIII APPLICATION: django-url-imports

urlpatterns = [
    # Required by Compose health checks and deployment smoke tests.
    path("health/", include("deployment_health.urls")),
    # BEGIN BU-ISCIII APPLICATION: django-url-routes
    path("", RedirectView.as_view(pattern_name="v1-swagger-ui", permanent=False)),
    path("admin/", admin.site.urls),
    path("v1/openapi/", PublicSpectacularAPIView.as_view(), name="v1-schema"),
    path(
        "v1/swagger/",
        PublicSpectacularSwaggerView.as_view(url_name="v1-schema"),
        name="v1-swagger-ui",
    ),
    path(
        "v1/swagger/redoc/",
        PublicSpectacularRedocView.as_view(url_name="v1-schema"),
        name="v1-redoc",
    ),
    path("openapi/", RedirectView.as_view(pattern_name="v1-schema", permanent=False)),
    path("swagger/", RedirectView.as_view(pattern_name="v1-swagger-ui", permanent=False)),
    path(
        "swagger/redoc/",
        RedirectView.as_view(pattern_name="v1-redoc", permanent=False),
    ),
    path("v1/", include(API_V1_URLS, namespace="pathocore_api_v1")),
    path("api/v1/", include(API_V1_URLS, namespace="pathocore_api_v1_legacy")),
    path("accounts/", include("django.contrib.auth.urls")),
    # END BU-ISCIII APPLICATION: django-url-routes
]
