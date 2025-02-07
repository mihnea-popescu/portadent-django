from rest_framework import serializers
from api.models import ScanPhoto, Scan
from PIL import Image
from core.image_processing.image import encode_image_to_base64


class ScanPhotoSerializer(serializers.ModelSerializer):
    image_base64 = serializers.SerializerMethodField()

    class Meta:
        model = ScanPhoto
        fields = ["id", "type", "file", "scan", "image_base64"]
        extra_kwargs = {
            'id': {'read_only': True},
            'type': {'required': True},
            'file': {'required': True, 'write_only': True},
            'scan': {'required': True},
            'image_base64': {'read_only': True},
        }

    def validate_scan(self, value):
        """
        Check that the provided scan corresponds to an existing Scan instance.
        """
        if not value:
            raise serializers.ValidationError("Invalid scan id: no Scan object found with this ID.")

        user = self.context['request'].user

        if not Scan.objects.filter(id=value.id, user_id=user.id).exists():
            raise serializers.ValidationError("Invalid scan id: no Scan object found with this ID.")
        return value

    def get_image_base64(self, obj):
        if isinstance(obj, ScanPhoto) and obj.file:
            with Image.open(obj.file.path) as img:
                img_format = img.format if img.format in ["JPEG", "PNG"] else "JPEG"
                return encode_image_to_base64(img, img_format)
        return None
