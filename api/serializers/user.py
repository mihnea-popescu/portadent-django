from rest_framework import serializers
from api.models import User
from .scan import ScanSerializer


class UserSerializer(serializers.ModelSerializer):
    # scans = ScanSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "password", "last_login", "username", "email", "first_name", "last_name", "is_staff",
                  "language_tag", "country_code", "timezone", "subscribed", "last_activity", "questionnaire_answers",
                  "created_at", "updated_at"
                  ]
        extra_kwargs = {
            "email": {"required": True},
            "password": {"required": True, "write_only": True},
            "id": {"read_only": True},
            "last_login": {"read_only": True},
            "username": {"read_only": True},
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
            "is_staff": {"read_only": True},
            "language_tag": {"read_only": True},
            "country_code": {"read_only": True},
            "timezone": {"read_only": True},
            "subscribed": {"read_only": True},
            "last_activity": {"read_only": True},
            'questionnaire_answers': {'read_only': True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            # "scans": {"read_only": True}
        }
