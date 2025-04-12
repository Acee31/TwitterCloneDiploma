from sqlalchemy import select

from app.db.base_model import Base
from app.db.models import Follow, Image, Like, Tweet, User
from app.db.db_settings import db_session

USER_DATA_TPL = [
    {"name": "User1", "api_key": "key1"},
    {"name": "User2", "api_key": "key2"},
    {"name": "User3", "api_key": "test"},
]

TWEET_DATA_TPL = [
    {"tweet_text": "First tweet", "user_id": None},
    {"tweet_text": "Second tweet", "user_id": None},
    {"tweet_text": "Third tweet", "user_id": None},
]

FOLLOW_DATA_TPL = [
    {"follower_id": None, "followed_id": None},
    {"follower_id": None, "followed_id": None},
    {"follower_id": None, "followed_id": None},
]

LIKE_DATA_TPL = [
    {"user_id": None, "tweet_id": None},
    {"user_id": None, "tweet_id": None},
    {"user_id": None, "tweet_id": None},
]

IMAGE_DATA = (
    {"tweet_id": 1, "path": "images/cosmos_1.jpg"},
    {"tweet_id": 2, "path": "images/cosmos_2.jpg"},
    {"tweet_id": 3, "path": "images/cosmos_3.jpeg"},
)


async def create_tables():
    async with db_session.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def insert_data(session):
    existing_users = (await session.execute(select(User))).scalars().all()
    if existing_users:
        return

    users = []
    for user_data in USER_DATA_TPL:
        new_user = User(**user_data)
        session.add(new_user)
        users.append(new_user)
    await session.commit()

    for i, tweet_data in enumerate(TWEET_DATA_TPL):
        tweet_data["user_id"] = users[i % len(users)].id
        new_tweet = Tweet(**tweet_data)
        session.add(new_tweet)
    await session.commit()

    for i, follow_data in enumerate(FOLLOW_DATA_TPL):
        follow_data["follower_id"] = users[i % len(users)].id
        follow_data["followed_id"] = users[(i + 1) % len(users)].id
        new_follow = Follow(**follow_data)
        session.add(new_follow)
    await session.commit()

    for i, like_data in enumerate(LIKE_DATA_TPL):
        like_data["user_id"] = users[i % len(users)].id
        like_data["tweet_id"] = (i % len(TWEET_DATA_TPL)) + 1
        new_like = Like(**like_data)
        session.add(new_like)
    await session.commit()

    for image_data in IMAGE_DATA:
        new_image = Image(**image_data)
        session.add(new_image)
    await session.commit()
