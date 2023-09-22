from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from images.views import ServeProtectedMedia


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include('users.urls')),
    path('users/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('images/', include('images.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^imgs/(?P<file_path>.+)$', ServeProtectedMedia.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
