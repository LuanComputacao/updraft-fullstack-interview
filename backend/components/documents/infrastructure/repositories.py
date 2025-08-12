from uuid import UUID

from components.documents.domain import models
from components.shared.infrastructure.sqlalchemy_base import (
    SQLAlchemyAbstractRepository,
)


class DocumentRepository(SQLAlchemyAbstractRepository):
    model = models.Document
    seen: set[models.Document]
