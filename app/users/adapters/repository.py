from abc import ABC, abstractmethod
from typing import Iterable, Optional

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.users.orm.models import Users


class AbstractRepository(ABC):
    def __init__(self):
        self.seen: set[Users] = set()

    async def add(self, user: Users):
        await self._add(user)
        self.seen.add(user)

    async def delete_by_email(self, email: EmailStr):
        user = await self.get_by_email(email)

        if user in self.seen:
            self.seen.remove(user)

        await self._delete(user)

    async def delete_by_id(self, id: int):
        user = await self.get_by_id(id)

        if user in self.seen:
            self.seen.remove(user)

        await self._delete(user)

    async def get_by_email(self, email: EmailStr) -> Optional[Users]:
        user = await self._get_by_email(email)
        if user:
            self.seen.add(user)
        return user

    async def get_by_id(self, id: int) -> Optional[Users]:
        user = await self._get_by_id(id)
        if user:
            self.seen.add(user)
        return user

    @abstractmethod
    async def _add(self, user: Users):
        raise NotImplementedError

    @abstractmethod
    async def _get_by_id(self, id: int) -> Optional[Users]:
        raise NotImplementedError

    @abstractmethod
    async def _get_by_email(self, email: EmailStr) -> Optional[Users]:
        raise NotImplementedError

    @abstractmethod
    async def _get_all_users(self) -> Iterable[Users]:
        raise NotImplementedError

    @abstractmethod
    async def _delete(self, user: Users):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        super().__init__()

        self.session = session

    async def _add(self, user: Users):
        self.session.add(user)
        await self.session.commit()

    async def _delete(self, user: Users):
        await self.session.delete(user)
        await self.session.commit()

    async def _get_by_id(self, id: int) -> Optional[Users]:
        result = await self.session.execute(select(Users).where(Users.id == id))
        return result.scalars().first()

    async def _get_by_email(self, email: EmailStr) -> Optional[Users]:
        result = await self.session.execute(select(Users).where(Users.email == email))
        return result.scalars().first()

    async def _get_all_users(self) -> Iterable[Users]:
        result = await self.session.execute(select(Users))
        return result.scalars().all()
