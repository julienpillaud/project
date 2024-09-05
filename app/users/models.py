import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.repository.interface import Base


class User(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    upn: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]


class UserSite(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id")
    )
    site_code: Mapped[str] = mapped_column(ForeignKey("site.code"))


class UserRole(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id")
    )
    role_code: Mapped[str] = mapped_column(ForeignKey("role.code"))
    site_code: Mapped[str] = mapped_column(ForeignKey("site.code"))
