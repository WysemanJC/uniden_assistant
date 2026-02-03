"""
Complete Uniden Scanner Favorites Models
Supports full import/export of f_list.cfg and f_*.hpd files with ALL record types
"""
from django.db import models


SCANNER_MODEL_CHOICES = [
    ('BCDx36HP', 'BCDx36HP'),
    ('BCD536HP', 'BCD536HP'),
    ('BCD436HP', 'BCD436HP'),
    ('SDS100', 'SDS100'),
    ('SDS150', 'SDS150'),
    ('SDS200', 'SDS200'),
]


# ============================================================================
# FAVORITES LIST (f_list.cfg)
# ============================================================================

class FavoritesList(models.Model):
    """F-List record from f_list.cfg
    
    Each instance represents one favorites list entry.
    Links to f_XXXXXX.hpd file containing the actual system/channel data.
    """
    # File metadata
    filename = models.CharField(max_length=255)  # e.g., f_000001.hpd
    scanner_model = models.CharField(max_length=50, choices=SCANNER_MODEL_CHOICES, default='BCDx36HP')
    format_version = models.CharField(max_length=10, default='1.00')
    
    # F-List fields
    user_name = models.CharField(max_length=255)  # UserName from spec (favorites list display name)
    location_control = models.CharField(max_length=10, default='Off')  # On/Off
    monitor = models.CharField(max_length=10, default='Off')  # On/Off
    quick_key = models.CharField(max_length=10, blank=True, default='Off')  # Off or 0-99
    number_tag = models.CharField(max_length=10, blank=True, default='Off')  # Off or 0-99
    
    # Startup configuration (10 keys)
    startup_keys = models.JSONField(default=list)  # StartupKey0-9 (10 On/Off values)
    
    # Startup quick keys (100 keys)
    s_qkeys = models.JSONField(default=list)  # S-Qkey_00 to S-Qkey_99 (100 On/Off values)
    
    # Metadata
    user_id = models.IntegerField(null=True, blank=True, db_index=True)
    order = models.IntegerField(default=0)  # Preserve order from f_list.cfg
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_name} ({self.filename})"

    class Meta:
        ordering = ['order']
        app_label = 'usersettings'
        verbose_name_plural = "Favorites Lists"


# ============================================================================
# CONVENTIONAL SYSTEMS
# ============================================================================

class ConventionalSystem(models.Model):
    """Conventional system definition from f_*.hpd
    
    Format: Conventional\tMyId\tParentId\tNameTag\tAvoid\tReserve\tSystemType\t
            QuickKey\tNumberTag\tSystemHoldTime\tAnalogAGC\tDigitalAGC\t
            DigitalWaitingTime\tDigitalThresholdMode\tDigitalThresholdLevel
    """
    favorites_list = models.ForeignKey(FavoritesList, on_delete=models.CASCADE, related_name='conventional_systems')
    
    # Conventional fields (15 total)
    my_id = models.CharField(max_length=100, blank=True)  # Empty or identifier in favorites
    parent_id = models.CharField(max_length=100, blank=True)  # Empty in favorites per spec
    name_tag = models.CharField(max_length=64)
    avoid = models.CharField(max_length=10, default='Off')  # On/Off
    reserve = models.CharField(max_length=100, blank=True)  # Reserved field (empty)
    system_type = models.CharField(max_length=50)  # System type identifier
    quick_key = models.CharField(max_length=10, default='Off')  # Off or 0-99
    number_tag = models.CharField(max_length=10, default='Off')  # Off or 0-999
    system_hold_time = models.IntegerField(default=0)  # 0-255 seconds
    analog_agc = models.CharField(max_length=10, default='Off')  # Off/On
    digital_agc = models.CharField(max_length=10, default='Off')  # Off/On
    digital_waiting_time = models.IntegerField(default=400)  # 0-1000 milliseconds
    digital_threshold_mode = models.CharField(max_length=20, default='Manual')  # Auto/Manual/Default
    digital_threshold_level = models.IntegerField(default=8)  # 5-13
    
    # DQKs_Status (inline - 100 D-Qkey flags)
    dqks_status = models.JSONField(default=list)  # 100 On/Off values
    
    # Metadata
    order = models.IntegerField(default=0)  # Preserve order in file
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name_tag}"

    class Meta:
        ordering = ['favorites_list', 'order']
        app_label = 'usersettings'


class CGroup(models.Model):
    """C-Group (Conventional Department/Group) from f_*.hpd
    
    Format: C-Group\tMyId\tParentId\tNameTag\tAvoid\tLatitude\tLongitude\t
            Range\tLocationType\tQuickKey\tFilter
    """
    conventional_system = models.ForeignKey(ConventionalSystem, on_delete=models.CASCADE, related_name='cgroups')
    
    # C-Group fields (10 total)
    my_id = models.CharField(max_length=100, blank=True)  # CGroupId=xx or empty
    parent_id = models.CharField(max_length=100, blank=True)  # AgencyId=xx or empty
    name_tag = models.CharField(max_length=64)
    avoid = models.CharField(max_length=10, default='Off')  # On/Off
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    range_miles = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    location_type = models.CharField(max_length=20, default='Circle')  # Circle/Rectangles
    quick_key = models.CharField(max_length=10, default='Off')  # Off or 0-99
    filter = models.CharField(max_length=20, blank=True)  # Global/Normal/Invert/Auto
    
    # Metadata
    order = models.IntegerField(default=0)  # Preserve order in file
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_tag

    class Meta:
        ordering = ['conventional_system', 'order']
        app_label = 'usersettings'
        verbose_name = "Conventional Group"


class CFreq(models.Model):
    """C-Freq (Conventional Frequency/Channel) from f_*.hpd
    
    Format: C-Freq\tMyId\tParentId\tNameTag\tAvoid\tFrequency\tModulation\t
            AudioOption\tFuncTagId\tAttenuator\tDelay\tVolumeOffset\t
            AlertTone\tAlertVolume\tAlertColor\tAlertPattern\tNumberTag\tPriorityChannel
    """
    cgroup = models.ForeignKey(CGroup, on_delete=models.CASCADE, related_name='cfreqs')
    
    # C-Freq fields (18 total)
    my_id = models.CharField(max_length=100, blank=True)  # CFreqId=xx or empty
    parent_id = models.CharField(max_length=100, blank=True)  # CGroupId=xx or empty
    name_tag = models.CharField(max_length=64)
    avoid = models.CharField(max_length=10, default='Off')  # On/Off
    frequency = models.BigIntegerField()  # Hz (1 = 1 Hz)
    modulation = models.CharField(max_length=10)  # AUTO/AM/NFM/FM
    audio_option = models.CharField(max_length=50, blank=True)  # TONE=xxxx, NAC=xxx, ColorCode=xx, RAN=xx, Area=x
    func_tag_id = models.IntegerField()  # 1-37, 208-218 (service type)
    attenuator = models.CharField(max_length=10, default='Off')  # On/Off
    delay = models.IntegerField(default=2)  # 30,10,5,4,3,2,1,0,-5,-10 seconds
    volume_offset = models.IntegerField(default=0)  # -3 to +3 dB
    alert_tone = models.CharField(max_length=10, default='Off')  # Off or 1-9
    alert_volume = models.CharField(max_length=10, default='Auto')  # Auto or 1-15
    alert_color = models.CharField(max_length=20, default='Off')  # Alert light color
    alert_pattern = models.CharField(max_length=20, default='On')  # Alert light pattern
    number_tag = models.CharField(max_length=10, default='Off')  # Off or 0-999
    priority_channel = models.CharField(max_length=10, default='Off')  # Off/On
    
    # Metadata
    order = models.IntegerField(default=0)  # Preserve order in file
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name_tag} - {self.frequency / 1000000:.2f} MHz"

    class Meta:
        ordering = ['cgroup', 'order']
        app_label = 'usersettings'
        verbose_name = "Conventional Frequency"


# ============================================================================
# TRUNK SYSTEMS
# ============================================================================

class TrunkSystem(models.Model):
    """Trunk system definition from f_*.hpd
    
    Format: Trunk\tMyId\tParentId\tNameTag\tAvoid\tReserve\tSystemType\t
            IDSearch\tAlertTone\tAlertVolume\tStatusBit\tNAC\tQuickKey\t
            NumberTag\tSiteHoldTime\tAnalogAGC\tDigitalAGC\tEndCode\t
            PriorityIDScan\tAlertColor\tAlertPattern\tTGIDFormat
    """
    favorites_list = models.ForeignKey(FavoritesList, on_delete=models.CASCADE, related_name='trunk_systems')
    
    # Trunk fields (21 total)
    my_id = models.CharField(max_length=100, blank=True)  # TrunkId=xx or empty
    parent_id = models.CharField(max_length=100, blank=True)  # StateId=xx or empty
    name_tag = models.CharField(max_length=64)
    avoid = models.CharField(max_length=10, default='Off')  # On/Off
    reserve = models.CharField(max_length=100, blank=True)  # Reserved field (empty)
    system_type = models.CharField(max_length=50)  # P25Standard, Motorola, Edacs, MotoTrbo, Nxdn, etc.
    id_search = models.CharField(max_length=10, default='Off')  # Off/On
    alert_tone = models.CharField(max_length=10, default='Off')  # Off or 1-9
    alert_volume = models.CharField(max_length=10, default='Auto')  # Auto or 1-15
    status_bit = models.CharField(max_length=10, default='Ignore')  # Yes/Ignore
    nac = models.CharField(max_length=10, default='Srch')  # Srch or 0-FFF hex
    quick_key = models.CharField(max_length=10, default='Off')  # Off or 0-99
    number_tag = models.CharField(max_length=10, default='Off')  # Off or 0-999
    site_hold_time = models.IntegerField(default=0)  # 0-255 seconds
    analog_agc = models.CharField(max_length=10, default='Off')  # Off/On
    digital_agc = models.CharField(max_length=10, default='Off')  # Off/On
    end_code = models.CharField(max_length=20, default='Analog')  # Analog/Analog+Digital/Ignore
    priority_id_scan = models.CharField(max_length=10, default='Off')  # Off/On
    alert_color = models.CharField(max_length=20, default='Off')  # Alert light color
    alert_pattern = models.CharField(max_length=20, default='On')  # Alert light pattern
    tgid_format = models.CharField(max_length=20, blank=True)  # NEXEDGE/IDAS
    
    # DQKs_Status (inline - 100 D-Qkey flags)
    dqks_status = models.JSONField(default=list)  # 100 On/Off values
    
    # Metadata
    order = models.IntegerField(default=0)  # Preserve order in file
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name_tag}"

    class Meta:
        ordering = ['favorites_list', 'order']
        app_label = 'usersettings'


class Site(models.Model):
    """Site (Trunk system site/tower) from f_*.hpd
    
    Format: Site\tMyId\tParentId\tNameTag\tAvoid\tLatitude\tLongitude\tRange\t
            Modulation\tMotBandType\tEdacsBandType\tLocationType\tAttenuator\t
            DigitalWaitingTime\tDigitalThresholdMode\tDigitalThresholdLevel\t
            QuickKey\tNAC\tFilter
    """
    trunk_system = models.ForeignKey(TrunkSystem, on_delete=models.CASCADE, related_name='sites')
    
    # Site fields (19 total)
    my_id = models.CharField(max_length=100, blank=True)  # SiteId=xx or empty
    parent_id = models.CharField(max_length=100, blank=True)  # TrunkId=xx or empty
    name_tag = models.CharField(max_length=64)
    avoid = models.CharField(max_length=10, default='Off')  # On/Off
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    range_miles = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    modulation = models.CharField(max_length=10, default='AUTO')  # AUTO/NFM/FM
    mot_band_type = models.CharField(max_length=20, default='Standard')  # Standard/Sprinter/Custom
    edacs_band_type = models.CharField(max_length=20, default='Wide')  # Wide/Narrow
    location_type = models.CharField(max_length=20, default='Circle')  # Circle/Rectangles
    attenuator = models.CharField(max_length=10, default='Off')  # On/Off
    digital_waiting_time = models.IntegerField(default=400)  # 0-1000 milliseconds
    digital_threshold_mode = models.CharField(max_length=20, default='Manual')  # Auto/Manual/Default
    digital_threshold_level = models.IntegerField(default=8)  # 5-13
    quick_key = models.CharField(max_length=10, default='Off')  # Off or 0-99
    nac = models.CharField(max_length=10, default='Srch')  # Srch or 0-FFF hex
    filter = models.CharField(max_length=20, blank=True)  # Global/Normal/Invert/Auto
    
    # Metadata
    order = models.IntegerField(default=0)  # Preserve order in file
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_tag

    class Meta:
        ordering = ['trunk_system', 'order']
        app_label = 'usersettings'


class BandPlanP25(models.Model):
    """BandPlan_P25 from f_*.hpd (follows Site record)
    
    Format: BandPlan_P25\tMyId\tBase0\tSpacing0\tBase1\tSpacing1\t...\tBaseF\tSpacingF
    """
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name='bandplan_p25')
    
    # Band Plan fields (32 total: 16 bands × 2 params)
    # Stored as JSON for flexibility: {0: {base: xxx, spacing: xxx}, ...}
    band_plan = models.JSONField(default=dict)  # Keys 0-F, values {base: Hz, spacing: Hz}
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"P25 Band Plan for {self.site.name_tag}"

    class Meta:
        app_label = 'usersettings'
        verbose_name = "P25 Band Plan"


class BandPlanMot(models.Model):
    """BandPlan_Mot (Motorola Custom Band Plan) from f_*.hpd
    
    Format: BandPlan_Mot\tMyId\tLower0\tUpper0\tSpacing0\tOffset0\t...\tLower5\tUpper5\tSpacing5\tOffset5
    """
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name='bandplan_mot')
    
    # Band Plan fields (24 total: 6 bands × 4 params)
    # Stored as JSON: {0: {lower: Hz, upper: Hz, spacing: Hz, offset: int}, ...}
    band_plan = models.JSONField(default=dict)  # Keys 0-5
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Motorola Band Plan for {self.site.name_tag}"

    class Meta:
        app_label = 'usersettings'
        verbose_name = "Motorola Band Plan"


class TFreq(models.Model):
    """T-Freq (Trunk Frequency) from f_*.hpd
    
    Format: T-Freq\tReserve(MyId)\tParentId\tReserve\tReserve(Avoid)\tFrequency\tLCN\tColorCode/RAN/Area
    """
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='tfreqs')
    
    # T-Freq fields (7 total)
    reserve_my_id = models.CharField(max_length=100, blank=True)  # Always TFreqId=0 or empty
    parent_id = models.CharField(max_length=100, blank=True)  # SiteId=xx or empty
    reserve1 = models.CharField(max_length=100, blank=True)  # Reserved (empty)
    reserve_avoid = models.CharField(max_length=10, default='Off')  # Always Off
    frequency = models.BigIntegerField()  # Hz (1 = 1 Hz)
    lcn = models.IntegerField(default=0)  # 0-4094 depending on system
    color_code_ran_area = models.CharField(max_length=50, blank=True)  # ColorCode=0-15, RAN=0-63, Area=0-1, Srch
    
    # Metadata
    order = models.IntegerField(default=0)  # Preserve order in file
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.frequency / 1000000:.2f} MHz (LCN {self.lcn})"

    class Meta:
        ordering = ['site', 'order']
        app_label = 'usersettings'
        verbose_name = "Trunk Frequency"


class TGroup(models.Model):
    """T-Group (Trunked Talk Group) from f_*.hpd
    
    Format: T-Group\tMyId\tParentId\tNameTag\tAvoid\tLatitude\tLongitude\t
            Range\tLocationType\tQuickKey
    """
    trunk_system = models.ForeignKey(TrunkSystem, on_delete=models.CASCADE, related_name='tgroups')
    
    # T-Group fields (9 total)
    my_id = models.CharField(max_length=100, blank=True)  # TGroupId=xx or empty
    parent_id = models.CharField(max_length=100, blank=True)  # TrunkId=xx or empty
    name_tag = models.CharField(max_length=64)
    avoid = models.CharField(max_length=10, default='Off')  # On/Off
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    range_miles = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    location_type = models.CharField(max_length=20, default='Circle')  # Circle/Rectangles
    quick_key = models.CharField(max_length=10, default='Off')  # Off or 0-99
    
    # Metadata
    order = models.IntegerField(default=0)  # Preserve order in file (T-Groups come AFTER Sites)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_tag

    class Meta:
        ordering = ['trunk_system', 'order']
        app_label = 'usersettings'
        verbose_name = "Trunk Group"


class TGID(models.Model):
    """TGID (Talkgroup ID) from f_*.hpd
    
    Format: TGID\tMyId\tParentId\tNameTag\tAvoid\tTGID\tAudioType\tFuncTagId\t
            Delay\tVolumeOffset\tAlertTone\tAlertVolume\tAlertColor\t
            AlertPattern\tNumberTag\tPriorityChannel\tTDMASlot
    """
    tgroup = models.ForeignKey(TGroup, on_delete=models.CASCADE, related_name='tgids')
    
    # TGID fields (17 total)
    my_id = models.CharField(max_length=100, blank=True)  # Tid=xx or empty
    parent_id = models.CharField(max_length=100, blank=True)  # TGroupId=xx or empty
    name_tag = models.CharField(max_length=64)
    avoid = models.CharField(max_length=10, default='Off')  # On/Off
    tgid = models.CharField(max_length=50)  # TGID formatted string per spec
    audio_type = models.CharField(max_length=20, default='ALL')  # ALL/ANALOG/DIGITAL
    func_tag_id = models.IntegerField()  # 1-37, 208-218 (service type)
    delay = models.IntegerField(default=2)  # 30,10,5,4,3,2,1,0,-5,-10 seconds
    volume_offset = models.IntegerField(default=0)  # -3 to +3 dB
    alert_tone = models.CharField(max_length=10, default='Off')  # Off or 1-9
    alert_volume = models.CharField(max_length=10, default='Auto')  # Auto or 1-15
    alert_color = models.CharField(max_length=20, default='Off')  # Alert light color
    alert_pattern = models.CharField(max_length=20, default='On')  # Alert light pattern
    number_tag = models.CharField(max_length=10, default='Off')  # Off or 0-999
    priority_channel = models.CharField(max_length=10, default='Off')  # Off/On
    tdma_slot = models.CharField(max_length=10, default='Any')  # 1/2/Any
    
    # Metadata
    order = models.IntegerField(default=0)  # Preserve order in file
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name_tag} (TGID {self.tgid})"

    class Meta:
        ordering = ['tgroup', 'order']
        app_label = 'usersettings'
        verbose_name = "Talkgroup ID"


# ============================================================================
# GEOGRAPHIC BOUNDARIES
# ============================================================================

class Rectangle(models.Model):
    """Rectangle (Geographic boundary) from f_*.hpd
    
    Format: Rectangle\tMyId\tLatitude1\tLongitude1\tLatitude2\tLongitude2
    
    Can be associated with Site, TGroup, or CGroup
    """
    # Polymorphic FK - only ONE of these should be set
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='rectangles', null=True, blank=True)
    tgroup = models.ForeignKey(TGroup, on_delete=models.CASCADE, related_name='rectangles', null=True, blank=True)
    cgroup = models.ForeignKey(CGroup, on_delete=models.CASCADE, related_name='rectangles', null=True, blank=True)
    
    # Rectangle fields (5 total)
    my_id = models.CharField(max_length=100, blank=True)  # SiteId=xx, TGroupId=xx, or CGroupId=xx
    latitude1 = models.DecimalField(max_digits=10, decimal_places=6)
    longitude1 = models.DecimalField(max_digits=10, decimal_places=6)
    latitude2 = models.DecimalField(max_digits=10, decimal_places=6)
    longitude2 = models.DecimalField(max_digits=10, decimal_places=6)
    
    # Metadata
    order = models.IntegerField(default=0)  # Preserve order in file
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        parent = self.site or self.tgroup or self.cgroup
        return f"Rectangle for {parent}"

    class Meta:
        ordering = ['order']
        app_label = 'usersettings'


# ============================================================================
# LEGACY MODELS (Keep for backward compatibility with existing code)
# ============================================================================

class ScannerProfile(models.Model):
    """Scanner configuration profile (legacy)"""
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=50)
    scanner_model = models.CharField(max_length=50, choices=SCANNER_MODEL_CHOICES, default='BCDx36HP')
    firmware_version = models.CharField(max_length=20, blank=True)
    user_id = models.IntegerField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data_file = models.FileField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_at']
        app_label = 'usersettings'


class ChannelGroup(models.Model):
    """Legacy channel group model - kept for backward compatibility"""
    cgroup_id = models.BigIntegerField(null=True, blank=True)
    profile = models.ForeignKey(ScannerProfile, on_delete=models.CASCADE, related_name='channel_groups', null=True, blank=True)
    favorites_list = models.ForeignKey(FavoritesList, on_delete=models.CASCADE, related_name='channel_groups', null=True, blank=True)
    name_tag = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    range_miles = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    location_type = models.CharField(max_length=50, blank=True)
    emergency_alert = models.CharField(max_length=10, blank=True, default='Off')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_tag

    class Meta:
        ordering = ['name_tag']
        app_label = 'usersettings'


class Frequency(models.Model):
    """Legacy frequency model - kept for backward compatibility"""
    MODULATION_CHOICES = [
        ('FM', 'FM'),
        ('NFM', 'NFM'),
        ('AM', 'AM'),
        ('AUTO', 'AUTO'),
    ]

    channel_group = models.ForeignKey(ChannelGroup, on_delete=models.CASCADE, related_name='frequencies')
    profile = models.ForeignKey(ScannerProfile, on_delete=models.CASCADE, related_name='frequencies_alt', null=True, blank=True)
    name_tag = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    enabled = models.BooleanField(default=True)
    frequency = models.BigIntegerField()
    modulation = models.CharField(max_length=20, choices=MODULATION_CHOICES)
    audio_option = models.CharField(max_length=50, blank=True)
    delay = models.IntegerField(default=15)
    attenuator = models.CharField(max_length=10, blank=True, default='Off')
    number_tag = models.IntegerField(null=True, blank=True)
    priority = models.IntegerField(default=0, blank=True)
    alert_tone = models.CharField(max_length=10, blank=True, default='Off')
    alert_light = models.CharField(max_length=10, blank=True, default='Off')
    volume_offset = models.CharField(max_length=10, blank=True, default='Off')
    p_ch = models.CharField(max_length=10, blank=True, default='Off')
    reserved = models.CharField(max_length=10, blank=True, default='Off')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name_tag or self.description} - {self.frequency / 1000000:.2f} MHz"

    class Meta:
        ordering = ['frequency']
        app_label = 'usersettings'


class Agency(models.Model):
    """Agency (legacy - unused)"""
    name = models.CharField(max_length=255)
    agency_id = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Agencies"
        ordering = ['name']
        app_label = 'usersettings'


# ============================================================================
# RAW FILE STORAGE
# ============================================================================

class ScannerFileRecord(models.Model):
    """Structured record storage for scanner files"""
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    record_type = models.CharField(max_length=100)
    fields = models.JSONField(default=list)
    spec_field_order = models.JSONField(default=list)
    spec_field_map = models.JSONField(default=dict)
    trailing_empty_fields = models.IntegerField(default=0)
    line_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['file_path', 'line_number']
        app_label = 'usersettings'
        indexes = [
            models.Index(fields=['file_path', 'line_number']),
            models.Index(fields=['record_type']),
        ]


class ScannerRawFile(models.Model):
    """Raw scanner file data for reconstruction and archiving"""
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500, blank=True)
    file_type = models.CharField(max_length=50)
    file_size = models.IntegerField()
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ['-upload_time']
        app_label = 'usersettings'


class ScannerRawLine(models.Model):
    """Individual raw lines from scanner files"""
    raw_file = models.ForeignKey(ScannerRawFile, on_delete=models.CASCADE, related_name='lines')
    line_number = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['raw_file', 'line_number']
        app_label = 'usersettings'
        indexes = [
            models.Index(fields=['raw_file', 'line_number']),
        ]
