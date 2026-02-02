from django.contrib import admin
from .models import ScannerProfile, Frequency, ChannelGroup, Agency, FavoritesList


@admin.register(ScannerProfile)
class ScannerProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'scanner_model', 'firmware_version', 'user_id', 'created_at']
    list_filter = ['scanner_model']
    search_fields = ['name', 'model']


@admin.register(Frequency)
class FrequencyAdmin(admin.ModelAdmin):
    list_display = ['name_tag', 'frequency', 'modulation', 'audio_option', 'enabled', 'profile']
    list_filter = ['modulation', 'enabled']
    search_fields = ['name_tag', 'audio_option']


@admin.register(ChannelGroup)
class ChannelGroupAdmin(admin.ModelAdmin):
    list_display = ['name_tag', 'profile', 'enabled']
    list_filter = ['enabled']
    search_fields = ['name_tag']


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'agency_id']
    search_fields = ['name', 'agency_id']


@admin.register(FavoritesList)
class FavoritesListAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'filename', 'location_control', 'monitor', 'number_tag', 'order']
    list_filter = ['location_control', 'monitor']
    search_fields = ['user_name', 'filename']
