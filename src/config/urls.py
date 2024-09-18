from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler403, handler400, handler500, handler404
from django.shortcuts import render
from web.users.views import HomePageView
import debug_toolbar
# from web.appointments.api.views import api_home
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(TokenAuthentication,),
)


def custom_permission_denied_view(request, exception=None):
    return render(request, 'errors/403.html', status=403)


def custom_bad_request_view(request, exception=None):
    return render(request, 'errors/400.html', status=400)


def custom_error_view(request):
    return render(request, 'errors/500.html', status=500)


def custom_404_view(request, exception):
    return render(request, 'errors/404.html', status=404)


handler403 = custom_permission_denied_view
handler400 = custom_bad_request_view
handler500 = custom_error_view
handler404 = custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls, name='admin_site'),
    path('api/', include('web.appointments.api.urls')),
    re_path('swagger/', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),

    path('appointments/', include('web.appointments.urls')),
    path('medical_records/', include('web.medical_records.urls')),
    path('users/', include('web.users.urls')),
    path('', HomePageView.as_view(), name='index'),
    path('__debug__/', include(debug_toolbar.urls))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
