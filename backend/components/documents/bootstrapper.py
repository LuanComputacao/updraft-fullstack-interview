from components.shared.application.message_bus import MessageBus
import inspect
from typing import Callable, Union
from components.shared.application.base import UnitOfWorkInterface
from components.shared.domain.base import LoggerInterface
from components.shared.infrastructure.sqlalchemy_base import SqlAlchemyUnitOfWork
from components.shared.infrastructure.logger import logger as default_logger
from components.documents.application.handler_maps import EVENT_HANDLER_MAPS, COMMAND_HANDLER_MAPS
from components.documents.infrastructure import repositories

def default_uow_factory() -> SqlAlchemyUnitOfWork:
  return SqlAlchemyUnitOfWork(documents=repositories.DocumentRepository)

class Bootstrapper:
  bus: MessageBus

  def bootstrap_factory(self) -> Callable[[], MessageBus]:
    return lambda: self.bootstrap()
  
  def bootstrap(
        self,
        uow_factory: Union[
            Callable[[], UnitOfWorkInterface], UnitOfWorkInterface
        ] = default_uow_factory,
        logger: LoggerInterface = default_logger,
  ) -> MessageBus:
    uow = uow_factory() if callable(uow_factory) else uow_factory
    dependencies = dict(
      uow=uow,
      logger=logger,
    )

    injected_event_handlers = {
        event_type: [
            self._get_inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in EVENT_HANDLER_MAPS.items()
    }
    injected_command_handlers = {
        command_type: self._get_inject_dependencies(handler, dependencies)
        for command_type, handler in COMMAND_HANDLER_MAPS.items()
    }
    self.bus = MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
        logger=logger,
    )

    return self.bus
  
  def _get_inject_dependencies(self, handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)