from django.contrib import admin
from .models import Country, State, County, HPDBAgency, HPDBChannelGroup, HPDBFrequency


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name_tag', 'code', 'country_id']
    search_fields = ['name_tag', 'code']


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name_tag', 'short_name', 'country', 'state_id']
    list_filter = ['country']
    search_fields = ['name_tag', 'short_name']


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ['name_tag', 'state', 'county_id']
    list_filter = ['state']
    search_fields = ['name_tag']


@admin.register(HPDBAgency)
class HPDBAgencyAdmin(admin.ModelAdmin):
    list_display = ['name_tag', 'system_type', 'enabled', 'agency_id']
    list_filter = ['system_type', 'enabled']
    search_fields = ['name_tag', 'agency_id']
    filter_horizontal = ['states', 'counties']


@admin.register(HPDBChannelGroup)
class HPDBChannelGroupAdmin(admin.ModelAdmin):
    list_display = ['name_tag', 'agency', 'enabled', 'cgroup_id']
    list_filter = ['enabled', 'agency']
    search_fields = ['name_tag']


@admin.register(HPDBFrequency)
class HPDBFrequencyAdmin(admin.ModelAdmin):
    list_display = ['name_tag', 'frequency', 'modulation', 'enabled', 'cfreq_id']
    list_filter = ['modulation', 'enabled']
    search_fields = ['name_tag']
