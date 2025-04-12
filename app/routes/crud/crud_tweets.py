from typing import List, Sequence, Tuple

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.db.models import Image, Like, Tweet, User


async def get_all_tweets(session: AsyncSession) -> Sequence[Tweet]:
    """
    Query the database to get all tweets

    :param session: The database session used for the query
    :return: A list of 'Tweet' objects
    """

    try:
        query = select(Tweet).options(
            joinedload(Tweet.user).load_only(User.id, User.name),
            selectinload(Tweet.likes),
            selectinload(Tweet.images),
        )
        res = await session.execute(query)
        return res.scalars().all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "result": False,
                "error_type": HTTP_500_INTERNAL_SERVER_ERROR,
                "error_message": "Database error",
            },
        )


async def add_like_to_tweet(session: AsyncSession, tweet_id: int, user_id: int) -> bool:
    """
    Adds a like to a user's tweet

    :param session: The database session used for the query
    :param tweet_id: The ID of the tweet to which the like will be added
    :param user_id: The ID of the user who is adding the like
    :return: Bool
    """

    try:
        tweet = await session.get(Tweet, tweet_id)
        if not tweet:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail={
                    "result": False,
                    "error_type": HTTP_404_NOT_FOUND,
                    "error_message": f"Tweet with id {tweet_id} not found",
                },
            )

        query = select(Like).where(Like.user_id == user_id, Like.tweet_id == tweet_id)
        result = await session.execute(query)
        if result.scalar():
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail={
                    "result": False,
                    "error_type": HTTP_400_BAD_REQUEST,
                    "error_message": "Already liked this tweet",
                },
            )

        like = Like(user_id=user_id, tweet_id=tweet_id)
        session.add(like)
        await session.commit()
        return True

    except SQLAlchemyError:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "result": False,
                "error_type": HTTP_500_INTERNAL_SERVER_ERROR,
                "error_message": "Database error",
            },
        )


async def delete_like_from_tweet(
    session: AsyncSession, tweet_id: int, user_id: int
) -> bool:
    """
    Deletes a like from a tweet

    :param session: The database session used for the query
    :param tweet_id: The ID of the tweet from which the like will be removed
    :param user_id: The ID of the user who is removing the like
    :return: Bool
    """

    try:
        tweet = await session.get(Tweet, tweet_id)
        if not tweet:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail={
                    "result": False,
                    "error_type": HTTP_404_NOT_FOUND,
                    "error_message": f"Tweet with id {tweet_id} not found",
                },
            )

        query = select(Like).where(Like.user_id == user_id, Like.tweet_id == tweet_id)
        result = await session.execute(query)
        like = result.scalar_one_or_none()
        if not like:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail={
                    "result": False,
                    "error_type": HTTP_404_NOT_FOUND,
                    "error_message": f"Tweet with id {tweet_id} doesn't have a like",
                },
            )

        await session.delete(like)
        await session.commit()
        return True

    except SQLAlchemyError:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "result": False,
                "error_type": HTTP_500_INTERNAL_SERVER_ERROR,
                "error_message": "Database error",
            },
        )


async def create_tweet(
    session: AsyncSession, user_id: int, tweet_text: str, image_ids: List[int] = None
) -> Tuple[bool, int]:
    """
    Creates a tweet and optionally associates images with it

    :param session: The database session used for the query
    :param user_id: The ID of the user who created the tweet
    :param tweet_text: The text that the user is sending
    :param image_ids: A list of image IDs to associate with the tweet (optional)
    :return: Tuple (bool, int). The tuple returns a bool and the tweet ID on a successful request
    """

    try:
        tweet = Tweet(tweet_text=tweet_text, user_id=user_id)
        session.add(tweet)
        await session.flush()

        if image_ids:
            query = select(Image).where(Image.id.in_(image_ids))
            result = await session.execute(query)
            images = result.scalars().all()
            for image in images:
                image.tweet_id = tweet.id

        await session.commit()
        return True, tweet.id

    except SQLAlchemyError:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "result": False,
                "error_type": HTTP_500_INTERNAL_SERVER_ERROR,
                "error_message": "Database error",
            },
        )


async def delete_tweet_db(session: AsyncSession, tweet_id, user_id: int) -> bool:
    """
    Deletes a tweet from the database

    :param session: The database session used for the query
    :param tweet_id: The ID of the tweet to be deleted
    :param user_id: The ID of the user who is trying to delete the tweet
    :return: Bool
    """

    try:
        query = select(Tweet).where(Tweet.id == tweet_id)
        result = await session.execute(query)
        tweet = result.scalars().first()

        if not tweet:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail={
                    "result": False,
                    "error_type": HTTP_404_NOT_FOUND,
                    "error_message": "Not found",
                },
            )

        if tweet.user_id != user_id:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail={
                    "result": False,
                    "error_type": HTTP_403_FORBIDDEN,
                    "error_message": "You cannot delete this tweet",
                },
            )

        await session.delete(tweet)
        await session.commit()
        return True
    except SQLAlchemyError:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "result": False,
                "error_type": HTTP_500_INTERNAL_SERVER_ERROR,
                "error_message": "Database error",
            },
        )
