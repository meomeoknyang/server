from rest_framework.response import Response

class CustomResponse(Response):
    def __init__(self, status_text, message, code, data=None, **kwargs):
        response_data = {
            "status": status_text,
            "message": message,
            "code": code,
            "data": data
        }
        super().__init__(response_data, status=code, **kwargs)
