from rest_framework import serializers
from api.models import Scan
from .scan_photo import ScanPhotoSerializer
from .scan_result import ScanResultSerializer


class ScanSerializer(serializers.ModelSerializer):
    scan_photos = ScanPhotoSerializer(many=True, read_only=True)
    scan_results = ScanResultSerializer(many=True, read_only=True)

    class Meta:
        model = Scan
        fields = ["id", "user_id", "hash", "status", "source", "summary", "risk", "created_at", "scan_photos",
                  "scan_results", "error_message"]
        extra_kwargs = {
            'id': {'read_only': True},
            'user_id': {'read_only': True},
            'hash': {'read_only': True},
            'summary': {'read_only': True},
            'risk': {'read_only': True},
            'created_at': {'read_only': True},
            'error_message': {'read_only': True},

            'status': {'required': True},
            'source': {'required': True},
        }
