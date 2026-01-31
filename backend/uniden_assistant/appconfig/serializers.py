from rest_framework import serializers
from .models import ScannerModel


class ScannerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScannerModel
        fields = ['id', 'code', 'name', 'enabled', 'sort_order']
