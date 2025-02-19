from abc import ABC, abstractmethod

from pydantic import EmailStr

from app.users.orm.models import Users


class AbstractRepository(ABC):
    def __init__(self):
        self.seen: set[Users] = set()

    def add(self, user):
        self._add(user)
        self.seen.add(user)

    def delete_by_email(self, email):
        user = self.get_by_email(email)

        self.seen.remove(user)
        self._delete(user)

    def delete_by_id(self, id):
        user = self.get_by_id(id)

        self.seen.remove(user)
        self._delete(user)

    def get_by_email(self, email) -> Users:
        user = self._get_by_email(email)

        if user:
            self.seen.add(user)

        return user

    def get_by_id(self, id) -> Users:
        user = self._get_by_id()

        if user:
            self.seen.add(user)
        
        return user

    @abstractmethod
    def _add(self, user: Users):
        raise NotImplementedError

    @abstractmethod
    def _get_by_id(self, user: Users):
        raise NotImplementedError

    @abstractmethod
    def _get_by_email(self, user: Users):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()

        self.session = session

    def _add(self, user):
        self.session.add(user)

    def _delete(self, user: Users):
        self.session.delete(user)

    def _get_by_id(self, id: int) -> Users:
        return self.session.query(Users).get(id=id)

    def _get_by_email(self, email: EmailStr) -> Users:
        return self.session.query(Users).get(email=email)
