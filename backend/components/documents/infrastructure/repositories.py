from components.shared.infrastructure.sqlalchemy_base import (
    SQLAlchemyAbstractRepository,
)
from uuid import UUID
from components.documents.domain import models


class DocumentRepository(SQLAlchemyAbstractRepository):
  model = models.Document
  seen: set[models.Document]
