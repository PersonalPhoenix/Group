from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.users.adapters.repository import (AbstractRepository,
                                           SqlAlchemyRepository)


class AbstractUnitOfWork(ABC):
    users: AbstractRepository

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


engine = create_async_engine(url=settings.get_database_url)
DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
# DEFAULT_SESSION_FACTORY.configure(bind=engine)

# engine = create_async_engine(
#     settings.get_database_url,
#     echo=True,
#     future=True,
# )
# DEFAULT_SESSION_FACTORY = sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
# )

# DEFAULT_SESSION_FACTORY = sessionmaker(
#     bind=create_async_engine(
#         settings.get_database_url,
#         isolation_level='REPEATABLE READ',
#     ),
#     class_=AsyncSession,
#     expire_on_commit=False,
# )


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    async def __aenter__(self) -> 'AbstractUnitOfWork':
        self.session: AsyncSession = self.session_factory()
        self.users = SqlAlchemyRepository(session=self.session)

        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)

        await self.session.close()

    async def _commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
