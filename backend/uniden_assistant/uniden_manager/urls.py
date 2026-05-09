from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UnifiedImportViewSet
from .views_info import VersionView, HealthView

router = DefaultRouter()
router.register(r'import', UnifiedImportViewSet, basename='unified-import')

urlpatterns = [
    path('', include(router.urls)),
    path('version/', VersionView.as_view(), name='version'),
    path('health/', HealthView.as_view(), name='health'),
    # Route favourites directly in-process — no HTTP proxy round-trip
    path('favourites/', include('uniden_assistant.favourites.urls')),
]
