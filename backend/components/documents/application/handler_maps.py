from components.documents.application.documents_service import DocumentsService
from components.documents.domain import commands

EVENT_HANDLER_MAPS = {}

COMMAND_HANDLER_MAPS = {
    commands.CreateDocument: DocumentsService.create_document,
    commands.UpdateDocument: DocumentsService.update_document,
    commands.SoftDeleteDocument: DocumentsService.soft_delete_document,
}
