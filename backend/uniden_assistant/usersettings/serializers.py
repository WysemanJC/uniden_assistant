from rest_framework import serializers
from .models import (
    ScannerProfile, Frequency, ChannelGroup, Agency, FavoritesList
)


class ObjectIdField(serializers.Field):
    """Custom field to handle MongoDB ObjectId"""
    def to_representation(self, value):
        return str(value)
    
    def to_internal_value(self, data):
        return data


class FrequencySerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    
    class Meta:
        model = Frequency
        fields = ['id', 'name', 'frequency', 'modulation', 'nac', 'enabled', 'priority', 'created_at', 'updated_at']


class ChannelGroupSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    frequencies = FrequencySerializer(many=True, read_only=True)
    frequency_ids = serializers.PrimaryKeyRelatedField(
        queryset=Frequency.objects.all(),
        source='frequencies',
        many=True,
        write_only=True
    )

    class Meta:
        model = ChannelGroup
        fields = ['id', 'name', 'description', 'enabled', 'frequencies', 'frequency_ids', 'created_at', 'updated_at']


class AgencySerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    
    class Meta:
        model = Agency
        fields = ['id', 'name', 'agency_id', 'description']


class ScannerProfileSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    frequencies = FrequencySerializer(many=True, read_only=True)
    channel_groups = ChannelGroupSerializer(many=True, read_only=True)

    class Meta:
        model = ScannerProfile
        fields = ['id', 'name', 'model', 'scanner_model', 'firmware_version', 'user_id', 'data_file', 'frequencies', 'channel_groups', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class FavoritesListSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    flags = serializers.SerializerMethodField()
    
    def get_flags(self, obj):
        import json
        try:
            return json.loads(obj.flags) if obj.flags else []
        except:
            return []
    
    class Meta:
        model = FavoritesList
        fields = ['id', 'name', 'filename', 'scanner_model', 'user_id', 'enabled', 'disabled_on_power', 'quick_key', 'list_number', 'order', 'flags', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
