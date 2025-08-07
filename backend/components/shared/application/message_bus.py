from typing import Callable, Dict, List, Type, Union

from components.shared.application.base import UnitOfWorkInterface
from components.shared.application.errors import UnknownMessageBusMessageType
from components.shared.domain.base import Command, Event, LoggerInterface

Message = Union[Command, Event]


class MessageBus:
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        logger: LoggerInterface,
        event_handlers: Dict[Type[Event], List[Callable]],
        command_handlers: Dict[Type[Command], Callable],
    ):
        self.uow = uow
        self.logger = logger
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self._queue = []
        self.results = []

    def handle(self, message: Message) -> None:
        self._queue.append(message)
        while self._queue:
            message = self._queue.pop(0)
            if isinstance(message, Event):
                self.handle_event(message)
            elif isinstance(message, Command):
                self.handle_command(message)
            else:
                raise UnknownMessageBusMessageType(message)

    def handle_event(self, event: Event):
        for handler in self.event_handlers[type(event)]:
            try:
                self.logger.info("Handling event %s", type(event))
                handler(event)
                self._queue.extend(self.uow.collect_new_events())
            except Exception as e:
                self.logger.exception(
                    "Exception handling event %s with %s", type(event), e
                )
                continue

    def handle_command(self, command: Command):
        self.logger.info("handling command %s", type(command))
        try:
            handler = self.command_handlers[type(command)]
            result = handler(command)
            self.results.append(result)
            self._queue.extend(self.uow.collect_new_events())
        except Exception as e:
            self.logger.exception(
                "Exception handling command %s with %s", type(command), e
            )
            raise e
