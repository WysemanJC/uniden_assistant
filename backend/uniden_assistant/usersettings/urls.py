from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ScannerProfileViewSet, FrequencyViewSet, ChannelGroupViewSet, AgencyViewSet, SDCardViewSet,
    FavoritesListViewSet, FavoritesImportViewSet, UserSettingsStatsView, ClearUserSettingsDataView,
    ClearScannerRawDataView, ExportFavoritesFolderView, CGroupViewSet, TGroupViewSet,
    CFreqViewSet, TGIDViewSet, ConventionalSystemViewSet, TrunkSystemViewSet,
)

router = DefaultRouter()
router.register(r'profiles', ScannerProfileViewSet, basename='profile')
router.register(r'frequencies', FrequencyViewSet, basename='frequency')
router.register(r'channel-groups', ChannelGroupViewSet, basename='channel-group')
router.register(r'agencies', AgencyViewSet, basename='agency')
router.register(r'sd', SDCardViewSet, basename='sd')
router.register(r'favorites-lists', FavoritesListViewSet, basename='favorites-list')
router.register(r'import-files', FavoritesImportViewSet, basename='favorites-import')
router.register(r'cgroups', CGroupViewSet, basename='cgroup')
router.register(r'tgroups', TGroupViewSet, basename='tgroup')
router.register(r'cfreqs', CFreqViewSet, basename='cfreq')
router.register(r'tgids', TGIDViewSet, basename='tgid')
router.register(r'conventional-systems', ConventionalSystemViewSet, basename='conventional-system')
router.register(r'trunk-systems', TrunkSystemViewSet, basename='trunk-system')

urlpatterns = [
    path('stats/', UserSettingsStatsView.as_view()),
    path('clear-data/', ClearUserSettingsDataView.as_view()),
    path('clear-raw-data/', ClearScannerRawDataView.as_view()),
    path('export-favorites/', ExportFavoritesFolderView.as_view()),
    path('', include(router.urls)),
]
