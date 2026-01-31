from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ScannerProfile, Frequency, ChannelGroup, Agency
from .serializers import ScannerProfileSerializer, FrequencySerializer, ChannelGroupSerializer, AgencySerializer


class ScannerProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for scanner profiles."""
    queryset = ScannerProfile.objects.all()
    serializer_class = ScannerProfileSerializer

    @action(detail=True, methods=['get'])
    def frequencies(self, request, pk=None):
        """Get all frequencies for a profile across all channel groups."""
        profile = self.get_object()
        frequencies = Frequency.objects.filter(channel_group__profile=profile)
        serializer = FrequencySerializer(frequencies, many=True)
        return Response(serializer.data)


class ChannelGroupViewSet(viewsets.ModelViewSet):
    """ViewSet for channel groups."""
    queryset = ChannelGroup.objects.all()
    serializer_class = ChannelGroupSerializer

    def get_queryset(self):
        """Filter by profile if provided."""
        queryset = ChannelGroup.objects.all()
        profile_id = self.request.query_params.get('profile', None)
        if profile_id is not None:
            queryset = queryset.filter(profile_id=profile_id)
        return queryset


class FrequencyViewSet(viewsets.ModelViewSet):
    """ViewSet for frequencies."""
    queryset = Frequency.objects.all()
    serializer_class = FrequencySerializer

    def get_queryset(self):
        """Filter by channel group if provided."""
        queryset = Frequency.objects.all()
        channel_group_id = self.request.query_params.get('channel_group', None)
        if channel_group_id is not None:
            queryset = queryset.filter(channel_group_id=channel_group_id)
        return queryset


class AgencyViewSet(viewsets.ModelViewSet):
    """ViewSet for agencies."""
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
