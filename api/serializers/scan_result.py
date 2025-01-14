from rest_framework import serializers
from api.models import ScanResult


class ScanResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanResult
        fields = ["id", "tooth_type", "severity", "details"]
        extra_kwargs = {
            'id': {'read_only': True},
            'tooth_type': {'required': True},
            'severity': {'required': True},
            'details': {'read_only': True},
        }
