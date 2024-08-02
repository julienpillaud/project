from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.repository.interface import Base


class User(Base):
    upn: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
