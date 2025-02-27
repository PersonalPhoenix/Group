from dataclasses import dataclass

from pydantic import EmailStr


class Command:
    pass


@dataclass
class CreateUser(Command):
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


@dataclass
class GetUserByEmail(Command):
    email: EmailStr


@dataclass
class GetUserById(Command):
    id: int
