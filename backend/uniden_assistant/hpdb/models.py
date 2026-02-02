from django.db import models


# HPDB Database Models (from ubcdx36/HPDB folder)
class Country(models.Model):
    """Country in HPDB hierarchy"""
    country_id = models.IntegerField(unique=True)
    name_tag = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_tag

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['country_id']
        app_label = 'hpdb'
        indexes = [
            models.Index(fields=['country_id']),
        ]
        indexes = [
            models.Index(fields=['country_id']),
        ]


class State(models.Model):
    """State/Province in HPDB hierarchy"""
    state_id = models.IntegerField(unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')
    name_tag = models.CharField(max_length=255)
    short_name = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name_tag} ({self.short_name})"

    class Meta:
        ordering = ['name_tag']
        app_label = 'hpdb'
        indexes = [
            models.Index(fields=['state_id']),
            models.Index(fields=['country']),
        ]


class County(models.Model):
    """County in HPDB hierarchy"""
    county_id = models.IntegerField(unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='counties')
    name_tag = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name_tag}, {self.state.short_name}"

    class Meta:
        verbose_name_plural = "Counties"
        ordering = ['name_tag']
        app_label = 'hpdb'
        indexes = [
            models.Index(fields=['county_id']),
            models.Index(fields=['state']),
        ]


class HPDBAgency(models.Model):
    """Agency from HPDB database (Conventional/Trunk systems)"""
    SYSTEM_TYPES = [
        ('Conventional', 'Conventional'),
        ('Trunk', 'Trunk'),
    ]

    agency_id = models.IntegerField(unique=True)
    name_tag = models.CharField(max_length=255)
    system_type = models.CharField(max_length=20, choices=SYSTEM_TYPES)
    enabled = models.BooleanField(default=False)
    states = models.ManyToManyField(State, blank=True, related_name='hpdb_agencies')
    counties = models.ManyToManyField(County, blank=True, related_name='hpdb_agencies')

    # Common fields for both Conventional and Trunk systems
    quick_key = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    emergency_alert = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    number_tag = models.IntegerField(null=True, blank=True)  # 0-9
    hold_time = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    priority_id_scan = models.CharField(max_length=10, blank=True, default='Off')  # Off/On/Srch
    agc_analog = models.IntegerField(default=400, blank=True)  # AGC value (0-400)
    agc_digital = models.CharField(max_length=20, blank=True, default='Manual')  # Auto/Manual/Default
    number_tag_index = models.IntegerField(default=0, blank=True)  # Index (0-9)

    # Trunk-specific fields (only used when system_type='Trunk')
    trunk_id_search = models.CharField(max_length=20, blank=True, default='')  # Auto/Ignore/etc
    trunk_end_code = models.CharField(max_length=20, blank=True, default='')  # Ignore/etc
    trunk_fleet_map = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    trunk_unit_id = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    trunk_emergency_alert_light = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    trunk_agc = models.CharField(max_length=20, blank=True, default='Analog')  # Analog/Digital
    trunk_status_bit = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    trunk_reserved1 = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    trunk_reserved2 = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    trunk_nxdn_format = models.CharField(max_length=20, blank=True, default='')  # NEXEDGE/etc

    raw_data = models.TextField(blank=True)  # Preserve original record
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name_tag} ({self.system_type})"

    class Meta:
        verbose_name_plural = "HPDB Agencies"
        ordering = ['name_tag']
        app_label = 'hpdb'


class HPDBChannelGroup(models.Model):
    """Channel group from HPDB database"""
    cgroup_id = models.BigIntegerField()
    agency = models.ForeignKey(HPDBAgency, on_delete=models.CASCADE, related_name='channel_groups')
    name_tag = models.CharField(max_length=255)
    enabled = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    range_miles = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    location_type = models.CharField(max_length=50, blank=True)  # Circle, Rectangles, etc.
    emergency_alert = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    raw_data = models.TextField(blank=True)  # Preserve original record

    def __str__(self):
        return f"{self.name_tag} ({self.agency.name_tag})"

    class Meta:
        ordering = ['name_tag']
        app_label = 'hpdb'
        indexes = [
            models.Index(fields=['cgroup_id']),
            models.Index(fields=['agency']),
        ]


class HPDBRectangle(models.Model):
    """Rectangle geographic bounds for channel groups or sites"""
    channel_group = models.ForeignKey(HPDBChannelGroup, on_delete=models.CASCADE, related_name='rectangles', null=True, blank=True)
    latitude_1 = models.DecimalField(max_digits=9, decimal_places=6)  # First corner
    longitude_1 = models.DecimalField(max_digits=10, decimal_places=6)  # First corner
    latitude_2 = models.DecimalField(max_digits=9, decimal_places=6)  # Opposite corner
    longitude_2 = models.DecimalField(max_digits=10, decimal_places=6)  # Opposite corner
    
    class Meta:
        app_label = 'hpdb'
        verbose_name_plural = 'HPDB Rectangles'
        indexes = [
            models.Index(fields=['channel_group']),
        ]

    def __str__(self):
        return f"Rectangle: ({self.latitude_1}, {self.longitude_1}) to ({self.latitude_2}, {self.longitude_2})"

    @property
    def min_latitude(self):
        """Minimum (southernmost) latitude"""
        return min(float(self.latitude_1), float(self.latitude_2))
    
    @property
    def max_latitude(self):
        """Maximum (northernmost) latitude"""
        return max(float(self.latitude_1), float(self.latitude_2))
    
    @property
    def min_longitude(self):
        """Minimum (westernmost) longitude"""
        return min(float(self.longitude_1), float(self.longitude_2))
    
    @property
    def max_longitude(self):
        """Maximum (easternmost) longitude"""
        return max(float(self.longitude_1), float(self.longitude_2))


class HPDBFrequency(models.Model):
    """Frequency from HPDB database"""
    cfreq_id = models.BigIntegerField()
    cgroup = models.ForeignKey(HPDBChannelGroup, on_delete=models.CASCADE, related_name='frequencies')
    name_tag = models.CharField(max_length=255, blank=True)  # Frequency label/description
    description = models.CharField(max_length=255, blank=True)  # Additional description (e.g., "Security", "Staff")
    enabled = models.BooleanField(default=False)
    frequency = models.BigIntegerField()  # in Hz
    modulation = models.CharField(max_length=20)
    audio_option = models.CharField(max_length=50, blank=True)  # TONE=, NAC=, ColorCode=, RAN=, Area= per spec
    delay = models.IntegerField(default=15)
    attenuator = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    number_tag = models.IntegerField(null=True, blank=True)  # 0-9
    priority = models.IntegerField(default=0, blank=True)  # Priority level
    alert_tone = models.CharField(max_length=10, blank=True, default='Off')  # Off/Auto/On
    alert_light = models.CharField(max_length=10, blank=True, default='Off')  # Off/Auto/On
    volume_offset = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    p_ch = models.CharField(max_length=10, blank=True, default='Off')  # Off/On (P-CH flag)
    reserved = models.CharField(max_length=10, blank=True, default='Off')  # Off/On (future use)
    raw_data = models.TextField(blank=True)  # Preserve original record

    def __str__(self):
        return f"{self.name_tag} - {self.frequency / 1000000:.4f} MHz"

    class Meta:
        ordering = ['frequency']
        app_label = 'hpdb'
        indexes = [
            models.Index(fields=['cfreq_id']),
            models.Index(fields=['cgroup']),
        ]


class HPDBSite(models.Model):
    """Trunked radio site from HPDB database"""
    agency = models.ForeignKey(HPDBAgency, on_delete=models.CASCADE, related_name='sites')
    name_tag = models.CharField(max_length=255)
    enabled = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    range_miles = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    modulation = models.CharField(max_length=20, blank=True, default='AUTO')  # AUTO/FM/etc
    bandwidth = models.CharField(max_length=20, blank=True, default='Standard')  # Standard/Narrow/Wide
    band_type = models.CharField(max_length=20, blank=True, default='Wide')  # Wide/Narrow
    location_type = models.CharField(max_length=20, blank=True, default='Circle')  # Circle/Rectangle
    emergency_alert = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    agc_analog = models.IntegerField(default=400, blank=True)  # AGC value (0-400)
    agc_digital = models.CharField(max_length=20, blank=True, default='Manual')  # Auto/Manual/Default
    number_tag = models.IntegerField(null=True, blank=True)  # 0-9
    reserved = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    raw_data = models.TextField(blank=True)  # Preserve original record

    def __str__(self):
        return f"{self.name_tag} ({self.agency.name_tag})"

    class Meta:
        ordering = ['name_tag']
        app_label = 'hpdb'
        indexes = [
            models.Index(fields=['agency']),
        ]


class HPDBTFreq(models.Model):
    """Trunked frequency from HPDB database"""
    site = models.ForeignKey(HPDBSite, on_delete=models.CASCADE, related_name='frequencies')
    enabled = models.BooleanField(default=False)
    frequency = models.BigIntegerField()  # in Hz
    lcn = models.IntegerField(default=0)  # Logical Channel Number
    mode = models.CharField(max_length=20, blank=True, default='Srch')  # Srch/etc
    raw_data = models.TextField(blank=True)  # Preserve original record

    def __str__(self):
        return f"{self.frequency / 1000000:.4f} MHz (LCN {self.lcn})"

    class Meta:
        ordering = ['frequency']
        app_label = 'hpdb'
        indexes = [
            models.Index(fields=['site']),
        ]


class HPDBTGroup(models.Model):
    """Trunked talk group from HPDB database"""
    agency = models.ForeignKey(HPDBAgency, on_delete=models.CASCADE, related_name='talk_groups')
    name_tag = models.CharField(max_length=255)
    enabled = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    range_miles = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    location_type = models.CharField(max_length=20, blank=True, default='Circle')  # Circle/Rectangle
    emergency_alert = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    raw_data = models.TextField(blank=True)  # Preserve original record

    def __str__(self):
        return f"{self.name_tag} ({self.agency.name_tag})"

    class Meta:
        ordering = ['name_tag']
        app_label = 'hpdb'
        indexes = [
            models.Index(fields=['agency']),
        ]


class HPDBTGID(models.Model):
    """Talk Group ID from HPDB database"""
    tgroup = models.ForeignKey(HPDBTGroup, on_delete=models.CASCADE, related_name='tgids')
    name_tag = models.CharField(max_length=255)
    enabled = models.BooleanField(default=False)
    tgid = models.IntegerField()  # Talk Group ID number
    audio_type = models.CharField(max_length=20, blank=True, default='ALL')  # ALL/Digital/Analog
    delay = models.IntegerField(default=208)  # Delay in ms
    number_tag = models.IntegerField(null=True, blank=True)  # 0-9
    priority = models.IntegerField(default=0, blank=True)  # Priority level
    alert_tone = models.CharField(max_length=10, blank=True, default='Off')  # Off/Auto/On
    alert_light = models.CharField(max_length=10, blank=True, default='Off')  # Off/Auto/On
    reserved1 = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    volume_offset = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    reserved2 = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    reserved3 = models.CharField(max_length=10, blank=True, default='Off')  # Off/On
    match_type = models.CharField(max_length=20, blank=True, default='Any')  # Any/Exact
    raw_data = models.TextField(blank=True)  # Preserve original record

    def __str__(self):
        return f"{self.name_tag} (TGID {self.tgid})"

    class Meta:
        ordering = ['tgid']
        app_label = 'hpdb'
        indexes = [
            models.Index(fields=['tgroup']),
            models.Index(fields=['tgid']),
        ]


class HPDBDQKsStatus(models.Model):
    """Quick Key Status (100 boolean flags) from HPDB database"""
    agency = models.OneToOneField(HPDBAgency, on_delete=models.CASCADE, related_name='quick_key_status')
    quick_key_status = models.JSONField(default=list)  # Array of 100 On/Off values
    raw_data = models.TextField(blank=True)  # Preserve original record

    def __str__(self):
        return f"Quick Keys for {self.agency.name_tag}"

    class Meta:
        verbose_name = "HPDB Quick Key Status"
        verbose_name_plural = "HPDB Quick Key Statuses"
        app_label = 'hpdb'
        indexes = [
            models.Index(fields=['agency']),
        ]


class HPDBBandPlan(models.Model):
    """Band plan configuration from HPDB database"""
    PLAN_TYPES = [
        ('P25', 'P25'),
        ('Motorola', 'Motorola'),
    ]

    agency = models.ForeignKey(HPDBAgency, on_delete=models.CASCADE, related_name='band_plans')
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    band_plan_data = models.JSONField(default=list)  # Array of 31-32 integer values
    raw_data = models.TextField(blank=True)  # Preserve original record

    def __str__(self):
        return f"{self.plan_type} Band Plan for {self.agency.name_tag}"

    class Meta:
        verbose_name = "HPDB Band Plan"
        app_label = 'hpdb'
        indexes = [
            models.Index(fields=['agency']),
        ]


class HPDBFileRecord(models.Model):
    """Structured record storage for HPDB files (reconstructable without raw lines)."""
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)  # e.g., HPDB/hpdb.cfg or HPDB/s_000001.hpd
    record_type = models.CharField(max_length=100)
    fields = models.JSONField(default=list)  # list of fields (excluding record_type)
    spec_field_order = models.JSONField(default=list)  # list of spec-aligned field names
    spec_field_map = models.JSONField(default=dict)  # spec field name -> value
    trailing_empty_fields = models.IntegerField(default=0)
    line_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['file_path', 'line_number']
        app_label = 'hpdb'
        indexes = [
            models.Index(fields=['file_path', 'line_number']),
            models.Index(fields=['record_type']),
        ]


class HPDBRawFile(models.Model):
    """Raw HPDB file data for reconstruction and archiving"""
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)  # 'cfg', 'hpd', etc.
    file_size = models.IntegerField()
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ['-upload_time']
        app_label = 'hpdb'


class HPDBRawLine(models.Model):
    """Individual raw lines from HPDB files for complete data reconstruction"""
    raw_file = models.ForeignKey(HPDBRawFile, on_delete=models.CASCADE, related_name='lines')
    line_number = models.IntegerField()  # Line number in original file
    content = models.TextField()  # Raw line content (preserves tabs, spacing)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['raw_file', 'line_number']
        app_label = 'hpdb'
        indexes = [
            models.Index(fields=['raw_file', 'line_number']),
        ]


class HPDBImportJob(models.Model):
    """Track HPDB import job progress and status"""
    STATUS_CHOICES = [
        ('uploading', 'Uploading'),
        ('uploaded', 'Upload Complete'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    job_id = models.CharField(max_length=36, unique=True, primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploading')
    
    # Upload stage
    total_files = models.IntegerField(default=0)
    uploaded_files = models.IntegerField(default=0)
    total_bytes = models.BigIntegerField(default=0)
    uploaded_bytes = models.BigIntegerField(default=0)
    
    # Processing stage
    processing_stage = models.CharField(max_length=50, blank=True)  # 'config', 'systems', etc.
    current_file = models.CharField(max_length=255, blank=True)
    processed_files = models.IntegerField(default=0)
    
    # Results
    error_message = models.TextField(blank=True)
    result_data = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Import {self.job_id[:8]} - {self.status}"

    class Meta:
        ordering = ['-created_at']
        app_label = 'hpdb'
