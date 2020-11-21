from beta_apis.constants import (DefaultResponseSerializer, FailedResponse,
                                 SuccessResponse)
from beta_apis.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins
from rest_framework_jwt.settings import api_settings
from .serializers import AuthUserSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AuthUserSerializer

    @swagger_auto_schema(
        request_body=AuthUserSerializer,
        responses={
            200: DefaultResponseSerializer,
        },
        tags=['account'],
        operation_id='Create new account'
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return FailedResponse(status_message='Invalid request')
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        if not User.validate_username(username):
            return FailedResponse(status_message='Username is not valid')
        user = User.objects.filter(username=username)
        if user:
            return FailedResponse(status_message='Username is not available')
        if not User.validate_password(password):
            return FailedResponse(status_message='Password is not valid')
        user = User(username=username, password=make_password(password))
        user.save()
        return SuccessResponse(status_message='Success')


class UserLoginAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AuthUserSerializer
#    authentication_classes = [JSONWebTokenAuthentication,]

    @swagger_auto_schema(
        request_body=AuthUserSerializer,
        responses={
            200: DefaultResponseSerializer,
        },
        tags=['account'],
        operation_id='Account login'
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return FailedResponse(status_message='Invalid request')
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        user = User.objects.filter(username=username).first()
        if not user or not check_password(password, user.password):
            return FailedResponse(status_message='Login failed. Invalid username or password.')
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return SuccessResponse(status_message='Success', data={
            "token": token,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "photo": user.photo
        })
