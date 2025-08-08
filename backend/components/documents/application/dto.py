from marshmallow import Schema
from marshmallow import fields


class Document(Schema):
    id = fields.Str()
    title = fields.Str()
    content_html = fields.Str()
    summary_html = fields.Str(allow_none=True)
    created_at = fields.DateTime()
