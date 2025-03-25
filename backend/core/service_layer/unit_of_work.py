import logging
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import AsyncSession
from backend.users.adapters.repository import (
    AbstractRepository,
    UserSqlAlchemyRepository,
)
from backend.config import settings


logger = logging.getLogger(__name__)


class AbstractUnitOfWork(ABC):
    """Абстракция, реализиющая паттерн "UoW". Реализует интерфейс для управлениями сессиями."""

    async def __aenter__(self) -> 'AbstractUnitOfWork':
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    async def commit(self):
        await self._commit()

    @abstractmethod
    async def _commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    def collect_new_events(self):
        raise NotImplementedError


engine = create_async_engine(url=settings.get_database_url, echo=False, poolclass=NullPool)
DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
logger.debug(f'Engine started to database: {settings.get_database_url}')


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    """Реализует интерфейс управления сессиями для модели пользователя."""

    users: AbstractRepository

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    async def __aenter__(self) -> 'AbstractUnitOfWork':
        self.session: AsyncSession = self.session_factory()

        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)

        await self.session.close()

    async def _commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    @property
    def users(self):
        return UserSqlAlchemyRepository(session=self.session)

    def collect_new_events(self):
        for user in self.users.seen:
            while user.events:
                yield user.events.pop(0)
