from pydantic import EmailStr
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm.properties import MappedColumn


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        type_=Integer,
        autoincrement=True,
        unique=True,
        nullable=False,
        primary_key=True,
    )


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


# class Messages(BaseModel): ...
