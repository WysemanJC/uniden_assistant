from django.db import models


class ScannerModel(models.Model):
    """Supported scanner models for the application"""
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    enabled = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['sort_order', 'name']
