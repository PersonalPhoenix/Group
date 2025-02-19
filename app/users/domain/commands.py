from dataclasses import dataclass

from pydantic import EmailStr


class Command:
    pass


@dataclass
class CreateUser(Command):
    id: int
    email: EmailStr
    password: str


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
