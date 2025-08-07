from abc import ABC
from types import SimpleNamespace
from typing import Any, Callable, List, Set, Type, Union

from sqlalchemy.orm import Session

from components.shared.application.base import UnitOfWorkInterface
from components.shared.domain.base import (
    Command,
    Event,
    LoggerInterface,
    RepositoryInterface,
)
from components.shared.infrastructure.db import DEFAULT_SESSION_MAKER
from components.shared.infrastructure.logger import logger


class SQLAlchemyAbstractRepository(RepositoryInterface, ABC):
    model: Any = None
    seen: Set[Any]

    def __init__(self, session: Session):
        self.session = session
        self._scopes: List[Callable] = []
        self.seen = set()

    def get_all(self):
        return self.session.query(self.model).all()

    def save(self, model) -> None:
        self._save(model)
        self.seen.add(model)

    def get(self, id_):
        r = self._get(id_)
        if r:
            self.seen.add(r)
        return r

    def delete(self, model: Any):
        self.session.delete(model)
        self.session.flush()

    def _save(self, model):
        self.session.add(model)
        self.session.flush()

    def _get(self, id_):
        return self.session.query(self.model).get(id_)

    def get_many_by_ids(self, ids: List) -> List[Type[model]]:
        results = self.session.query(self.model).filter(self.model.id.in_(ids)).all()

        [self.seen.add(r) for r in results]

        return results


class SqlAlchemyUnitOfWork(UnitOfWorkInterface):
    session: Session

    def __init__(
        self,
        session_factory: Callable[[], Session] = DEFAULT_SESSION_MAKER,
        logger: LoggerInterface = logger,  # @todo remove
        **kwargs: Type[SQLAlchemyAbstractRepository]
    ):
        self._session_factory = session_factory
        self.logger = logger
        self._repository_config = kwargs

    def __enter__(self) -> UnitOfWorkInterface:
        self.session = self._session_factory()
        repositories = {
            name: repository(self.session)
            for name, repository in self._repository_config.items()
        }
        self.repositories = SimpleNamespace(**repositories)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def collect_new_events(self) -> List[Union[Event, Command]]:
        repositories = self.repositories.__dict__
        for repository_name in repositories:
            repository = repositories[repository_name]
            for model in repository.seen:
                while model.events:
                    yield model.events.pop(0)
