from flask import Flask, g, request, Response, stream_with_context
from flask_compress import Compress
from flask_cors import CORS
from flask_restx import Api, Resource, Namespace, fields
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

documents_ns = Namespace(
    "documents", path="/api/documents", description="Documents CRUD"
)
summaries_ns = Namespace(
    "summaries", path="/api/documents", description="Document summaries & streaming"
)

# Models
create_document_model = documents_ns.model(
    "CreateDocument",
    {
        "title": fields.String(required=True),
        "content_html": fields.String(required=True),
    },
)
document_model = documents_ns.model(
    "Document",
    {
        "id": fields.String,
        "title": fields.String,
        "content_html": fields.String,
        "summary_html": fields.String,
    },
)
summary_model = summaries_ns.model(
    "Summary", {"document_id": fields.String, "summary_html": fields.String}
)
summary_save_model = summaries_ns.model(
    "SaveSummary", {"content_html": fields.String(required=True)}
)


# Documents endpoints
@documents_ns.route("/")
class DocumentsCollection(Resource):
    @documents_ns.marshal_with(
        documents_ns.model(
            "DocumentList", {"items": fields.List(fields.Nested(document_model))}
        )
    )
    def get(self):
        from components.documents.application import views
        from components.documents.user_interface.bus import bus_factory

        bus = bus_factory()
        with bus.uow as uow:
            items = views.get_document_collection(uow.session)
            return {"items": items}, 200

    @documents_ns.expect(create_document_model)
    @documents_ns.marshal_with(document_model, code=201)
    def post(self):
        from components.documents.domain import commands
        from components.documents.user_interface.bus import bus_factory

        payload = request.get_json()
        bus = bus_factory()
        bus.handle(
            commands.CreateDocument(
                title=payload["title"], content_html=payload["content_html"]
            )
        )
        doc_id = bus.results.pop()
        with bus.uow as uow:
            from components.documents.application import views

            doc = views.get_document_scalar(uow.session, doc_id)
            return doc, 201


@documents_ns.route("/<string:document_id>")
class DocumentResource(Resource):
    @documents_ns.marshal_with(document_model)
    def get(self, document_id):
        from uuid import UUID
        from components.documents.user_interface.bus import bus_factory
        from components.documents.application import views

        bus = bus_factory()
        with bus.uow as uow:
            doc = views.get_document_scalar(uow.session, UUID(document_id))
            return doc, 200

    @documents_ns.expect(create_document_model)
    @documents_ns.marshal_with(document_model)
    def put(self, document_id):
        from uuid import UUID
        from components.documents.domain import commands
        from components.documents.user_interface.bus import bus_factory
        from components.documents.application import views

        payload = request.get_json()
        bus = bus_factory()
        bus.handle(
            commands.UpdateDocument(
                id=UUID(document_id),
                title=payload["title"],
                content_html=payload["content_html"],
            )
        )
        with bus.uow as uow:
            doc = views.get_document_scalar(uow.session, UUID(document_id))
            return doc, 200

    def delete(self, document_id):
        from uuid import UUID
        from components.documents.domain import commands
        from components.documents.user_interface.bus import bus_factory

        bus = bus_factory()
        bus.handle(commands.SoftDeleteDocument(id=UUID(document_id)))
        return "", 204


# Summaries endpoints
@summaries_ns.route("/<string:document_id>/summary")
class SummaryResource(Resource):
    @summaries_ns.marshal_with(summary_model)
    def get(self, document_id):
        from uuid import UUID
        from components.summary.user_interface.bus import bus_factory

        bus = bus_factory()
        with bus.uow as uow:
            doc = uow.repositories.documents.get(UUID(document_id))
            return {
                "document_id": document_id,
                "summary_html": getattr(doc, "summary_html", None),
            }, 200

    @summaries_ns.expect(summary_save_model)
    def post(self, document_id):
        from uuid import UUID
        from components.summary.domain import commands as scmd
        from components.summary.user_interface.bus import bus_factory

        payload = request.get_json()
        bus = bus_factory()
        bus.handle(
            scmd.SaveSummary(
                document_id=UUID(document_id), content_html=payload["content_html"]
            )
        )
        return "", 201

    @summaries_ns.expect(summary_save_model)
    def put(self, document_id):
        from uuid import UUID
        from components.summary.domain import commands as scmd
        from components.summary.user_interface.bus import bus_factory

        payload = request.get_json()
        bus = bus_factory()
        bus.handle(
            scmd.UpdateSummary(
                document_id=UUID(document_id), content_html=payload["content_html"]
            )
        )
        return "", 200

    def delete(self, document_id):
        from uuid import UUID
        from components.summary.domain import commands as scmd
        from components.summary.user_interface.bus import bus_factory

        bus = bus_factory()
        bus.handle(scmd.DeleteSummary(document_id=UUID(document_id)))
        return "", 204


# Streaming endpoint via RESTX delegando implementação existente
@summaries_ns.route("/<string:document_id>/summary/stream")
class SummaryStream(Resource):
    def post(self, document_id: str):
        from uuid import UUID
        from components.summary.user_interface.http.summary_api import stream_summary

        return stream_summary(UUID(document_id))


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
    auto_load_blueprints: bool = False,
) -> Flask:
    flask_app = Flask(import_name)
    api = Api(
        flask_app,
        version="1.0",
        title="Updraft API",
        description="Document and Summary API",
        doc="/swagger/",
    )

    # Registrar namespaces RESTX (substitui blueprints para documentação)
    api.add_namespace(documents_ns)
    api.add_namespace(summaries_ns)

    # Não registrar blueprints para evitar conflito de rotas duplicadas
    # if auto_load_blueprints:
    #     register_blueprints(flask_app)

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
        logger.warning("Missing tenant config")
        logger.info(f"headers {request.headers}")
        logger.info(f"path {request.path}")
        logger.info(f"host: {request.host}")
        return Response(status=403)
    set_current_tenant(tenant)


app = create_app(__name__)
