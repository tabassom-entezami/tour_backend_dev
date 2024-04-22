from nameko.exceptions import deserialize_to_instance


@deserialize_to_instance
class BusinessException(Exception):
    status = 500

    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs
        super(BusinessException, self).__init__(message, *kwargs.values())


@deserialize_to_instance
class NotFound(BusinessException):
    status = 404


@deserialize_to_instance
class NoUniqueMatch(BusinessException):
    status = 409


@deserialize_to_instance
class BadRequest(BusinessException):
    status = 400


@deserialize_to_instance
class InvalidJson(BusinessException):
    status = 400


@deserialize_to_instance
class Conflict(BusinessException):
    status = 409


@deserialize_to_instance
class QuotaExceeded(BusinessException):
    status = 409


@deserialize_to_instance
class Unauthorized(BusinessException):
    status = 401


@deserialize_to_instance
class Forbidden(BusinessException):
    status = 403


@deserialize_to_instance
class InternalError(BusinessException):
    status = 500


@deserialize_to_instance
class ValidationError(BusinessException):
    status = 400

    def __init__(self, message, errors=None):
        errors = errors or {}
        super(ValidationError, self).__init__(
            message=message,
            errors=errors
        )


@deserialize_to_instance
class MissingHttpHeader(BusinessException):
    status = 400

    def __init__(self, message, header_name):
        super(MissingHttpHeader, self).__init__(
            message=message,
            header_name=header_name,
        )


@deserialize_to_instance
class InvalidHttpHeader(BusinessException):
    status = 400

    def __init__(self, message, header_name):
        super(InvalidHttpHeader, self).__init__(
            message=message,
            header_name=header_name,
        )


@deserialize_to_instance
class TooManyRequest(BusinessException):
    status = 429


@deserialize_to_instance
class MethodNotAllowed(BusinessException):
    status = 405
