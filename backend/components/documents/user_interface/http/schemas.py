from typing import List, Optional, Literal, Dict
from uuid import UUID

from pydantic import BaseModel

class CreateDocumentRequest(BaseModel):
  title: str
  content_html: str

class UpdateDocumentRequest(CreateDocumentRequest):
  pass