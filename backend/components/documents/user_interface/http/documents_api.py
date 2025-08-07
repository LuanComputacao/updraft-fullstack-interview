from uuid import UUID

from flask import Blueprint, jsonify
from components.documents.user_interface.bus import bus_factory
from components.documents.domain import commands
from components.shared.user_interface.utils import parse_with_for_http
from components.documents.user_interface.http import schemas
from components.documents.application import views

documents_blueprint = Blueprint("documents", __name__, url_prefix="/api/documents")

@documents_blueprint.post("/")
@parse_with_for_http(schemas.CreateDocumentRequest)
def create_document(payload: commands.CreateDocument):
  bus = bus_factory()
  bus.handle(commands.CreateDocument(title=payload.title, content_html=payload.content_html))
  
  document_id = bus.results.pop()
  with bus.uow as uow:
    document = views.get_document_scalar(uow.session, document_id)
    return jsonify(document), 201

@documents_blueprint.put("/<uuid:document_id>")
@parse_with_for_http(schemas.UpdateDocumentRequest)
def update_document(document_id: UUID, payload: commands.UpdateDocument):
  bus = bus_factory()
  bus.handle(commands.UpdateDocument(id=document_id, title=payload.title, content_html=payload.content_html))
  
  with bus.uow as uow:
    document = views.get_document_scalar(uow.session, document_id)
    return jsonify(document), 200

@documents_blueprint.delete("/<uuid:document_id>")
def soft_delete_document(document_id: UUID):
  bus = bus_factory()
  bus.handle(commands.SoftDeleteDocument(id=document_id))
  
  return "OK", 204

@documents_blueprint.get("/<uuid:document_id>")
def get_document_scalar(document_id: UUID):
  bus = bus_factory()
  with bus.uow as uow:
    document = views.get_document_scalar(uow.session, document_id)
    return jsonify(document), 200

@documents_blueprint.get("/")
def get_document_collection():
  bus = bus_factory()
  with bus.uow as uow:
    documents = views.get_document_collection(uow.session)
    return jsonify({"items": documents}), 200