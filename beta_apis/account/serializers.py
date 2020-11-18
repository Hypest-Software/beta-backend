from rest_framework import serializers
from beta_apis.models import User

class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    