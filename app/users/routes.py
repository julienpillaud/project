import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_user_service
from app.users.schemas import UserCreate, UserDetail
from app.users.service import UserService

router = APIRouter(tags=["users"], prefix="/users")


UserServiceDependency = Annotated[UserService, Depends(get_user_service)]


@router.get("/", response_model=list[UserDetail])
def get_users(user_service: UserServiceDependency) -> Any:
    return user_service.get_users()


@router.get("/{user_id}", response_model=UserDetail)
def get_user(user_service: UserServiceDependency, user_id: uuid.UUID) -> Any:
    if user := user_service.get_user(user_id=user_id):
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post("/", response_model=UserDetail)
def create_user(user_service: UserServiceDependency, user_create: UserCreate) -> Any:
    if user_service.get_user_by_upn(upn=user_create.upn):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    return user_service.create_user(user_create=user_create)


@router.delete("/{user_id}")
def delete_user(user_service: UserServiceDependency, user_id: uuid.UUID) -> None:
    if not user_service.get_user(user_id=user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_service.delete_user(user_id=user_id)
