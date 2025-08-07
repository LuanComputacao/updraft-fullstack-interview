from typing import Callable, List, TypedDict

from flask import Flask
from marshmallow import ValidationError as MarshmallowValidationError
from pydantic import ValidationError as PydanticValidationError

from components.shared.application.errors import ApplicationError
from components.shared.domain.errors import AuthorizationError
from components.shared.domain.errors import DomainError, EntityNotFound
from components.shared.infrastructure.errors import NoConfigForTenant
from components.shared.user_interface.errors import ResourceNotFound

from .http_error_handlers import (
    application_error_handler,
    generic_error_handler,
    resource_not_found_handler,
    authorization_error_handler
)


class ErrorToHandlerMap(TypedDict):
    errors: List
    handler: Callable


def register_error_handlers(
    app: Flask, error_to_handler_map_registry: List[ErrorToHandlerMap]
) -> Flask:
    for mapper in error_to_handler_map_registry:
        for error in mapper["errors"]:
            app.register_error_handler(error, mapper["handler"])
    app.register_error_handler(404, resource_not_found_handler)
    app.register_error_handler(Exception, generic_error_handler)

    return app


def get_error_to_handler_mappers() -> List[ErrorToHandlerMap]:
    error_handlers = list()

    error_handlers.append(
        ErrorToHandlerMap(
            errors=[
                ApplicationError,
                DomainError,
                EntityNotFound,
                PydanticValidationError,
                MarshmallowValidationError,
            ],
            handler=application_error_handler,
        )
    )

    error_handlers.append(
        ErrorToHandlerMap(
            errors=[ResourceNotFound, NoConfigForTenant],
            handler=resource_not_found_handler,
        )
    )

    error_handlers.append(
        ErrorToHandlerMap(
            errors=[AuthorizationError],
            handler=authorization_error_handler,
        )
    )

    return error_handlers
