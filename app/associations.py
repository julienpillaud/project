from sqlalchemy import Column, ForeignKey, Table

from app.repository.interface import Base

user_site_table = Table(
    "user_site",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("site_id", ForeignKey("site.id"), primary_key=True),
)
