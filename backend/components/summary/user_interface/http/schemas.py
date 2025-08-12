from pydantic import BaseModel


class SaveSummaryRequest(BaseModel):
    content_html: str


class UpdateSummaryRequest(SaveSummaryRequest):
    pass
