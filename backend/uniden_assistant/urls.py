from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScannerProfileViewSet, FrequencyViewSet, ChannelGroupViewSet, AgencyViewSet

router = DefaultRouter()
router.register(r'profiles', ScannerProfileViewSet)
router.register(r'frequencies', FrequencyViewSet)
router.register(r'channel-groups', ChannelGroupViewSet)
router.register(r'agencies', AgencyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
