from django.db import models


# HPDB Database Models (from ubcdx36/HPDB folder)
class Country(models.Model):
    """Country in HPDB hierarchy"""
    country_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']
        app_label = 'hpdb'


class State(models.Model):
    """State/Province in HPDB hierarchy"""
    state_id = models.IntegerField(unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']
        app_label = 'hpdb'


class County(models.Model):
    """County in HPDB hierarchy"""
    county_id = models.IntegerField(unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='counties')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.state.code}"

    class Meta:
        verbose_name_plural = "Counties"
        ordering = ['name']
        app_label = 'hpdb'


class HPDBAgency(models.Model):
    """Agency from HPDB database (Conventional/Trunk systems)"""
    SYSTEM_TYPES = [
        ('Conventional', 'Conventional'),
        ('Trunk', 'Trunk'),
    ]

    agency_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    system_type = models.CharField(max_length=20, choices=SYSTEM_TYPES)
    enabled = models.BooleanField(default=False)
    states = models.ManyToManyField(State, blank=True, related_name='hpdb_agencies')
    counties = models.ManyToManyField(County, blank=True, related_name='hpdb_agencies')
    raw_data = models.TextField(blank=True)  # Preserve original record
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.system_type})"

    class Meta:
        verbose_name_plural = "HPDB Agencies"
        ordering = ['name']
        app_label = 'hpdb'


class HPDBChannelGroup(models.Model):
    """Channel group from HPDB database"""
    cgroup_id = models.BigIntegerField()
    agency = models.ForeignKey(HPDBAgency, on_delete=models.CASCADE, related_name='channel_groups')
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    range_miles = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    location_type = models.CharField(max_length=50, blank=True)  # Circle, Rectangles, etc.
    raw_data = models.TextField(blank=True)  # Preserve original record

    def __str__(self):
        return f"{self.name} ({self.agency.name})"

    class Meta:
        ordering = ['name']
        app_label = 'hpdb'


class HPDBFrequency(models.Model):
    """Frequency from HPDB database"""
    cfreq_id = models.BigIntegerField()
    cgroup = models.ForeignKey(HPDBChannelGroup, on_delete=models.CASCADE, related_name='frequencies')
    name = models.CharField(max_length=255, blank=True)  # Frequency label/description
    description = models.CharField(max_length=255, blank=True)  # Additional description (e.g., "Security", "Staff")
    enabled = models.BooleanField(default=False)
    frequency = models.BigIntegerField()  # in Hz
    modulation = models.CharField(max_length=20)
    tone = models.CharField(max_length=50, blank=True)
    delay = models.IntegerField(default=15)
    raw_data = models.TextField(blank=True)  # Preserve original record

    def __str__(self):
        return f"{self.name} - {self.frequency / 1000000:.4f} MHz"

    class Meta:
        ordering = ['frequency']
        app_label = 'hpdb'


class HPDBFileRecord(models.Model):
    """Structured record storage for HPDB files (reconstructable without raw lines)."""
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)  # e.g., HPDB/hpdb.cfg or HPDB/s_000001.hpd
    record_type = models.CharField(max_length=100)
    fields = models.JSONField(default=list)  # list of fields (excluding record_type)
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
