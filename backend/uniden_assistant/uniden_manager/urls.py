from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserSettingsProxyView, UnifiedImportViewSet

router = DefaultRouter()
router.register(r'import', UnifiedImportViewSet, basename='unified-import')

urlpatterns = [
    path('', include(router.urls)),
    path('favourites/<path:path>', UserSettingsProxyView.as_view()),
    path('favourites/', UserSettingsProxyView.as_view()),
]
