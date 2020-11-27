from rest_framework.response import Response
from rest_framework import serializers

class FailedResponse(Response):

    def __init__(self, data=dict(), status_code=400, status_message='', **kwargs):
        data['message'] = status_message
        super().__init__(data, status=status_code,  **kwargs)


class SuccessResponse(Response):

    def __init__(self, data=None, status_code=200, status_message='Success', **kwargs):
        data['message'] = status_message
        super().__init__(data, status=status_code, **kwargs)


class RawResponse(Response):
    def __init__(self, data=None, **kwargs):
        super().__init__(data, **kwargs)


class DefaultResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    statusCode = serializers.IntegerField()
    statusMessage = serializers.CharField()
    data = serializers.Field()

