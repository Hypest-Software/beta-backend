from rest_framework.response import Response


class FailedResponse(Response):
    response_data = {
        "success": False,
        "statusCode": 400,
        "statusMessage": "",
        "data": None
    }

    def __init__(self, data=None, status_code=400, status_message='', **kwargs):
        response_data = self.response_data
        response_data['statusMessage'] = status_message
        response_data['statusCode'] = status_code
        response_data['data'] = data
        data = response_data
        super().__init__(data, **kwargs)


class SuccessResponse(Response):
    response_data = {
        "success": True,
        "statusCode": 0,
        "statusMessage": "Success",
        "data": None
    }

    def __init__(self, data=None, status_code=200, status_message='Success', **kwargs):
        response_data = self.response_data
        response_data['statusMessage'] = status_message
        response_data['statusCode'] = status_code
        response_data['data'] = data
        data = response_data
        super().__init__(data, **kwargs)


class RawResponse(Response):
    def __init__(self, data=None, **kwargs):
        super().__init__(data, **kwargs)
