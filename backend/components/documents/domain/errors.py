import uuid

from components.shared.domain.errors import EntityNotFound


class CannotUpdateArchivedDocument(EntityNotFound):
    def __init__(self, document_id: uuid.UUID):
        self.message = (
            f"Document with id {document_id} is archived and cannot be updated"
        )
