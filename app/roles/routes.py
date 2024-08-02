from typing import Any

from fastapi import APIRouter

from app.roles.schemas import RoleDetail

router = APIRouter(tags=["roles"], prefix="/roles")


@router.get("/", response_model=list[RoleDetail])
def get_roles() -> Any:
    return {}
