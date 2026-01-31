from django.contrib import admin
from .models import ScannerProfile, ChannelGroup, Frequency, Agency


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(ScannerProfile)
class ScannerProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-updated_at',)


@admin.register(ChannelGroup)
class ChannelGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile', 'created_at')
    list_filter = ('profile',)
    search_fields = ('name',)


@admin.register(Frequency)
class FrequencyAdmin(admin.ModelAdmin):
    list_display = ('frequency', 'name', 'agency', 'modulation', 'enabled', 'channel_group')
    list_filter = ('modulation', 'enabled', 'agency', 'channel_group')
    search_fields = ('name', 'frequency')
    ordering = ('frequency',)
