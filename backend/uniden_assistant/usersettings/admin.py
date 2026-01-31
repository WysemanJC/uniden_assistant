from django.contrib import admin
from .models import ScannerProfile, Frequency, ChannelGroup, Agency, FavoritesList


@admin.register(ScannerProfile)
class ScannerProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'scanner_model', 'firmware_version', 'user_id', 'created_at']
    list_filter = ['scanner_model']
    search_fields = ['name', 'model']


@admin.register(Frequency)
class FrequencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'frequency', 'modulation', 'nac', 'enabled', 'profile']
    list_filter = ['modulation', 'enabled']
    search_fields = ['name', 'nac']


@admin.register(ChannelGroup)
class ChannelGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'profile', 'enabled']
    list_filter = ['enabled']
    search_fields = ['name']


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'agency_id']
    search_fields = ['name', 'agency_id']


@admin.register(FavoritesList)
class FavoritesListAdmin(admin.ModelAdmin):
    list_display = ['name', 'filename', 'scanner_model', 'enabled', 'list_number', 'order']
    list_filter = ['scanner_model', 'enabled']
    search_fields = ['name', 'filename']
