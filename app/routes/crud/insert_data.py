"""This module contains functions, which insert test data in the database."""

from sqlalchemy import select

from app.db.base_model import Base
from app.db.db_settings import db_session
from app.db.models import Follow, Image, Like, Tweet, User

USER_DATA_TPL = (
    {"name": "User1", "api_key": "key1"},
    {"name": "User2", "api_key": "key2"},
    {"name": "User3", "api_key": "test"},
)

TWEET_DATA_TPL = (
    {"tweet_text": "First tweet", "user_id": 1},
    {"tweet_text": "Second tweet", "user_id": 2},
    {"tweet_text": "Third tweet", "user_id": 3},
)

FOLLOW_DATA_TPL = (
    {"follower_id": 1, "followed_id": 2},
    {"follower_id": 2, "followed_id": 1},
    {"follower_id": 3, "followed_id": 2},
)

LIKE_DATA_TPL = (
    {"user_id": 1, "tweet_id": 1},
    {"user_id": 2, "tweet_id": 2},
    {"user_id": 3, "tweet_id": 3},
)

IMAGE_DATA = (
    {"tweet_id": 2, "path": "images/cosmos_2.jpg"},
    {"tweet_id": 3, "path": "images/cosmos_3.jpeg"},
)


async def create_tables():
    """Create all tables in the database."""
    async with db_session.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def insert_users(session):
    """Insert test users."""
    for user_data in USER_DATA_TPL:
        user = User(**user_data)
        session.add(user)
    await session.commit()


async def insert_tweets(session):
    """Insert test tweets."""
    for tweet_data in TWEET_DATA_TPL:
        session.add(Tweet(**tweet_data))
    await session.commit()


async def insert_follows(session):
    """Insert test follows."""
    for follow_data in FOLLOW_DATA_TPL:
        session.add(Follow(**follow_data))
    await session.commit()


async def insert_likes(session):
    """Insert test likes."""
    for like_data in LIKE_DATA_TPL:
        session.add(Like(**like_data))
    await session.commit()


async def insert_images(session):
    """Insert test images."""
    for image_data in IMAGE_DATA:
        session.add(Image(**image_data))
    await session.commit()


async def insert_data(session):
    """Insert test data in the database."""
    existing_users = (await session.execute(select(User))).scalars().all()
    if existing_users:
        return

    await insert_users(session)
    await insert_tweets(session)
    await insert_follows(session)
    await insert_likes(session)
    await insert_images(session)
