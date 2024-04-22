import logging
import os

import pytest

_logger = logging.getLogger(__name__)


sample_data = {
    'test_user': {
        'email': os.environ['TEST_USER'],
        'password': os.environ['TEST_PASS'],
    },
}


@pytest.fixture(scope="session")
def web_session():
    """
    Provide a HTTP client to send request
    """
    from requests import Session
    from werkzeug.urls import url_join

    class WebSession(Session):
        def request(self, method, url, *args, **kwargs):
            url = url_join(os.environ.get('TEST_ENDPOINT','http://127.0.0.1:8000/'), url)
            return Session.request(self, method, url, *args, **kwargs)

    sess = WebSession()
    with sess:
        _logger.debug("Web session got created")
        yield sess
    _logger.debug("Tearing down web session")
