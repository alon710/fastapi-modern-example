from typing import Optional, cast
from app.schemas import UserCreate, UserUpdate, UsersFilter
from sqlmodel import Session, select
from sqlalchemy.orm import InstrumentedAttribute
from datetime import datetime, timedelta
from app.models import Users


class UsersDataAccess:
    def __init__(self, database: Session):
        self.database = database

    def create_user(
        self,
        user: UserCreate,
    ) -> Users:
        db_user = Users(**user.model_dump(mode="json"))
        self.database.add(db_user)
        self.database.commit()
        self.database.refresh(db_user)
        return db_user

    def get_users(
        self,
        filters: Optional[UsersFilter] = None,
        offset: int = 0,
        limit: int = 10,
    ) -> list[Users]:
        query = select(Users)

        if filters:
            if filters.ids:
                query = query.where(
                    cast(InstrumentedAttribute, Users.id).in_(filters.ids)
                )

            if filters.emails:
                query = query.where(
                    cast(InstrumentedAttribute, Users.email).in_(filters.emails)
                )

            if filters.first_names:
                query = query.where(
                    cast(InstrumentedAttribute, Users.first_name).in_(
                        filters.first_names
                    )
                )

            if filters.ages:
                if filters.ages.min_:
                    query = query.where(
                        cast(InstrumentedAttribute, Users.age) >= filters.ages.min_
                    )

                if filters.ages.max_:
                    query = query.where(
                        cast(InstrumentedAttribute, Users.age) <= filters.ages.max_
                    )

            if filters.is_active is not None:
                query = query.where(Users.is_active == filters.is_active)

            if filters.created_at_range:
                if filters.created_at_range.min_date:
                    query = query.where(
                        cast(InstrumentedAttribute, Users.created_at)
                        >= filters.created_at_range.min_date
                    )

                if filters.created_at_range.max_date:
                    query = query.where(
                        cast(InstrumentedAttribute, Users.created_at)
                        <= filters.created_at_range.max_date
                    )

            if filters.last_connection_range:
                if filters.last_connection_range.min_date:
                    query = query.where(
                        cast(InstrumentedAttribute, Users.last_connection)
                        >= filters.last_connection_range.min_date
                    )

                if filters.last_connection_range.max_date:
                    query = query.where(
                        cast(InstrumentedAttribute, Users.last_connection)
                        <= filters.last_connection_range.max_date
                    )

        query = query.offset(offset).limit(limit)

        query_results = self.database.exec(query)
        results: list[Users] = query_results.all()

        return results

    def update_user(
        self,
        user: UserUpdate,
    ) -> Optional[Users]:
        if not (db_user := self.database.get(Users, user.id)):
            return None

        if user.email:
            db_user.email = user.email

        if user.first_name:
            db_user.first_name = user.first_name

        if user.age is not None:
            db_user.age = user.age

        if user.is_active is not None:
            db_user.is_active = user.is_active

        if user.last_connection:
            db_user.last_connection = user.last_connection

        self.database.add(db_user)
        self.database.commit()
        self.database.refresh(db_user)

        return db_user

    def deactivate_inactive_users(self, days: int = 365):
        query = select(Users).where(
            cast(InstrumentedAttribute, Users.last_connection)
            <= datetime.now() - timedelta(days=days)
        )
        result = self.database.exec(query)
        for user in result.all():
            user.is_active = False
            self.database.add(user)
        self.database.commit()
        return result
