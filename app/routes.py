from typing import Optional
from app.schemas import User, UserCreate, UserUpdate, UsersFilter
from fastapi import APIRouter, Depends, status
from app.database import get_session
from app.service import UsersService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, database=Depends(get_session)) -> User:
    return UsersService.create_user(user=user, database=database)


@router.get("")
def get_users(
    filters: UsersFilter,
    database=Depends(get_session),
    offset: int = 0,
    limit: int = 10,
) -> list[User]:
    return UsersService.get_users(
        filters=filters,
        offset=offset,
        limit=limit,
        database=database,
    )


@router.patch("/update")
def update_user(
    user_update: UserUpdate,
    database=Depends(get_session),
) -> Optional[User]:
    return UsersService.update_user(
        user=user_update,
        database=database,
    )
