from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserSettingsProxyView, UnifiedImportViewSet
from .views_info import VersionView, HealthView

router = DefaultRouter()
router.register(r'import', UnifiedImportViewSet, basename='unified-import')

urlpatterns = [
    path('', include(router.urls)),
    path('version/', VersionView.as_view(), name='version'),
    path('health/', HealthView.as_view(), name='health'),
    path('favourites/<path:path>', UserSettingsProxyView.as_view()),
    path('favourites/', UserSettingsProxyView.as_view()),
]
