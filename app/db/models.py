"""This module contains ORM models of database."""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from app.db.base_model import BaseModel

MAX_NAME_LENGTH = 50
MAX_IMAGE_PATH_LENGTH = 255


class Follow(BaseModel):
    """
    Model representing a follow relationship between two users.

    A user can follow another user.
    """

    __tablename__ = "follows"

    follower_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    followed_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))


class User(BaseModel):
    """
    Model representing a user in the database.

    A user can follow other users and be followed.
    """

    __tablename__ = "users"

    name = mapped_column(String(MAX_NAME_LENGTH), nullable=False)
    api_key = mapped_column(String(100))
    tweets = relationship("Tweet", backref="user", cascade="all, delete-orphan")
    likes = relationship("Like", backref="user", cascade="all, delete-orphan")

    following = relationship(
        "User",
        secondary="follows",
        primaryjoin="User.id == Follow.follower_id",
        secondaryjoin="User.id == Follow.followed_id",
        back_populates="followers",
        lazy="selectin",
    )

    followers = relationship(
        "User",
        secondary="follows",
        primaryjoin="User.id == Follow.followed_id",
        secondaryjoin="User.id == Follow.follower_id",
        back_populates="following",
        lazy="selectin",
    )


class Tweet(BaseModel):
    """
    Model representing a tweet created by a user.

    A tweet can have multiple likes and images.
    """

    __tablename__ = "tweets"

    tweet_text = mapped_column(String(100))
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    likes = relationship("Like", backref="tweet", cascade="all, delete-orphan")
    images = relationship("Image", backref="tweet", cascade="all, delete-orphan")


class Like(BaseModel):
    """Model representing a like on a tweet by a user."""

    __tablename__ = "likes"

    user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    tweet_id = mapped_column(Integer, ForeignKey("tweets.id", ondelete="CASCADE"))


class Image(BaseModel):
    """Model representing an image associated with a tweet."""

    __tablename__ = "images"

    tweet_id = mapped_column(ForeignKey("tweets.id", ondelete="CASCADE"))
    path = mapped_column(String(MAX_IMAGE_PATH_LENGTH))
