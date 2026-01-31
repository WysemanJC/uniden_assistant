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


class Frequency(models.Model):
    """Frequency entry"""
    MODULATION_CHOICES = [
        ('FM', 'FM'),
        ('AM', 'AM'),
        ('AUTO', 'AUTO'),
    ]

    profile = models.ForeignKey(ScannerProfile, on_delete=models.CASCADE, related_name='frequencies')
    name = models.CharField(max_length=255)
    frequency = models.BigIntegerField()  # in Hz
    modulation = models.CharField(max_length=10, choices=MODULATION_CHOICES)
    nac = models.CharField(max_length=10, blank=True)  # Network Access Code
    enabled = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.frequency / 1000000:.2f} MHz"

    class Meta:
        ordering = ['frequency']
        app_label = 'usersettings'


class ChannelGroup(models.Model):
    """Channel group (like a favorites list)"""
    profile = models.ForeignKey(ScannerProfile, on_delete=models.CASCADE, related_name='channel_groups')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    enabled = models.BooleanField(default=True)
    frequencies = models.ManyToManyField(Frequency, blank=True, related_name='groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
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
    """Favorites list entry from f_list.cfg"""
    name = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)  # e.g., f_000001.hpd
    # User ownership (stored as ID to avoid cross-DB FK to auth)
    user_id = models.IntegerField(null=True, blank=True, db_index=True)
    # Normalize per-scanner model
    scanner_model = models.CharField(max_length=50, choices=SCANNER_MODEL_CHOICES, default='BCDx36HP')
    enabled = models.BooleanField(default=False)  # parts[3] - On/Off
    disabled_on_power = models.BooleanField(default=True)  # parts[4] - On/Off for power up
    quick_key = models.CharField(max_length=10, blank=True)  # parts[5]
    list_number = models.IntegerField()  # parts[6]
    order = models.IntegerField(default=0)
    # Store all flag fields (parts[7:] from f_list.cfg)
    flags = models.TextField(blank=True)  # JSON-serialized flags
    raw_data = models.TextField(blank=True)  # Store raw tab-delimited data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.filename})"

    class Meta:
        ordering = ['order', 'list_number']
        app_label = 'usersettings'
