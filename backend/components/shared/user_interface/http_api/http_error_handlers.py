import logging
from typing import Tuple

from flask import Response, jsonify, request, g, has_request_context

logger = logging.getLogger()


def authorization_error_handler(e):
    message = str(e) or "You don't have the required access to perform this operation."
    return make_error_response(e, message, 403)


def authentication_error_handler(e):
    message = str(e) or "You must be an authenticated user to access this resource."
    return make_error_response(e, message, 401)


def application_error_handler(e):
    message = str(e) or "The server could not process your request"
    return make_error_response(e, message, 400)


def resource_not_found_handler(e):
    message = (
        str(e) or f"The resource you are looking for was not found: {request.path}."
    )
    return make_error_response(e, message, 404)


def generic_error_handler(e):
    return make_error_response(e, str(e), 500)


def make_error_response(
    e: BaseException, message: str, status_code: int
) -> Tuple[Response, int]:
    _log_error(e, message, status_code)
    req_id = g.request_id if has_request_context() else None
    return (
        jsonify(
            error=e.__class__.__name__,
            description=message,
            status_code=status_code,
            request_id=req_id,
            path=request.path,
        ),
        status_code,
    )


def _log_error(e: BaseException, message: str, status_code: int) -> None:
    logger.exception(
        "Error %(error_class)s caught"
        " with message %(message)s"
        " and produced the HTTP status code %(status_code)s",
        dict(
            error_class=e.__class__.__name__, message=message, status_code=status_code
        ),
    )
