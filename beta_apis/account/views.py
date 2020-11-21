from beta_apis.constants import (DefaultResponseSerializer, FailedResponse,
                                 SuccessResponse)
from beta_apis.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins

from .serializers import CreateUserSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    @swagger_auto_schema(
        request_body=CreateUserSerializer,
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
