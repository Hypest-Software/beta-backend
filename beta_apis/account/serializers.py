from rest_framework import serializers
from beta_apis.models import User


class AuthUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AccountUpdateInfoSerializer(serializers.Serializer):
    email = serializers.CharField(required=False, allow_blank=True,
                                 allow_null=True)
    first_name = serializers.CharField(required=False, allow_blank=True,
                                 allow_null=True)
    last_name = serializers.CharField(required=False, allow_blank=True,
                                 allow_null=True)
    full_name = serializers.CharField(required=False, allow_blank=True,
                                 allow_null=True)
