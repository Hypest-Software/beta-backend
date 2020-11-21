from rest_framework import serializers
from beta_apis.models import User

class AuthUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    