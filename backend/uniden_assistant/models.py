from django.db import models


class ScannerProfile(models.Model):
    """Represents a scanner profile with associated frequencies and channel groups."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name


class Agency(models.Model):
    """Represents an agency that owns frequencies."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "agencies"
        ordering = ['name']

    def __str__(self):
        return self.name


class ChannelGroup(models.Model):
    """Groups related frequencies together."""
    profile = models.ForeignKey(ScannerProfile, on_delete=models.CASCADE, related_name='channel_groups')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.profile.name} - {self.name}"


class Frequency(models.Model):
    """Represents a frequency entry with associated metadata."""
    MODULATION_CHOICES = [
        ('AM', 'Amplitude Modulation'),
        ('FM', 'Frequency Modulation'),
        ('NFM', 'Narrowband FM'),
        ('WFM', 'Wideband FM'),
    ]

    channel_group = models.ForeignKey(ChannelGroup, on_delete=models.CASCADE, related_name='frequencies')
    frequency = models.DecimalField(max_digits=12, decimal_places=4)
    name = models.CharField(max_length=255)
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, blank=True)
    modulation = models.CharField(max_length=10, choices=MODULATION_CHOICES, default='FM')
    description = models.TextField(blank=True)
    priority = models.IntegerField(default=0)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['frequency']

    def __str__(self):
        return f"{self.frequency} MHz - {self.name}"
