import abc
from typing import Any, Iterable, List
from uuid import UUID

from pydantic import BaseModel


class RepositoryInterface(abc.ABC):
    @abc.abstractmethod
    def save(self, model: Any):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id_: Any) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, model: Any):
        raise NotImplementedError

    @abc.abstractmethod
    def get_many_by_ids(self, ids: List) -> List[Any]:
        raise NotImplementedError


class Event:
    _name: str

    def get_event_name(self):
        return self._name

    def get_event_body(self) -> dict:
        return self.__dict__


class Command(BaseModel):
    pass


class Entity:
    id: Any
    events: List[Event] = []

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return other.id == self.id


class LoggerInterface(abc.ABC):
    @abc.abstractmethod
    def debug(self, message: str, *args, **kwargs) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def info(self, message: str, *args, **kwargs) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def warning(self, message: str, *args, **kwargs) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def error(self, message: str, *args, **kwargs) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def critical(self, message: str, *args, **kwargs) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def exception(self, message: str, *args, **kwargs) -> None:
        raise NotImplementedError
