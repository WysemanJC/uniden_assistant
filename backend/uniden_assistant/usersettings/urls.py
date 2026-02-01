from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ScannerProfileViewSet, FrequencyViewSet, ChannelGroupViewSet, AgencyViewSet, SDCardViewSet,
    FavoritesListViewSet, FavoritesImportViewSet, UserSettingsStatsView, ClearUserSettingsDataView,
)

router = DefaultRouter()
router.register(r'profiles', ScannerProfileViewSet, basename='profile')
router.register(r'frequencies', FrequencyViewSet, basename='frequency')
router.register(r'channel-groups', ChannelGroupViewSet, basename='channel-group')
router.register(r'agencies', AgencyViewSet, basename='agency')
router.register(r'sd', SDCardViewSet, basename='sd')
router.register(r'favorites-lists', FavoritesListViewSet, basename='favorites-list')
router.register(r'import-files', FavoritesImportViewSet, basename='favorites-import')

urlpatterns = [
    path('stats/', UserSettingsStatsView.as_view()),
    path('clear-data/', ClearUserSettingsDataView.as_view()),
    path('', include(router.urls)),
]
