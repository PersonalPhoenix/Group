from abc import ABC, abstractmethod
from typing import Any, Iterable, Optional

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.users.domain.events import CreatedUser
from backend.users.domain.models import User
from backend.users.orm.models import Users


class AbstractRepository(ABC):
    """Абстракция, реализующая паттерн "Репозиторий". Реализует интерфейс хранения данных и операций с ними."""

    def __init__(self):
        self.seen: set[User] = set()

    async def add(self, user: User):
        await self._add(user)
        # user.events.append(CreatedUser(user.email)) # TODO пристроить оповещение на почту
        self.seen.add(user)
    
    async def delete(self, user: User):
        if user in self.seen:
            self.seen.remove(user)

        await self._delete(user)

    async def get_all(self) -> Iterable[User]:
        users = await self._get_all()
        
        if users:
            self.seen.update(users)
    
        return users
        
    async def get_by_filter(self, filters) -> Iterable[User]:
        users = await self._get_by_filter(filters)

        if users:
            self.seen.update(users)

        return users
    
    async def get_by_email(self, email: EmailStr) -> Optional[User]:
        user = await self._get_by_email(email)

        if user:
            self.seen.add(user)

        return user

    async def get_by_id(self, id: int) -> Optional[User]:
        user = await self._get_by_id(id)

        if user:
            self.seen.add(user)

        return user

    async def get_by_tag(self, tag: str) -> Optional[User]:
        user = await self._get_by_tag(tag)

        if user:
            self.seen.add(user)

        return user

    @abstractmethod
    async def _add(self, user: User):
        raise NotImplementedError

    @abstractmethod
    async def _get_all(self) -> Iterable[User]:
        raise NotImplementedError

    @abstractmethod
    async def _get_by_filter(self, filter: dict[str, Any]) -> Iterable[User]:
        raise NotImplementedError

    @abstractmethod
    async def _get_by_id(self, id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def _get_by_email(self, email: EmailStr) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def _get_by_tag(self, tag: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def _delete(self, user: User):
        raise NotImplementedError


class UserSqlAlchemyRepository(AbstractRepository):
    """Реализует интерфейс хранения данных и операций с ними с помощью ORM SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        super().__init__()

        self.session = session

    async def _add(self, user: User):
        self.session.add(user)
        await self.session.commit()

    async def _get_all(self) -> Iterable[User]:
        result = await self.session.execute(select(Users).order_by('id'))
    
        return result.scalars().all()

    async def _get_by_filter(self, filter: dict[str, Any]) -> Iterable[User]:
        query = select(Users).filter_by(**filter)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def _get_by_id(self, id: int) -> Optional[User]:
        result = await self.session.execute(select(Users).where(Users.id == id))

        return result.scalars().first()

    async def _get_by_tag(self, tag: str) -> Optional[User]:
        result = await self.session.execute(select(Users).where(Users.tag == tag))
    
        return result.scalars().first()

    async def _get_by_email(self, email: EmailStr) -> Optional[User]:
        result = await self.session.execute(select(Users).where(Users.email == email))

        return result.scalars().first()

    async def _delete(self, user: User):
        await self.session.delete(user)
        await self.session.commit()
