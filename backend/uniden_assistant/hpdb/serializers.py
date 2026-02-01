from rest_framework import serializers
from .models import (
    Country, State, County, HPDBAgency, HPDBChannelGroup, HPDBFrequency
)


class ObjectIdField(serializers.Field):
    """Custom field to handle MongoDB ObjectId"""
    def to_representation(self, value):
        return str(value)
    
    def to_internal_value(self, data):
        return data


class CountrySerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    
    class Meta:
        model = Country
        fields = ['id', 'country_id', 'name', 'code']


class StateSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    country_name = serializers.CharField(source='country.name', read_only=True)
    
    class Meta:
        model = State
        fields = ['id', 'state_id', 'name', 'code', 'country', 'country_name']


class CountySerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    state_code = serializers.CharField(source='state.code', read_only=True)
    
    class Meta:
        model = County
        fields = ['id', 'county_id', 'name', 'state', 'state_name', 'state_code']


class HPDBFrequencySerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    
    class Meta:
        model = HPDBFrequency
        fields = ['id', 'cfreq_id', 'name', 'description', 'enabled', 'frequency', 'modulation', 'tone', 'delay']


class HPDBChannelGroupSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    frequencies = HPDBFrequencySerializer(many=True, read_only=True)
    frequency_count = serializers.IntegerField(source='frequencies.count', read_only=True)
    
    class Meta:
        model = HPDBChannelGroup
        fields = ['id', 'cgroup_id', 'name', 'enabled', 'latitude', 'longitude', 'range_miles', 'location_type', 'frequencies', 'frequency_count']


class HPDBAgencySerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    states = StateSerializer(many=True, read_only=True)
    counties = CountySerializer(many=True, read_only=True)
    channel_groups = HPDBChannelGroupSerializer(many=True, read_only=True)
    group_count = serializers.IntegerField(source='channel_groups.count', read_only=True)
    
    class Meta:
        model = HPDBAgency
        fields = ['id', 'agency_id', 'name', 'system_type', 'enabled', 'states', 'counties', 'channel_groups', 'group_count']


class HPDBTreeSerializer(serializers.Serializer):
    """Serializer for hierarchical tree view of HPDB data"""
    id = serializers.CharField()  # Changed from IntegerField to CharField for ObjectId compatibility
    type = serializers.CharField()
    name = serializers.CharField()
    code = serializers.CharField(required=False)
    children = serializers.ListField(required=False)
