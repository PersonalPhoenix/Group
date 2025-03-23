from dataclasses import dataclass

from pydantic import EmailStr


@dataclass(unsafe_hash=False)
class User:
    """Предметная область, реализующая логику пользователя."""

    tag: str
    email: EmailStr
    password: str
    role_id: int
