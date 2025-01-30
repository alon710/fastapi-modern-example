import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserCreate(BaseModel):
    first_name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False)
    age: int = Field(nullable=False, gt=0, lt=120)


class User(UserCreate):
    id: str
    created_at: datetime.datetime
    last_connection: Optional[datetime.datetime]
    is_active: bool


class UserUpdate(BaseModel):
    id: str
    first_name: Optional[str]
    email: Optional[EmailStr]
    age: Optional[int]
    is_active: Optional[bool]
    last_connection: Optional[datetime.datetime]


class NumberRangeFilter(BaseModel):
    min_: Optional[int] = Field(default=None, alias="min")
    max_: Optional[int] = Field(default=None, alias="max")

    model_config = ConfigDict(populate_by_name=True)


class DatesRangeFilter(BaseModel):
    min_date: Optional[datetime.datetime] = Field(default=None, alias="min")
    max_date: datetime.datetime = Field(default=None, alias="max")

    model_config = ConfigDict(populate_by_name=True)


class UsersFilter(BaseModel):
    ids: Optional[list[str]] = Field(default=None)
    first_names: Optional[list[str]] = Field(default=None)
    emails: Optional[list[EmailStr]] = Field(default=None)
    ages: Optional[NumberRangeFilter] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)
    created_at_range: Optional[DatesRangeFilter] = Field(default=None)
    last_connection_range: Optional[DatesRangeFilter] = Field(default=None)
