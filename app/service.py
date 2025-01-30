from typing import Optional
from app.schemas import User, UserCreate, UserUpdate, UsersFilter
from fastapi import HTTPException, status
from sqlmodel import Session

from app.data_access import UsersDataAccess


class UsersService:
    @classmethod
    def create_user(
        cls,
        database: Session,
        user: UserCreate,
    ) -> User:
        db_user = UsersDataAccess(database=database).create_user(user=user)
        return User(**db_user.model_dump())

    @classmethod
    def get_users(
        cls,
        database: Session,
        filters: Optional[UsersFilter] = None,
        offset: int = 0,
        limit: int = 10,
    ) -> list[User]:
        data_access = UsersDataAccess(database=database)

        db_users = data_access.get_users(
            filters=filters,
            offset=offset,
            limit=limit,
        )

        return [User(**db_user.model_dump()) for db_user in db_users]

    @classmethod
    def update_user(
        cls,
        database: Session,
        user: UserUpdate,
    ) -> Optional[User]:
        db_user = UsersDataAccess(database=database).update_user(user=user)

        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user.id} not found",
            )

        return User(**db_user.model_dump())

    @classmethod
    def deactivate_inactive_users(cls, database: Session):
        UsersDataAccess(database=database).deactivate_inactive_users()
