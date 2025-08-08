from components.shared.domain.base import Command
from pydantic import constr
import uuid


class SaveSummary(Command):
    document_id: uuid.UUID
    content_html: constr(min_length=1, max_length=100000)


class UpdateSummary(Command):
    document_id: uuid.UUID
    content_html: constr(min_length=1, max_length=100000)


class DeleteSummary(Command):
    document_id: uuid.UUID
