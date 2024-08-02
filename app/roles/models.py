from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.repository.interface import Base


class Role(Base):
    code: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(String)
