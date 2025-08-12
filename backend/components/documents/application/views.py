from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session, aliased, joinedload

from components.documents.application import dto
from components.documents.domain import models


def get_document_collection(session: Session) -> list:
    documents = session.query(models.Document).all()
    return dto.Document(many=True).dump(documents)


def get_document_scalar(session: Session, document_id: UUID) -> Optional[dict]:
    document = (
        session.query(models.Document)
        .filter(models.Document.id == document_id)
        .one_or_none()
    )
    if document:
        return dto.Document().dump(document)
