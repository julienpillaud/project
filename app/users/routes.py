from typing import Any

from fastapi import APIRouter

from app.users.schemas import UserDetail

router = APIRouter(tags=["users"], prefix="/users")


@router.get("/", response_model=list[UserDetail])
def get_users() -> Any:
    return {}
