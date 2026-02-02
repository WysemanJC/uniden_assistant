from django.db import models


SCANNER_MODEL_CHOICES = [
    ('BCDx36HP', 'BCDx36HP'),
    ('BCD536HP', 'BCD536HP'),
    ('BCD436HP', 'BCD436HP'),
    ('SDS100', 'SDS100'),
    ('SDS150', 'SDS150'),
    ('SDS200', 'SDS200'),
]


class ScannerProfile(models.Model):
    """Scanner configuration profile"""
    name = models.CharField(max_length=255)
    # Legacy free-form model label
    model = models.CharField(max_length=50)
    # Normalized model for multi-model support
    scanner_model = models.CharField(max_length=50, choices=SCANNER_MODEL_CHOICES, default='BCDx36HP')
    firmware_version = models.CharField(max_length=20, blank=True)
    # User ownership (stored as ID to avoid cross-DB FK to auth)
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
    """Channel group from favorites (compatible with HPDB format)
    
    Can be associated with either:
    - A FavoritesList (for favorites data from f_*.hpd files)
    - A ScannerProfile (for other scanner data)
    """
    cgroup_id = models.BigIntegerField(null=True, blank=True)  # Can be null per spec
    # Legacy profile FK - optional, used for non-favorites data
    profile = models.ForeignKey(ScannerProfile, on_delete=models.CASCADE, related_name='channel_groups', null=True, blank=True)
    # New favorites_list FK - links C-Group records directly to F-List entries
    favorites_list = models.ForeignKey('FavoritesList', on_delete=models.CASCADE, related_name='channel_groups', null=True, blank=True)
    name_tag = models.CharField(max_length=255)  # Matches HPDB field name
    enabled = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    range_miles = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    location_type = models.CharField(max_length=50, blank=True)  # Circle, Rectangles, etc.
    emergency_alert = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_tag

    class Meta:
        ordering = ['name_tag']
        app_label = 'usersettings'


class Frequency(models.Model):
    """Frequency entry (compatible with HPDB format)"""
    MODULATION_CHOICES = [
        ('FM', 'FM'),
        ('NFM', 'NFM'),
        ('AM', 'AM'),
        ('AUTO', 'AUTO'),
    ]

    channel_group = models.ForeignKey(ChannelGroup, on_delete=models.CASCADE, related_name='frequencies')
    profile = models.ForeignKey(ScannerProfile, on_delete=models.CASCADE, related_name='frequencies_alt', null=True, blank=True)
    name_tag = models.CharField(max_length=255, blank=True)  # Frequency label/description (matches HPDB)
    description = models.CharField(max_length=255, blank=True)  # Additional description
    enabled = models.BooleanField(default=True)
    frequency = models.BigIntegerField()  # in Hz
    modulation = models.CharField(max_length=20, choices=MODULATION_CHOICES)
    audio_option = models.CharField(max_length=50, blank=True)  # TONE=, NAC=, ColorCode=, RAN=, Area= per spec
    delay = models.IntegerField(default=15)
    attenuator = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    number_tag = models.IntegerField(null=True, blank=True)  # 0-9
    priority = models.IntegerField(default=0, blank=True)
    alert_tone = models.CharField(max_length=10, blank=True, default='Off')  # Off/Auto/On
    alert_light = models.CharField(max_length=10, blank=True, default='Off')  # Off/Auto/On
    volume_offset = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    p_ch = models.CharField(max_length=10, blank=True, default='Off')  # Off/On (P-CH flag)
    reserved = models.CharField(max_length=10, blank=True, default='Off')  # Off/On (future use)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name_tag or self.description} - {self.frequency / 1000000:.2f} MHz"

    class Meta:
        ordering = ['frequency']
        app_label = 'usersettings'


class Agency(models.Model):
    """Agency (e.g., Police, Fire, EMS)"""
    name = models.CharField(max_length=255)
    agency_id = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Agencies"
        ordering = ['name']
        app_label = 'usersettings'


class FavoritesList(models.Model):
    """Favorites list entry from f_list.cfg
    
    Each row represents one F-List record from the f_list.cfg file.
    ChannelGroups (C-Group records) link to this via favorites_list FK.
    """
    user_name = models.CharField(max_length=255)  # UserName from spec
    filename = models.CharField(max_length=255)  # Filename from spec (e.g., f_000001.hpd)
    location_control = models.CharField(max_length=10, default='Off')  # LocationControl: On/Off
    monitor = models.CharField(max_length=10, default='Off')  # Monitor: On/Off
    quick_key = models.CharField(max_length=10, blank=True, default='Off')  # QuickKey: Off or 0-99
    number_tag = models.CharField(max_length=10, blank=True, default='Off')  # NumberTag: Off or 0-99
    # User ownership (stored as ID to avoid cross-DB FK to auth)
    user_id = models.IntegerField(null=True, blank=True, db_index=True)
    order = models.IntegerField(default=0)
    # Store startup keys and S-Qkey flags (parts[7:] from f_list.cfg)
    startup_keys = models.JSONField(default=list)  # StartupKey0-9 (10 fields)
    s_qkeys = models.JSONField(default=list)  # S-Qkey_00 to S-Qkey_99 (100 fields)
    raw_data = models.TextField(blank=True)  # Store raw tab-delimited data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_name} ({self.filename})"

    class Meta:
        ordering = ['order', 'number_tag']
        app_label = 'usersettings'


class ScannerFileRecord(models.Model):
    """Structured record storage for scanner files (reconstructable without raw lines)."""
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)  # e.g., profile.cfg, favorites_lists/f_list.cfg
    record_type = models.CharField(max_length=100)
    fields = models.JSONField(default=list)  # list of fields (excluding record_type)
    spec_field_order = models.JSONField(default=list)  # list of spec-aligned field names
    spec_field_map = models.JSONField(default=dict)  # spec field name -> value
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
    file_type = models.CharField(max_length=50)  # 'cfg', 'hpd', 'inf', etc.
    file_size = models.IntegerField()
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ['-upload_time']
        app_label = 'usersettings'


class ScannerRawLine(models.Model):
    """Individual raw lines from scanner files for complete data reconstruction"""
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
