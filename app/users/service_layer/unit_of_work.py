from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import Config
from app.users.adapters.repository import AbstractRepository, SqlAlchemyRepository


class AbstractUnitOfWork(ABC):
    users: AbstractRepository

    def __enter__(self) -> 'AbstractUnitOfWork':
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    @abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        Config.get_postgres_url(),
        isolation_level='REPEATABLE READ',
    ),
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.users = SqlAlchemyRepository(self.session)

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
