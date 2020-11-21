from rest_framework import serializers
from rest_framework.serializers import Serializer
from beta_apis.models import Report

class SubmitReportSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    is_public = serializers.BooleanField(required=False, default=True)
    describe = serializers.CharField(required=False)

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'latitude', 'longitude', 'describe', 'is_public', 'created_at', 'updated_at']


class UploadPhotoSerializer(serializers.Serializer):
    report_id = serializers.CharField(required=True)
    photo = serializers.CharField(required=True)

