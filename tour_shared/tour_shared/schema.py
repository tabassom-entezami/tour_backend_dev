from json.decoder import JSONDecodeError
import logging
from typing import Optional
from marshmallow import Schema as BaseSchema, ValidationError
from tour_shared import exceptions

logger = logging.getLogger(__name__)


class Schema(BaseSchema):

    def loads(self, *args, **kwargs):
        try:
            return super(Schema, self).loads(*args, **kwargs)
        except JSONDecodeError:
            raise exceptions.InvalidJson('Invalid JSON')

    def load(self, *args, **kwargs):
        try:
            return super(Schema, self).load(*args, **kwargs)
        except ValidationError as exp:
            raise exceptions.ValidationError(
                'Invalid input parameters',
                errors=parse_validation_error(exp.messages)
            )


def parse_validation_error(
        messages: dict,
        result: Optional[dict] = None,
        parent_keys: Optional[list] = None
):
    """Converts nested marshmallow ValidationError.messages into flat dictionary.

    Refer to tests in order to understand the functionality and see an example.
    """
    result = result if result is not None else {}
    parent_keys = parent_keys if parent_keys is not None else []
    for key, value in messages.items():
        if isinstance(value, dict):
            parse_validation_error(value, result, parent_keys + [str(key)])
        elif isinstance(value, (tuple, list)):
            result[".".join(parent_keys + [str(key)])] = value[0]

    return result
