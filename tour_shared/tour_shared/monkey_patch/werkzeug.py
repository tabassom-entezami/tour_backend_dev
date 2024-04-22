"""
Importing this module will monkey patch the 404 and 405 default errors in werkzeug
to make them similar to our own errors.
"""

from werkzeug import  exceptions as werkzeug_exc
from tour_shared.responses import JSONErrorResponse

__all__ = []


def not_found(self, environ=None):
    return JSONErrorResponse(
        error_code="InvalidPath",
        message='The requested URL was not found on the server.',
        status=404,
    )


def method_not_allowed(self, environ=None):
    return JSONErrorResponse(
        error_code="InvalidHTTPMethod",
        message='The method is not allowed for the requested URL.',
        status=405,
    )


werkzeug_exc.NotFound.get_response = not_found
werkzeug_exc.MethodNotAllowed.get_response = method_not_allowed

