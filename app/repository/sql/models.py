from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.repository.sql.base import Base

user_site_table = Table(
    "user_site",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("site_id", ForeignKey("site.id"), primary_key=True),
)


class Role(Base):
    code: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]


class Site(Base):
    code: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]


class User(Base):
    upn: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]

    sites: Mapped[list[Site]] = relationship(secondary=user_site_table)
