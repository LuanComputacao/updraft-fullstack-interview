from components.shared.application.base import UnitOfWorkInterface
from components.shared.domain.base import LoggerInterface
from components.documents.application import errors as doc_errors
from components.summary.domain import commands
from components.summary.application.providers import get_provider


class SummaryService:
    @staticmethod
    def save_summary(
        command: commands.SaveSummary,
        uow: UnitOfWorkInterface,
        logger: LoggerInterface,
    ):
        with uow:
            document = uow.repositories.documents.get(command.document_id)
            if not document:
                raise doc_errors.DocumentNotFound(command.document_id)
            document.summary_html = command.content_html
            uow.repositories.documents.save(document)
            uow.commit()
            logger.info(f"Summary saved for document {document.id}")
            return document.id

    @staticmethod
    def update_summary(
        command: commands.UpdateSummary,
        uow: UnitOfWorkInterface,
        logger: LoggerInterface,
    ):
        with uow:
            document = uow.repositories.documents.get(command.document_id)
            if not document:
                raise doc_errors.DocumentNotFound(command.document_id)
            document.summary_html = command.content_html
            uow.repositories.documents.save(document)
            uow.commit()
            logger.info(f"Summary updated for document {document.id}")

    @staticmethod
    def delete_summary(
        command: commands.DeleteSummary,
        uow: UnitOfWorkInterface,
        logger: LoggerInterface,
    ):
        with uow:
            document = uow.repositories.documents.get(command.document_id)
            if not document:
                raise doc_errors.DocumentNotFound(command.document_id)
            document.summary_html = None
            uow.repositories.documents.save(document)
            uow.commit()
            logger.info(f"Summary deleted for document {document.id}")

    @staticmethod
    def generate_stream(
        document_id,
        options: dict | None,
        uow: UnitOfWorkInterface,
        logger: LoggerInterface,
    ):
        # Not a bus command (streaming), but uses same dependencies
        with uow:
            document = uow.repositories.documents.get(document_id)
            if not document:
                raise doc_errors.DocumentNotFound(document_id)
            content = document.content_html
        provider = get_provider()
        return provider.stream_summary(content, options or {})
