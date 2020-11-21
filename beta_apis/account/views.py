from beta_apis.constants import (DefaultResponseSerializer, FailedResponse,
                                 SuccessResponse)
from beta_apis.models import Users
from django.contrib.auth.hashers import check_password, make_password
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins
from beta_apis.jwt_utils import encode_jwt
from .serializers import AuthUserSerializer, AccountUpdateInfoSerializer
from beta_apis.permissions import IsLoggedIn

class UserRegisterAPIView(generics.CreateAPIView):
    queryset = Users.objects.all()
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
        if not Users.validate_username(username):
            return FailedResponse(status_message='Username is not valid')
        user = Users.objects.filter(username=username)
        if user:
            return FailedResponse(status_message='Username is not available')
        if not Users.validate_password(password):
            return FailedResponse(status_message='Password is not valid')
        user = Users(username=username, password=make_password(password))
        user.save()
        return SuccessResponse(status_message='Success')


class UserLoginAPIView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = AuthUserSerializer

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
        user = Users.objects.filter(username=username).first()
        if not user or not check_password(password, user.password):
            return FailedResponse(status_message='Login failed. Invalid username or password.')
        print(user.id)
        token = encode_jwt(str(user.id))
        return SuccessResponse(status_message='Success', data={
            "token": token,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "photo": user.photo
        })


class UserUpdateInfoAPIView(generics.CreateAPIView):
    serializer_class = AccountUpdateInfoSerializer
    permission_classes = [IsLoggedIn, ]
    @swagger_auto_schema(
        request_body=AccountUpdateInfoSerializer,
        responses={
            200: DefaultResponseSerializer,
        },
        tags=['account'],
        operation_id='Update account information'
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return FailedResponse(status_message='Invalid request')
        email = serializer.data.get('email')
        first_name = serializer.data.get('first_name')
        last_name = serializer.data.get('last_name')
        full_name = serializer.data.get('full_name')
        user = request.user
        if email:
            if '.' in email and '@' in email:
                user.email = email
            else:
                return FailedResponse(status_message='Email address is not valid')
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if full_name:
            user.full_name = full_name
        user.save()
        return SuccessResponse(status_message='Success',data={
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "photo": user.photo
        })