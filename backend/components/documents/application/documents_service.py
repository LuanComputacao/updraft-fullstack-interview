from components.shared.application.base import UnitOfWorkInterface
from components.documents.domain import commands
from components.shared.domain.base import LoggerInterface
from components.documents.domain import models
from components.documents.application import errors


class DocumentsService:
  @staticmethod
  def create_document(
    command: commands.CreateDocument,
    uow: UnitOfWorkInterface,
    logger: LoggerInterface,
  ):
    with uow:
      logger.info(f"Creating document: {command.title}")
      document = models.Document(title=command.title, content_html=command.content_html)

      uow.repositories.documents.save(document)
      uow.commit()
      
      logger.info(f"Document created: {document.id}")
      return document.id
  
  @staticmethod
  def update_document(
    command: commands.UpdateDocument,
    uow: UnitOfWorkInterface,
    logger: LoggerInterface,
  ):
    with uow:
      logger.info(f"Updating document: {command.id}")
      document = uow.repositories.documents.get(command.id)
      if not document:
        raise errors.DocumentNotFound(command.id)
      
      document.update(command.title, command.content_html)

      uow.repositories.documents.save(document)
      uow.commit()
      logger.info(f"Document updated: {document.id}")
    

  @staticmethod
  def soft_delete_document(
    command: commands.SoftDeleteDocument,
    uow: UnitOfWorkInterface,
    logger: LoggerInterface,
  ):
    with uow:
      logger.info(f"Soft deleting document: {command.id}")
      document = uow.repositories.documents.get(command.id)
      if not document:
        raise errors.DocumentNotFound(command.id)
      
      document.soft_delete()
      
      uow.repositories.documents.save(document)
      uow.commit()
      logger.info(f"Document soft deleted: {document.id}")
