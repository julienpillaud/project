from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_session
from app.repository.interface import AbstractRepository
from app.users.models import UserSQLRepository
from app.users.schemas import UserDetail
from app.users.service import UserService

router = APIRouter(tags=["users"], prefix="/users")


def get_repository(
    session: Annotated[Session, Depends(get_session)],
) -> UserSQLRepository:
    return UserSQLRepository(session=session)


RepositoryDependency = Annotated[
    AbstractRepository[UserDetail], Depends(get_repository)
]


@router.get("/", response_model=list[UserDetail])
def get_users(repository: RepositoryDependency) -> Any:
    return UserService.get_users(repository=repository)
