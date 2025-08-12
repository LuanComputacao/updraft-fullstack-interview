import abc
import uuid
from types import SimpleNamespace
from typing import Generator, List, Union

from sqlalchemy.orm import Session

from components.shared.domain.base import Command, Event


class UnitOfWorkInterface(abc.ABC):
    repositories: SimpleNamespace
    session: Session

    def __enter__(self) -> "UnitOfWorkInterface":
        return self

    def __exit__(self, *args):
        self.rollback()
        pass

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    def collect_new_events(self) -> List[Union[Event, Command]]:
        raise NotImplementedError


class TenantResolverInterface(abc.ABC):
    @abc.abstractmethod
    def get_current_tenant(self):
        raise NotImplementedError


class SecretManagerInterface(abc.ABC):
    @abc.abstractmethod
    def get_tenant_secrets(self) -> dict:
        raise NotImplementedError
