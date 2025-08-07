import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Index,
    MetaData,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry

from components.documents.domain import models

metadata = MetaData()
mapper_registry = registry()


document_table = Table(
    "documents",
    metadata,
    Column(
        "id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), nullable=False
    ),
    Column("title", String(length=255), nullable=False),
    Column("content_html", String, nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("archived_at", DateTime, nullable=True),
    Index("idx_documents_id_search", "id"),
    Index("idx_documents_archived_at_search", "archived_at"),
)


def start_mappers():
    mapper_registry.map_imperatively(
        models.Document,
        document_table,
    )
