from sqlalchemy.orm import Session, joinedload, aliased
from components.documents.application import dto
from components.documents.domain import models
from uuid import UUID
from typing import Optional

def get_document_collection(session: Session) -> list:
  documents = session.query(models.Document).all()
  return dto.Document(many=True).dump(documents)

def get_document_scalar(session: Session, document_id: UUID) -> Optional[dict]:
  document = session.query(models.Document).filter(models.Document.id == document_id).one_or_none()
  if document:
    return dto.Document().dump(document)
