import datetime


def iso_now():
    return datetime.datetime.now().replace(microsecond=0).isoformat()


def get_url(method, **kwargs):
    """
    Give URL-name and required path parameters, returns URL
    """
    method2endpoint = {
    }
    # Prepend the version
    endpoint = '/{version}{endpoint}'.format(
        version='v1',
        endpoint=method2endpoint[method]
    )
    url = endpoint.format(**kwargs)
    return url
