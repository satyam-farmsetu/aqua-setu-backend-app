"""
URL configuration for aqua_setu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Global admin branding
admin.site.site_header = "AquaSetu Admin"
admin.site.site_title = "AquaSetu Admin"
admin.site.index_title = "Operations Dashboard"


# OpenAPI Urls
schema_urlpatterns = [
    path("", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]


# V1 API Urls
v1_api_urlpatterns = [
    path("accounts/", include("accounts.urls.v1")),
]

urlpatterns = [
    # Admin Urls
    path("admin/", admin.site.urls),
    # OpenAPI Urls
    path("schema/", include(schema_urlpatterns)),
    # V1 API Urls
    path("v1/", include(v1_api_urlpatterns)),
]
