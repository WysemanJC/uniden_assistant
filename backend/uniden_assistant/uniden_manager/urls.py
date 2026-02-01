from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HPDBProxyView, UserSettingsProxyView, AppConfigProxyView, UnifiedImportViewSet

router = DefaultRouter()
router.register(r'import', UnifiedImportViewSet, basename='unified-import')

urlpatterns = [
    path('', include(router.urls)),
    path('hpdb/<path:path>', HPDBProxyView.as_view()),
    path('hpdb/', HPDBProxyView.as_view()),
    path('usersettings/<path:path>', UserSettingsProxyView.as_view()),
    path('usersettings/', UserSettingsProxyView.as_view()),
    path('appconfig/<path:path>', AppConfigProxyView.as_view()),
    path('appconfig/', AppConfigProxyView.as_view()),
]
