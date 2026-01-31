from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CountryViewSet, StateViewSet, CountyViewSet,
    HPDBAgencyViewSet, HPDBChannelGroupViewSet, HPDBFrequencyViewSet,
    HPDBTreeViewSet, HPDBImportViewSet, HPDBStatsView,
)

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='hpdb-country')
router.register(r'states', StateViewSet, basename='hpdb-state')
router.register(r'counties', CountyViewSet, basename='hpdb-county')
router.register(r'agencies', HPDBAgencyViewSet, basename='hpdb-agency')
router.register(r'channel-groups', HPDBChannelGroupViewSet, basename='hpdb-channel-group')
router.register(r'frequencies', HPDBFrequencyViewSet, basename='hpdb-frequency')
router.register(r'tree', HPDBTreeViewSet, basename='hpdb-tree')
router.register(r'import-files', HPDBImportViewSet, basename='hpdb-import')

urlpatterns = [
    path('stats/', HPDBStatsView.as_view()),
    path('', include(router.urls)),
]
