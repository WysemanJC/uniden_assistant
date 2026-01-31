from rest_framework import serializers
from .models import ScannerProfile, Frequency, ChannelGroup, Agency


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ['id', 'name', 'description', 'created_at']


class FrequencySerializer(serializers.ModelSerializer):
    agency_name = serializers.CharField(source='agency.name', read_only=True)

    class Meta:
        model = Frequency
        fields = [
            'id', 'channel_group', 'frequency', 'name', 'agency', 'agency_name',
            'modulation', 'description', 'priority', 'enabled', 'created_at', 'updated_at'
        ]


class ChannelGroupSerializer(serializers.ModelSerializer):
    frequencies = FrequencySerializer(many=True, read_only=True)

    class Meta:
        model = ChannelGroup
        fields = ['id', 'profile', 'name', 'description', 'frequencies', 'created_at']


class ScannerProfileSerializer(serializers.ModelSerializer):
    channel_groups = ChannelGroupSerializer(many=True, read_only=True)

    class Meta:
        model = ScannerProfile
        fields = ['id', 'name', 'description', 'channel_groups', 'created_at', 'updated_at']
