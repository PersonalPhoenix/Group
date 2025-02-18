from sqlalchemy import (
    Integer,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class BaseModel(DeclarativeBase):

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        type_=Integer,
        autoincrement=True,
        unique=True,
        nullable=False,
    )


class Users(BaseModel):
    ...


class Messages(BaseModel):
    ...
