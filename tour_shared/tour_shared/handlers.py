from functools import partial
import logging

import werkzeug.exceptions
from nameko.rpc import Rpc
from eventlet.event import Event
from nameko.web.handlers import HttpRequestHandler
from werkzeug import Response

from tour_shared.exceptions import *
# noinspection PyUnresolvedReferences
from tour_shared.monkey_patch.werkzeug import *
from tour_shared.responses import JSONResponse, JSONErrorResponse
from tour_shared.middlewares import translation_middleware

logger = logging.getLogger(__name__)


class TourRPC(Rpc):
    def __init__(self, *args, **kwargs):
        if 'expected_exceptions' not in kwargs:
            kwargs['expected_exceptions'] = (BusinessException, )
        super(TourRPC, self).__init__(*args, **kwargs)


rpc = TourRPC.decorator


class APIRequestHandler(HttpRequestHandler):
    """
    Extend nameko ``HttpRequestHandler`` class to provide some extra check and
    functionality for API endpoints.
    """

    def __init__(self, method, url, **kwargs):
        kwargs['expected_exceptions'] = self.get_expected_exceptions()
        version = kwargs.pop('version', 1)
        url = f'/v{version!r}{url}'
        super(APIRequestHandler, self).__init__(method, url, **kwargs)

    def get_expected_exceptions(self):
        return BusinessException, werkzeug.exceptions.BadRequest

    @translation_middleware
    def handle_request(self, request):
        """
        Override parent method to fit in some extra logic.
        """
        request.shallow = False
        try:
            context_data = self.server.context_data_from_headers(request)
            args, kwargs = self.get_entrypoint_parameters(request)

            self.check_signature(args, kwargs)
            event = Event()
            self.container.spawn_worker(
                self, args, kwargs, context_data=context_data,
                handle_result=partial(self.handle_result, event))
            result = event.wait()

            response = self.response_from_result(result)

        except Exception as exc:
            response = self.response_from_exception(exc)
        return response

    def response_from_result(self, result):
        if isinstance(result, JSONResponse) or isinstance(result, Response):
            return result

        headers = None
        if isinstance(result, tuple):
            if len(result) == 3:
                status, headers, payload = result
            else:
                status, payload = result
        else:
            payload = result
            status = 200

        return JSONResponse(payload, status=status, headers=headers)

    def response_from_exception(self, exc):
        """Handle exceptions in controller."""
        if not any(isinstance(exc, expected_exc) for expected_exc in self.get_expected_exceptions()):
            logger.exception(f'Unhandled exception reached the gateway exit: {exc}')
            return JSONErrorResponse(
                error_code="InternalError",
                message="We're sorry for the inconvenience, there is a problem "
                        "on our side, please try again later "
                        "and if the problem persists, contact HashStudio support.",
                status=500,
            )
        return JSONErrorResponse(
            error_code=exc.__class__.__name__,
            message=getattr(exc, 'message', str(exc)),
            params=getattr(exc, 'kwargs', {}),
            status=getattr(exc, 'status', 400),
        )

    @classmethod
    def get(cls, url, **kwargs):
        return cls.decorator('GET', url, **kwargs)

    @classmethod
    def post(cls, url, **kwargs):
        return cls.decorator('POST', url, **kwargs)

    @classmethod
    def put(cls, url, **kwargs):
        return cls.decorator('PUT', url, **kwargs)

    @classmethod
    def patch(cls, url, **kwargs):
        return cls.decorator('PATCH', url, **kwargs)

    @classmethod
    def delete(cls, url, **kwargs):
        return cls.decorator('DELETE', url, **kwargs)


api = APIRequestHandler

