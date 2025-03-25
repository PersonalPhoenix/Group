from dataclasses import dataclass

from pydantic import EmailStr


class Event:
    pass


@dataclass
class CreatedUser(Event):
    email: EmailStr
