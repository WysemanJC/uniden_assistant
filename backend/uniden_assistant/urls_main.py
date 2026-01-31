"""
URL configuration for uniden_assistant project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/uniden_manager/', include('uniden_assistant.uniden_manager.urls')),
    path('api/hpdb/', include('uniden_assistant.hpdb.urls')),
    path('api/usersettings/', include('uniden_assistant.usersettings.urls')),
    path('api/appconfig/', include('uniden_assistant.appconfig.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
