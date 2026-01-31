from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScannerModelViewSet

router = DefaultRouter()
router.register(r'scanner-models', ScannerModelViewSet, basename='scanner-model')

urlpatterns = [
    path('', include(router.urls)),
]
