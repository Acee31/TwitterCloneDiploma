from typing import List

from pydantic import BaseModel, Field


class ResponseSchema(BaseModel):
    result: bool = Field(default=True)


class UserBase(BaseModel):
    """
    Base user scheme
    """

    id: int = Field(default=1, description="User ID in database")
    name: str = Field(default="Name", description="User name")


class UserSchema(UserBase):
    followers: List[UserBase] = Field(..., description="List of user's subscribers")
    following: List[UserBase] = Field(..., description="List of user subscriptions")


class UserOut(BaseModel):
    """
    Scheme of output of user with boolean search result from db,
    his id, name and list of subscriptions and subscribers
    """

    result: bool = Field(default=True)
    user: UserSchema
