import logging
from functools import wraps

from werkzeug import Request

from \
    .i18n import translate


_logger = logging.getLogger(__name__)


class Middleware(type):
    def __new__(mcs, name, bases, attribute_dict):
        for attr in attribute_dict:
            value = attribute_dict[attr]
            if hasattr(value, 'nameko_entrypoints'):
                for middleware in attribute_dict['middlewares']:
                    attribute_dict[attr] = middleware(value)

        return super(Middleware, mcs).__new__(mcs, name, bases, attribute_dict)


def translation_middleware(func):
    @wraps(func)
    def decorator(svc, *args, **kwargs):
        first_arg = None
        if args:
            first_arg = args[0]

        if first_arg is not None:
            if isinstance(first_arg, Request):
                setup_http_lang(first_arg)
            elif isinstance(first_arg, dict):
                setup_rpc_lang(first_arg)
            else:
                _logger.warning('Language context cannot be founded')
        else:
            _logger.warning('Language context cannot be founded')

        result = func(svc, *args, **kwargs)
        return result

    def setup_http_lang(request):
        language_code = translate.get_language_from_request(request)
        if hasattr(request, 'access_info'):
            request.access_info['language'] = language_code
        else:
            request.access_info = {'language': language_code}
        translate.activate(language_code)

    def setup_rpc_lang(access_info):
        if "language" in access_info:
            translate.activate(access_info['language'])
        else:
            _logger.warning('Language context is not provided')

    return decorator
