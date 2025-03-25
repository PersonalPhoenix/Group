from dataclasses import asdict, dataclass

from pydantic import EmailStr


class Command:
    def get_is_not_none_attribute(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class RegisterUser(Command):
    tag: str
    email: EmailStr
    password: str
    role_id: int = 1  #  Enum


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
