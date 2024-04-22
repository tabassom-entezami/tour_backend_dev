import logging

from nameko.rpc import RpcProxy

from tour_shared.handlers import api
from tour_shared.middlewares import Middleware, translation_middleware

_logger = logging.getLogger(__name__)


class GatewayController(metaclass=Middleware):
    """
    Service acts as a gateway to other services over HTTP.
    """
    name = 'gateway'

    processor_rpc = RpcProxy('auth')

    middlewares = [translation_middleware]

    @api.get('/health')
    def health_check(self, request):
        return 200, {}
