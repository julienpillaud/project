from sqlalchemy.orm import Mapped, mapped_column

from app.repository.interface import Base


class Site(Base):
    code: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
