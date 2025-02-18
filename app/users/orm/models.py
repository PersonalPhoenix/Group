from datetime import (
    datetime,
)

from sqlalchemy import (
    Integer,
    DateTime,
    func,
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

    created: Mapped[datetime] = mapped_column(
        type_=DateTime(
            timezone=True,
        ),
        default=func.now(),
        nullable=False,
    )

    updated: Mapped[datetime] = mapped_column(
        type_=DateTime(
            timezone=True,
        ),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class Users(BaseModel):
    ...


class Messages(BaseModel):
    ...
