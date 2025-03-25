from dataclasses import dataclass
from typing import List

from pydantic import EmailStr

from backend.users.domain.events import Event


class User:
    """Предметная область, реализующая логику пользователя."""

    def __init__(self, tag: str, email: EmailStr, password: str, role_id: int):
        self.tag = tag
        self.email = email
        self.password = password
        self.role_id = role_id
        self.events: List[Event] = []
