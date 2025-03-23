from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import Integer


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        type_=Integer,
        autoincrement=True,
        unique=True,
        nullable=False,
        primary_key=True,
    )

    @classmethod
    def get_columns(cls):
        return cls.__table__.columns

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.get_columns()}

    