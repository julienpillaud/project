from sqlalchemy.orm import Mapped, mapped_column

from app.repository.interface import Base


class Role(Base):
    code: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
