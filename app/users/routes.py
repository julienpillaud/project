import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_session
from app.repository.user_repository import SQLAlchemyUserRepository
from app.users.schemas import UserCreate, UserDetail
from app.users.service import UserService

router = APIRouter(tags=["users"], prefix="/users")


def get_service(session: Annotated[Session, Depends(get_session)]) -> UserService:
    repository = SQLAlchemyUserRepository(session=session)
    return UserService(repository=repository)


ServiceDependency = Annotated[UserService, Depends(get_service)]


@router.get("/", response_model=list[UserDetail])
def get_users(service: ServiceDependency) -> Any:
    return service.get_users()


@router.get("/{user_id}", response_model=UserDetail)
def get_user(service: ServiceDependency, user_id: uuid.UUID) -> Any:
    if user := service.get_user(user_id=user_id):
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post("/", response_model=UserDetail)
def create_user(service: ServiceDependency, user_create: UserCreate) -> Any:
    if service.get_user_by_upn(upn=user_create.upn):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    return service.create_user(user_create=user_create)


@router.delete("/{user_id}")
def delete_user(service: ServiceDependency, user_id: uuid.UUID) -> None:
    if not service.get_user(user_id=user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    service.delete_user(user_id=user_id)
