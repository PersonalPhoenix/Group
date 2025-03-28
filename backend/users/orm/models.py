from pydantic import EmailStr
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm.properties import MappedColumn

from backend.core.orm.models import BaseModel


class Users(BaseModel):
    __tablename__ = 'user.users'

    tag: Mapped[str] = MappedColumn(
        type_=String,
        unique=True,
        nullable=False,
    )

    email: Mapped[EmailStr] = mapped_column(
        type_=String,
        unique=True,
        nullable=False,
    )

    password: Mapped[str] = mapped_column(
        type_=String,
        nullable=False,
    )

    # info_id: Mapped[int] = mapped_column(
    #     type_=Integer,  # TODO сделать сслыкой на отдельную таблицу в бд
    #     nullable=False,
    # )

    role_id: Mapped[int] = mapped_column(
        type_=Integer,  # TODO Сделать ссылкой на отдельную таблицу в бд\ либо enum
        nullable=False,
        default=1,  # TODO Присобачить энам сюда
    )

    def __repr__(self):
        return f'User({self.id!r}, {self.email!r})'
