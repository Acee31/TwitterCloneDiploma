"""This module contains the Tweet, Image and Like Schemas."""

from typing import List, Optional

from pydantic import BaseModel, Field

from app.db.schemas.user_schemas import UserBase


class TweetCreate(BaseModel):
    """Schema for creating a tweet."""

    tweet_data: str = Field(default="Some text", description="Tweet text")
    tweet_media_ids: Optional[List[int]] = None


class LikeSchema(BaseModel):
    """Schema for a like on a tweet."""

    user_id: int = Field(default=1, description="User ID")
    name: str = Field(default="Name", description="User name")


class ImageSchema(BaseModel):
    """Image schema."""

    result: bool
    media_id: int


class TweetBase(BaseModel):
    """Base schema for a tweet, used in the response."""

    id: int = Field(default=1, description="Tweet ID")
    content: str = Field(default="Some text", description="Tweet text")
    attachments: List[str]
    author: UserBase
    likes: List[LikeSchema]


class TweetOut(BaseModel):
    """API response schema for retrieving a list of tweets."""

    result: bool
    tweets: List[TweetBase]


class TweetCreateSchema(BaseModel):
    """Create tweet response schema."""

    result: bool
    tweet_id: int
