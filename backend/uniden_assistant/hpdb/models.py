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

    def __str__(self):
        return f"{self.name} ({self.agency.name})"

    class Meta:
        ordering = ['name']
        app_label = 'hpdb'


class HPDBFrequency(models.Model):
    """Frequency from HPDB database"""
    cfreq_id = models.BigIntegerField()
    cgroup = models.ForeignKey(HPDBChannelGroup, on_delete=models.CASCADE, related_name='frequencies')
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=False)
    frequency = models.BigIntegerField()  # in Hz
    modulation = models.CharField(max_length=20)
    tone = models.CharField(max_length=50, blank=True)
    delay = models.IntegerField(default=15)

    def __str__(self):
        return f"{self.name} - {self.frequency / 1000000:.4f} MHz"

    class Meta:
        ordering = ['frequency']
        app_label = 'hpdb'
