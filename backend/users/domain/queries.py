from dataclasses import dataclass, asdict

from pydantic import EmailStr


class Query:
    def get_is_not_none_attribute(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class AuthenticateUser(Query):
    email: EmailStr
    password: str


@dataclass
class GetCurrentUser(Query):
    token: str


@dataclass
class GetAllUsers(Query):
    pass


@dataclass
class GetUserByEmail(Query):
    email: EmailStr


@dataclass
class GetUserByTag(Query):
    tag: str


@dataclass
class GetUserById(Query):
    id: int


@dataclass
class GetUsersByFilter(Query):
    id: int
    tag: str
    email: EmailStr
    role_id: int
