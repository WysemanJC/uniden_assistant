from rest_framework import serializers
from .models import (
    Country, State, County, HPDBAgency, HPDBChannelGroup, HPDBFrequency, HPDBRectangle
)


class CountrySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='country_id', read_only=True)
    
    class Meta:
        model = Country
        fields = ['id', 'name_tag', 'code']


class StateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='state_id', read_only=True)
    country_id = serializers.IntegerField(source='country.country_id', read_only=True)
    country_name_tag = serializers.CharField(source='country.name_tag', read_only=True)
    
    class Meta:
        model = State
        fields = ['id', 'name_tag', 'short_name', 'country_id', 'country_name_tag']


class CountySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='county_id', read_only=True)
    state_id = serializers.IntegerField(source='state.state_id', read_only=True)
    state_name_tag = serializers.CharField(source='state.name_tag', read_only=True)
    state_short_name = serializers.CharField(source='state.short_name', read_only=True)
    
    class Meta:
        model = County
        fields = ['id', 'name_tag', 'state_id', 'state_name_tag', 'state_short_name']


class HPDBFrequencySerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='cfreq_id', read_only=True)
    cgroup_id = serializers.CharField(source='cgroup.cgroup_id', read_only=True)
    
    class Meta:
        model = HPDBFrequency
        fields = ['id', 'name_tag', 'description', 'enabled', 'frequency', 'modulation', 'audio_option', 'delay', 'cgroup_id']


class HPDBRectangleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HPDBRectangle
        fields = ['id', 'latitude_1', 'longitude_1', 'latitude_2', 'longitude_2', 'min_latitude', 'max_latitude', 'min_longitude', 'max_longitude']
        read_only_fields = ['id', 'min_latitude', 'max_latitude', 'min_longitude', 'max_longitude']


class HPDBChannelGroupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='cgroup_id', read_only=True)
    agency_id = serializers.IntegerField(source='agency.agency_id', read_only=True)
    frequencies = HPDBFrequencySerializer(many=True, read_only=True)
    frequency_count = serializers.IntegerField(source='frequencies.count', read_only=True)
    rectangles = HPDBRectangleSerializer(many=True, read_only=True)
    
    class Meta:
        model = HPDBChannelGroup
        fields = ['id', 'name_tag', 'enabled', 'latitude', 'longitude', 'range_miles', 'location_type', 'agency_id', 'frequencies', 'frequency_count', 'rectangles']


class HPDBAgencySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='agency_id', read_only=True)
    channel_groups = HPDBChannelGroupSerializer(many=True, read_only=True)
    group_count = serializers.IntegerField(source='channel_groups.count', read_only=True)
    
    class Meta:
        model = HPDBAgency
        fields = [
            'id', 'name_tag', 'system_type', 'enabled', 'channel_groups', 'group_count',
            'quick_key', 'emergency_alert', 'number_tag', 'hold_time', 'priority_id_scan',
            'agc_analog', 'agc_digital', 'trunk_id_search', 'trunk_end_code', 
            'trunk_emergency_alert_light', 'trunk_status_bit', 'trunk_nxdn_format'
        ]


class HPDBTreeSerializer(serializers.Serializer):
    """Serializer for hierarchical tree view of HPDB data"""
    id = serializers.CharField()  # spec ID in format "country-123", "state-45", etc.
    type = serializers.CharField()
    name_tag = serializers.CharField()
    code = serializers.CharField(required=False)
    children = serializers.ListField(required=False)
