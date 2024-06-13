from django.contrib import admin
from django.urls import path,include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Instahyre API",
        default_version="v1",
        description="API documentation for Instahyre project",
    ),
    public=True,
)

urlpatterns = [
    path(
        "api/",
        include(
            [
                path(
                    "redoc/",
                    schema_view.with_ui("redoc", cache_timeout=0),
                    name="schema-redoc",
                ),
                path(
                    "swagger/",
                    schema_view.with_ui("swagger", cache_timeout=0),
                    name="swagger-ui",
                ),
            ]
        ),
    ),
    path('admin/', admin.site.urls),
    path('api/', include('phonebook.urls')),
]