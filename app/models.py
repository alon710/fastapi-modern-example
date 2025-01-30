import datetime
from typing import Optional
from uuid import uuid4

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class Users(SQLModel, table=True):  # type: ignore
    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        nullable=False,
        index=True,
    )
    first_name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False)
    age: int = Field(nullable=False, gt=0, lt=120)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    last_connection: Optional[datetime.datetime] = Field(default=None)
    is_active: bool = Field(default=True)

    class Config:
        arbitrary_types_allowed = True
