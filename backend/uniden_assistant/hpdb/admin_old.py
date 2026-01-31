from django.contrib import admin
from .models import ScannerProfile, Frequency, ChannelGroup, Agency


@admin.register(ScannerProfile)
class ScannerProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'firmware_version', 'created_at']
    search_fields = ['name', 'model']


@admin.register(Frequency)
class FrequencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'frequency', 'modulation', 'nac', 'enabled']
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
