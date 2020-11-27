from beta_apis.constants import (DefaultResponseSerializer, FailedResponse,
                                 SuccessResponse)
from beta_apis.models import Users, ReportPhoto, Report
from django.contrib.auth.hashers import check_password, make_password
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins
from beta_apis.jwt_utils import encode_jwt
from .serializers import SubmitReportSerializer, ReportSerializer, UploadPhotoSerializer, ReportPhotoSerializer
from beta_apis.permissions import IsLoggedIn
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings
import os
import base64
import json
from geopy.geocoders import Nominatim

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


        geolocator = Nominatim(user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36")
        location = geolocator.reverse(f'{request.data["latitude"]}, {request.data["longitude"]}')
        address = split_data(location)["powiat"]

        report = Report(
            user_id = request.user.id,
            latitude = serializer.data.get('latitude'),
            longitude = serializer.data.get('longitude'),
            describe = serializer.data.get('describe'),
            is_public = serializer.data.get('is_public'),
            address = address
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


class ListMyReportAPIView(generics.ListAPIView):
    permission_classes = [IsLoggedIn, ]
    @swagger_auto_schema(
        responses={
            200: DefaultResponseSerializer,
        },
        tags=['report'],
        operation_id='Get all report of current acccount'
    )
    def get(self, request, *args, **kwargs):
        reports = ReportSerializer(Report.objects.filter(user_id=request.user.id), many=True).data
        for report in reports:
            photos = ReportPhoto.objects.filter(report_id=report["id"])
            report['photo'] = ReportPhotoSerializer(photos, many=True).data
        return SuccessResponse(status_message='Success',data=reports)


class ListAllReportAPIView(generics.ListAPIView):
    permission_classes = [IsLoggedIn, ]
    @swagger_auto_schema(
        responses={
            200: DefaultResponseSerializer,
        },
        tags=['report'],
        operation_id='Get all report of current acccount'
    )
    def get(self, request, *args, **kwargs):
        reports = ReportSerializer(Report.objects.all(), many=True).data
        return SuccessResponse(status_message='Success',data=reports)


def find_nearby_powiat(cords: str):
    cords = list(map(float, cords.split(", ")))
    for i in range(-10, 10):
        for j in range(-10, 10):
            if i < 0:
                x =  float("-0.0000" + str(i)[1:])
            else:
                x = float("0.0000" + str(i))
            if j < 0:
                y =  float("-0.0000" + str(j)[1:])
            else:
                y = float("0.0000" + str(j))
            test_loc = geolocator.reverse(f"{cords[0]+x}, {cords[1]+y}")
            test_loc = str(test_loc).split(", ")
            if len(test_loc) == 7:
                print(i,j)
                return None
    print(len(test_loc))
    


def split_data(data: str):
    data = str(data)
    data = data.split(",")
    for data_index, d in enumerate(data):
        data[data_index] = d.strip()
    print()
    if len(data) != 7:
        empty_result = {"kraj": "",
                        "wojewodztwo": "",
                        "powiat": "",
                        "gmina": "",
                        "kod_pocztowy": "",
                        "miejscowossc": "",
                        "ulica": ""}
        return empty_result
    result = {"kraj": data[-1],
              "wojewodztwo": data[-3],
              "powiat": data[-4],
              "gmina": data[-5],
              "kod_pocztowy": data[-2],
              "miejscowossc": data[-6],
              "ulica": data[-7]}
    return result