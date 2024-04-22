import json

from werkzeug import Response

from tour_shared.encoders import ObjectJsonEncoder


class JSONResponse(Response):
    """Extend werkzeug ``Response`` for RFC 4627(json) comply."""
    default_mimetype = 'application/json'

    def __init__(self, response, **kwargs):
        if response is None:
            raise ValueError('response should not be None')
        super().__init__(
            response=json.dumps(response, cls=ObjectJsonEncoder),
            **kwargs
        )


class JSONErrorResponse(JSONResponse):
    def __init__(self, error_code, message, status, params=None, **kwargs):
        payload = {
            "error_code": error_code,
            "message": message,
            **(params or {}),
        }
        super(JSONErrorResponse, self).__init__(
            response=payload,
            status=status,
            **kwargs,
        )

