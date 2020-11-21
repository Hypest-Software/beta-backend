from beta_apis.constants import (DefaultResponseSerializer, FailedResponse,
                                 SuccessResponse)
from beta_apis.models import Users, ReportPhoto, Report
from django.contrib.auth.hashers import check_password, make_password
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins
from beta_apis.jwt_utils import encode_jwt
from .serializers import SubmitReportSerializer, ReportSerializer, UploadPhotoSerializer
from beta_apis.permissions import IsLoggedIn
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings
import os
import base64
import json

class SendReportAPIView(generics.CreateAPIView):
    serializer_class = SubmitReportSerializer
    permission_classes = [IsLoggedIn, ]
    @swagger_auto_schema(
        request_body=SubmitReportSerializer,
        responses={
            200: DefaultResponseSerializer,
        },
        tags=['report'],
        operation_id='Send new report'
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return FailedResponse(status_message='Invalid request')
        report = Report(
            latitude = request.data["latitude"],
            longitude = request.data["longitude"],
            describe = request.data["describe"],
            is_public = request.data["is_public"]
        )
        report.save()
        return SuccessResponse(status_message='Success', data=ReportSerializer(report).data)


class UploadPhotoAPIView(generics.CreateAPIView):
    serializer_class = UploadPhotoSerializer
    permission_classes = [IsLoggedIn, ]
    @swagger_auto_schema(
        request_body=UploadPhotoSerializer,
        responses={
            200: DefaultResponseSerializer,
        },
        tags=['report'],
        operation_id='Upload new photo'
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return FailedResponse(status_message='Invalid request')
        report = Report.objects.filter(id=request.data["report_id"]).first()
        if not report:
            return FailedResponse(status_message='Report not found')
        credentials_dict = json.loads(base64.b64decode(settings.GCP_AUTH))
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            credentials_dict
        )
        client = storage.Client(credentials=credentials, project=settings.GCP_PROJECT_ID)
        bucket = client.get_bucket(settings.GCP_BUCKET_NAME)
        image = base64.b64decode(serializer.data.get('photo'))

        record = ReportPhoto(user_id=request.user.id, report_id=request.data["report_id"])
        record.save()

        blob = bucket.blob(f'images/{record.id}.jpg',chunk_size=262144)
        blob.upload_from_string(image)
        blob.make_public()

        record.public_url = blob.public_url
        record.save()

        return SuccessResponse(status_message='Success',data= {
            "photo_id": record.id,
            "public_url": blob.public_url
        })

