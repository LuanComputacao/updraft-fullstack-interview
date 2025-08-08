from flask import Flask, g, request, Response
from flask_compress import Compress
from flask_cors import CORS
from typing import List
from uuid import uuid4
from components.shared.infrastructure.os import env
from components.shared.user_interface.http_api.http_error_mappers import (
    register_error_handlers,
    ErrorToHandlerMap,
    get_error_to_handler_mappers,
)
from components.documents.infrastructure.orm import (
    start_mappers as start_documents_mappers,
)
from components.documents.user_interface.http.documents_api import documents_blueprint
from components.summary.user_interface.http.summary_api import summary_blueprint

from components.shared.infrastructure.logger import logger
from components.shared.infrastructure.tenant import (
    set_current_tenant,
    get_tenant_from_http_request,
    get_tenant_from_path,
)

IS_DEV = env.bool("IS_LOCAL_ENV", False)


def register_blueprints(flask_app: Flask):
    logger.info("registering blueprint")
    flask_app.register_blueprint(documents_blueprint)
    flask_app.register_blueprint(summary_blueprint)
    logger.info("successfully registered blueprints")


def get_error_to_handler_map_registries() -> List[ErrorToHandlerMap]:
    return get_error_to_handler_mappers()


def set_middlewares(flask_app: Flask) -> Flask:
    flask_app.before_request(ensure_request_id)
    flask_app.before_request(set_tenant)
    flask_app.after_request(propagate_request_id)

    return flask_app


def set_cors(flask_app: Flask) -> Flask:
    CORS(flask_app, max_age=3600)

    return flask_app


def set_compression(flask_app: Flask) -> Flask:
    flask_app.config.from_mapping({"COMPRESS_ALGORITHM": ["br", "gzip"]})
    compress = Compress()
    compress.init_app(app=flask_app)
    return flask_app


def start_mappers() -> None:
    start_documents_mappers()


def create_app(
    import_name: str,
    auto_load_blueprints: bool = True,
) -> Flask:
    flask_app = Flask(import_name)

    if auto_load_blueprints:
        register_blueprints(flask_app)

    start_mappers()

    flask_app = register_error_handlers(
        flask_app, get_error_to_handler_map_registries()
    )

    flask_app = set_middlewares(flask_app)
    flask_app = set_cors(flask_app)
    flask_app = set_compression(flask_app)

    return flask_app


def ensure_request_id() -> None:
    request_id = request.headers.get("X-Request-Id", False) or str(uuid4())
    g.request_id = request_id


def propagate_request_id(response: Response) -> Response:
    response.headers.set("X-Request-Id", g.request_id)
    return response


def set_tenant():
    tenant = get_tenant_from_http_request(request) or get_tenant_from_path(request)
    if not tenant:
        logger.warning(f"Missing tenant config")
        logger.info(f"headers {request.headers}")
        logger.info(f"path {request.path}")
        logger.info(f"host: {request.host}")
        return Response(status=403)
    set_current_tenant(tenant)


app = create_app(__name__)
