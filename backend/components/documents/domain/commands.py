from components.shared.domain.base import Command
from pydantic import constr
import uuid


class CreateDocument(Command):
  title: constr(min_length=1, max_length=255)
  content_html: constr(min_length=1, max_length=100000)

class UpdateDocument(Command):
  id: uuid.UUID
  title: constr(min_length=1, max_length=255)
  content_html: constr(min_length=1, max_length=100000)

class SoftDeleteDocument(Command):
  id: uuid.UUID
