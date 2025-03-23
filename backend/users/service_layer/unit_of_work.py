from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.service_layer.unit_of_work import (
    DEFAULT_SESSION_FACTORY,
    AbstractUnitOfWork,
)
from backend.users.adapters.repository import (
    UserAbstractRepository,
    UserSqlAlchemyRepository,
)


class UserSqlAlchemyUnitOfWork(AbstractUnitOfWork):
    """Реализует интерфейс управления сессиями для модели пользователя."""

    users: UserAbstractRepository

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    async def __aenter__(self) -> 'AbstractUnitOfWork':
        self.session: AsyncSession = self.session_factory()
        self.users = UserSqlAlchemyRepository(session=self.session)

        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)

        await self.session.close()

    async def _commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
