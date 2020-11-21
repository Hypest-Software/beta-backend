from rest_framework import serializers
from rest_framework.serializers import Serializer


class SubmitReportSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    describe = serializers.CharField(required=False)
    photo_id = serializers.CharField(required=False)


class UploadPhotoSerializer(serializers.Serializer):
    photo = serializers.CharField(required=True)

