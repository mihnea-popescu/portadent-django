from rest_framework import serializers


class WebScanSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    questionnaire_answers = serializers.JSONField(required=True)
    language_tag = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=32)
    country_code = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=8)
    timezone = serializers.IntegerField(required=False, allow_null=True, min_value=-1000,
                                        max_value=1000)


class FeedbackSerializer(serializers.Serializer):
    feedback_type = serializers.CharField(required=True, max_length=100)
    details = serializers.CharField(required=True, allow_null=True, max_length=500)
    params = serializers.JSONField(required=True)
