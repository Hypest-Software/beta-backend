from .serializers import CreateUserSerializer
from rest_framework import mixins
from rest_framework import generics
from beta_apis.models import User
from beta_apis.constants import SuccessResponse, FailedResponse
from django.contrib.auth.hashers import make_password, check_password

class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

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