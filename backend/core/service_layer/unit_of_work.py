from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from backend.config import settings


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


engine = create_async_engine(url=settings.get_database_url, echo=False, poolclass=NullPool)
DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
