"""This module contains the User Schema."""

from typing import List

from pydantic import BaseModel, Field


class ResponseSchema(BaseModel):
    """Standard response schema."""

    result: bool = Field(default=True)


class UserBase(BaseModel):
    """Base user schema."""

    id: int = Field(default=1, description="User ID in database")
    name: str = Field(default="Name", description="User name")


class UserSchema(UserBase):
    """Schema for representing a user with followers and following."""

    followers: List[UserBase] = Field(..., description="List of user's subscribers")
    following: List[UserBase] = Field(..., description="List of user subscriptions")


class UserOut(BaseModel):
    """
    User output schema.

    The schema has a boolean search result from the DB, its id,
    name and a list of subscriptions and subscribers
    """

    result: bool = Field(default=True)
    user: UserSchema
