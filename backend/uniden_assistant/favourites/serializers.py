from rest_framework import serializers
from .models import (
    ScannerProfile, Frequency, ChannelGroup, Agency, FavoritesList,
    ConventionalSystem, TrunkSystem, CGroup, CFreq, Site, BandPlanP25, BandPlanMot,
    TFreq, TGroup, TGID, Rectangle, FleetMap, UnitId, AvoidTgid
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
        fields = ['id', 'name_tag', 'description', 'frequency', 'modulation', 'audio_option', 'enabled', 'priority', 'delay', 'alert_tone', 'alert_light', 'attenuator', 'volume_offset', 'p_ch', 'number_tag', 'reserved', 'created_at', 'updated_at']


class ChannelGroupSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    frequencies = FrequencySerializer(many=True, read_only=True)

    class Meta:
        model = ChannelGroup
        fields = ['id', 'name_tag', 'enabled', 'location_type', 'latitude', 'longitude', 'range_miles', 'emergency_alert', 'frequencies', 'created_at', 'updated_at']


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
        fields = ['id', 'name', 'model', 'firmware_version', 'user_id', 'data_file', 'frequencies', 'channel_groups', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


# ============================================================================
# FAVORITES HIERARCHICAL SERIALIZERS
# ============================================================================

class CFreqSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    
    class Meta:
        model = CFreq
        fields = ['id', 'name_tag', 'avoid', 'frequency', 'modulation', 'audio_option', 'func_tag_id',
                  'attenuator', 'delay', 'volume_offset', 'alert_tone', 'alert_volume',
                  'alert_color', 'alert_pattern', 'number_tag', 'priority_channel', 'order']


class RectangleSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    
    class Meta:
        model = Rectangle
        fields = ['id', 'latitude_nw', 'longitude_nw', 'latitude_se', 'longitude_se', 'order']


class CGroupSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    cfreqs = CFreqSerializer(many=True, read_only=True)
    rectangles = RectangleSerializer(many=True, read_only=True)
    
    class Meta:
        model = CGroup
        fields = ['id', 'name_tag', 'avoid', 'latitude', 'longitude', 'range_miles',
                  'location_type', 'quick_key', 'filter', 'cfreqs', 'rectangles', 'order']


class CGroupWriteSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)

    class Meta:
        model = CGroup
        fields = ['id', 'name_tag', 'avoid', 'latitude', 'longitude', 'range_miles',
                  'location_type', 'quick_key', 'filter']


class ConventionalSystemSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    cgroups = CGroupSerializer(many=True, read_only=True)
    
    class Meta:
        model = ConventionalSystem
        fields = ['id', 'name_tag', 'system_type', 'avoid', 'quick_key', 'number_tag',
                  'system_hold_time', 'analog_agc', 'digital_agc', 'digital_waiting_time',
                  'digital_threshold_mode', 'digital_threshold_level', 'dqks_status', 'cgroups', 'order']


class ConventionalSystemWriteSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)

    class Meta:
        model = ConventionalSystem
        fields = [
            'id', 'name_tag', 'system_type', 'avoid', 'quick_key', 'number_tag',
            'system_hold_time', 'analog_agc', 'digital_agc', 'digital_waiting_time',
            'digital_threshold_mode', 'digital_threshold_level'
        ]


# Trunk System Serializers
class BandPlanP25Serializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    
    class Meta:
        model = BandPlanP25
        fields = ['id', 'band_index', 'base_frequency', 'bandwidth', 'order']


class BandPlanMotSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    
    class Meta:
        model = BandPlanMot
        fields = ['id', 'band_index', 'base_frequency', 'bandwidth', 'offset', 'spacing', 'order']


class TFreqSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    
    class Meta:
        model = TFreq
        fields = ['id', 'frequency', 'lcn', 'color_code', 'order']


class TGIDSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    
    class Meta:
        model = TGID
        fields = ['id', 'name_tag', 'avoid', 'tgid', 'audio_type', 'func_tag_id', 'delay', 
                  'volume_offset', 'alert_tone', 'alert_volume', 'alert_color',
                  'alert_pattern', 'priority_channel', 'number_tag', 'tdma_slot', 'order']


class TGroupSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    tgids = TGIDSerializer(many=True, read_only=True)
    rectangles = RectangleSerializer(many=True, read_only=True)
    
    class Meta:
        model = TGroup
        fields = ['id', 'name_tag', 'avoid', 'latitude', 'longitude', 'range_miles',
                  'location_type', 'quick_key', 'filter', 'tgids', 'rectangles', 'order']


class TGroupWriteSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)

    class Meta:
        model = TGroup
        fields = ['id', 'name_tag', 'avoid', 'latitude', 'longitude', 'range_miles',
                  'location_type', 'quick_key', 'filter']


class SiteSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    band_plans_p25 = BandPlanP25Serializer(many=True, read_only=True)
    band_plans_mot = BandPlanMotSerializer(many=True, read_only=True)
    tfreqs = TFreqSerializer(many=True, read_only=True)
    rectangles = RectangleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Site
        fields = ['id', 'name_tag', 'avoid', 'latitude', 'longitude', 'range_miles',
                  'modulation', 'mot_band_type', 'edacs_band_type', 'location_type',
                  'attenuator', 'digital_waiting_time', 'digital_threshold_mode',
                  'digital_threshold_level', 'quick_key', 'nac', 'filter',
                  'band_plans_p25', 'band_plans_mot', 'tfreqs', 'rectangles', 'order']


class FleetMapSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    
    class Meta:
        model = FleetMap
        fields = ['id', 'name_tag', 'fleet_map_id', 'alert_tone', 'alert_volume',
                  'alert_color', 'alert_pattern', 'order']


class UnitIdSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    
    class Meta:
        model = UnitId
        fields = ['id', 'name_tag', 'unit_id', 'alert_tone', 'alert_volume',
                  'alert_color', 'alert_pattern', 'order']


class AvoidTgidSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    
    class Meta:
        model = AvoidTgid
        fields = ['id', 'tgid', 'order']


class TrunkSystemSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    fleet_maps = FleetMapSerializer(many=True, read_only=True)
    unit_ids = UnitIdSerializer(many=True, read_only=True)
    avoid_tgids = AvoidTgidSerializer(many=True, read_only=True)
    sites = SiteSerializer(many=True, read_only=True)
    tgroups = TGroupSerializer(many=True, read_only=True)
    
    class Meta:
        model = TrunkSystem
        fields = [
            'id', 'name_tag', 'system_type', 'avoid', 'quick_key', 'number_tag',
            'id_search', 'alert_tone', 'alert_volume', 'status_bit', 'nac',
            'site_hold_time', 'analog_agc', 'digital_agc', 'end_code',
            'priority_id_scan', 'alert_color', 'alert_pattern', 'tgid_format',
            'dqks_status', 'fleet_maps', 'unit_ids', 'avoid_tgids', 'sites', 'tgroups', 'order'
        ]


class TrunkSystemWriteSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)

    class Meta:
        model = TrunkSystem
        fields = [
            'id', 'name_tag', 'system_type', 'avoid', 'quick_key', 'number_tag',
            'id_search', 'alert_tone', 'alert_volume', 'status_bit', 'nac',
            'site_hold_time', 'analog_agc', 'digital_agc', 'end_code',
            'priority_id_scan', 'alert_color', 'alert_pattern', 'tgid_format'
        ]


class FavoritesListDetailSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    conventional_systems = ConventionalSystemSerializer(many=True, read_only=True)
    trunk_systems = TrunkSystemSerializer(many=True, read_only=True)
    
    class Meta:
        model = FavoritesList
        fields = ['id', 'user_name', 'filename', 'scanner_model', 'format_version',
                  'conventional_systems', 'trunk_systems', 'location_control', 'monitor',
                  'quick_key', 'number_tag', 'startup_keys', 's_qkeys', 'order',
                  'user_id', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class FavoritesListSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    
    class Meta:
        model = FavoritesList
        fields = ['id', 'user_name', 'filename', 'scanner_model', 'format_version', 'location_control', 'monitor', 'quick_key', 'number_tag', 
              'user_id', 'order', 'startup_keys', 's_qkeys', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
