import logging

from nameko_tracer import constants
from nameko_tracer.formatters import serialise


class TracerJSONFormatter(logging.Formatter):
    """ Format trace data as JSON string
    """
    def __init__(self, **option):
        self.option = option

    def format(self, record):
        return f"[tracer] {serialise(getattr(record, constants.TRACE_KEY), **self.option)}"
