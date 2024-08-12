import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_session
from app.repository.user_repository import SQLAlchemyUSerRepository
from app.users.schemas import UserDetail
from app.users.service import UserService

router = APIRouter(tags=["users"], prefix="/users")


def get_service(session: Annotated[Session, Depends(get_session)]) -> UserService:
    repository = SQLAlchemyUSerRepository(session=session)
    return UserService(repository=repository)


ServiceDependency = Annotated[UserService, Depends(get_service)]


@router.get("/", response_model=list[UserDetail])
def get_users(service: ServiceDependency) -> Any:
    return service.get_users()


@router.get("/{user_id}", response_model=UserDetail)
def get_user(service: ServiceDependency, user_id: uuid.UUID) -> Any:
    if user := service.get_user(user_id=user_id):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
