from dataclasses import asdict, dataclass

from pydantic import EmailStr


class Command:
    def get_is_not_none_attribute(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class CreateUser(Command):
    tag: str
    email: EmailStr
    password: str
    role_id: int = 1  #  Enum


@dataclass
class GetAllUsers(Command):
    pass


@dataclass
class DeleteUserById(Command):
    id: int


@dataclass
class DeleteUserByEmail(Command):
    email: EmailStr


@dataclass
class EditUser(Command):
    id: int
    fields: dict


@dataclass
class GetUserByEmail(Command):
    email: EmailStr


@dataclass
class GetUserById(Command):
    id: int


@dataclass
class GetUsersByFilter(Command):
    id: int
    tag: str
    email: EmailStr
    role_id: int
