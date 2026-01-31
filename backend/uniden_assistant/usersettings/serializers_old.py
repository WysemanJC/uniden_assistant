from rest_framework import serializers
from .models import (
    ScannerProfile, Frequency, ChannelGroup, Agency,
    Country, State, County, HPDBAgency, HPDBChannelGroup, HPDBFrequency,
    FavoritesList
)


class FrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Frequency
        fields = ['id', 'name', 'frequency', 'modulation', 'nac', 'enabled', 'priority', 'created_at', 'updated_at']


class ChannelGroupSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Agency
        fields = ['id', 'name', 'agency_id', 'description']


class ScannerProfileSerializer(serializers.ModelSerializer):
    frequencies = FrequencySerializer(many=True, read_only=True)
    channel_groups = ChannelGroupSerializer(many=True, read_only=True)

    class Meta:
        model = ScannerProfile
        fields = ['id', 'name', 'model', 'scanner_model', 'firmware_version', 'user_id', 'data_file', 'frequencies', 'channel_groups', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


# HPDB Serializers
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_id', 'name', 'code']


class StateSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)
    
    class Meta:
        model = State
        fields = ['id', 'state_id', 'name', 'code', 'country', 'country_name']


class CountySerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    state_code = serializers.CharField(source='state.code', read_only=True)
    
    class Meta:
        model = County
        fields = ['id', 'county_id', 'name', 'state', 'state_name', 'state_code']


class HPDBFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = HPDBFrequency
        fields = ['id', 'cfreq_id', 'name', 'enabled', 'frequency', 'modulation', 'tone', 'delay']


class HPDBChannelGroupSerializer(serializers.ModelSerializer):
    frequencies = HPDBFrequencySerializer(many=True, read_only=True)
    frequency_count = serializers.IntegerField(source='frequencies.count', read_only=True)
    
    class Meta:
        model = HPDBChannelGroup
        fields = ['id', 'cgroup_id', 'name', 'enabled', 'latitude', 'longitude', 'range_miles', 'location_type', 'frequencies', 'frequency_count']


class HPDBAgencySerializer(serializers.ModelSerializer):
    states = StateSerializer(many=True, read_only=True)
    counties = CountySerializer(many=True, read_only=True)
    channel_groups = HPDBChannelGroupSerializer(many=True, read_only=True)
    group_count = serializers.IntegerField(source='channel_groups.count', read_only=True)
    
    class Meta:
        model = HPDBAgency
        fields = ['id', 'agency_id', 'name', 'system_type', 'enabled', 'states', 'counties', 'channel_groups', 'group_count']


class HPDBTreeSerializer(serializers.Serializer):
    """Serializer for hierarchical tree view of HPDB data"""
    id = serializers.IntegerField()
    type = serializers.CharField()
    name = serializers.CharField()
    code = serializers.CharField(required=False)
    children = serializers.ListField(required=False)


class FavoritesListSerializer(serializers.ModelSerializer):
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
