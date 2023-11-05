from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from .custom_schema import CustomSchemaGenerator


schema_view = get_schema_view(
    openapi.Info(
        title="AI Revolution API",
        default_version='v1',
        description="API for AI Revolution project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="legas@yandex.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=CustomSchemaGenerator,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('prompts.urls')),
    path('api/v1/', include('notekeeper.urls')),

    # path('api/v1/conversations/', include('conversations.urls')),

    path('api-auth/', include('rest_framework.urls')),

    path('docs/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
