from dataclasses import dataclass, field
from datetime import datetime
from components.shared.domain.base import Entity
import uuid
from typing import Optional
from datetime import datetime, UTC
from components.documents.domain import errors

@dataclass(eq=False, unsafe_hash=False)
class Document(Entity):
    id: uuid.UUID = field(default_factory=lambda: uuid.uuid4(), init=False)
    title: str
    content_html: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    archived_at: Optional[datetime] = None


    def update(self, title: str, content_html: str) -> None:
        if self.archived_at:
            raise errors.CannotUpdateArchivedDocument(self.id)
        self.title = title
        self.content_html = content_html

    def soft_delete(self) -> None:
        if self.archived_at:
            raise errors.CannotUpdateArchivedDocument(self.id)
        self.archived_at = datetime.now(UTC)