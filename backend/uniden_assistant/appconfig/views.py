from rest_framework import viewsets
from .models import ScannerModel
from .serializers import ScannerModelSerializer


class ScannerModelViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only app configuration for supported scanner models"""
    queryset = ScannerModel.objects.all()
    serializer_class = ScannerModelSerializer
