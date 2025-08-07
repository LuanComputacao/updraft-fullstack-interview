from functools import wraps
from flask import request
import json

def parse_with_for_http(schema, **kwargs):
    """Decorator used to parse json input using the specified schema
    :param schema which schema to use for Marshalisation
    :param kwargs will be passed down to the pydantic model Schema
    :param arg_name will be inserted as a keyword argument containing the
        deserialized data.
    """

    def decorator(f):
        @wraps(f)
        def inner(*fargs, **fkwargs):
            json = request.get_json(silent=True) or {}
            entity = schema(**json)
            return f(payload=entity, *fargs, **fkwargs)

        return inner

    return decorator
