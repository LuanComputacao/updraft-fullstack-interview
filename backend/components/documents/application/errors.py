import uuid

from components.shared.domain.errors import EntityNotFound


class DocumentNotFound(EntityNotFound):
    def __init__(self, document_id: uuid.UUID):
        self.message = f"Document with id {document_id} not found"
