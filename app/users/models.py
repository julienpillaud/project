from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.associations import user_site_table
from app.repository.interface import Base
from app.sites.models import Site


class User(Base):
    upn: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]

    sites: Mapped[list[Site]] = relationship(secondary=user_site_table)
