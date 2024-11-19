"""
URL configuration for meomeoknyang project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.http import HttpResponse
import logging
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

schema_view = get_schema_view(
    openapi.Info(
        title="meomeoknyang API",
        default_version='v3',
        description="API documentation for the Django project",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

try:
    logger = logging.getLogger('django')
except ValueError as e:
    logger = logging.getLogger(__name__)
    logger.error(f"Error configuring logger: {e}")


def test_logging(request):
    logger.error("This is a test error message!")  # ERROR 수준의 로그 전송
    return HttpResponse("Check your Loggly account.")


urlpatterns = [
    path('test_logging/', test_logging),

    path("admin/", admin.site.urls),
    path('', include('restaurants.urls')),  # restaurants 앱
    path('reviews/', include('reviews.urls')),
    path('users/', include('users.urls')),
    path('', include('cafe.urls')),
    path('', include('stamps.urls')),
    path('', include('search.urls')),

    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),

    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
