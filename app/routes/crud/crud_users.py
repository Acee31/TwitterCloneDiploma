"""This module contains CRUD-function for user."""

from typing import Optional, Union

from fastapi import HTTPException
from sqlalchemy import Column, select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, joinedload
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.db.models import Follow, User


async def get_user(session: AsyncSession, api_key_or_id: Union[str, int]) -> User:
    """
    Fetch a user from the database using their API key or user ID.

    :param session: The database session used for the query
    :param api_key_or_id: API key or the user ID
    :return: A 'User' object
    """
    param_type = Union[InstrumentedAttribute[int], Column[int]]
    param: Optional[param_type] = None
    try:
        if isinstance(api_key_or_id, int):
            param = User.id
        else:
            param = User.api_key
        query = (
            select(User)
            .where(param == api_key_or_id)
            .options(
                joinedload(User.followers).load_only(User.id, User.name),
                joinedload(User.following).load_only(User.id, User.name),
            )
        )
        res = await session.execute(query)

        return res.unique().scalars().one()
    except NoResultFound:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail={
                "result": False,
                "error_type": HTTP_404_NOT_FOUND,
                "error_message": f"Not found user with api-key/id: {api_key_or_id}",
            },
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "result": False,
                "error_type": HTTP_500_INTERNAL_SERVER_ERROR,
                "error_message": "Database error",
            },
        )


async def follow_user_by_id(
    session: AsyncSession,
    follower_id: int,
    followed_id: int,
) -> bool:
    """
    Allow a user to follow another user by their user ID.

    :param session: The database session used for the query
    :param follower_id: The ID of the user who wants to follow another user
    :param followed_id: The ID of the user to be followed
    :return: Bool
    """
    if followed_id == follower_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail={
                "result": False,
                "error_type": HTTP_400_BAD_REQUEST,
                "error_message": "Cannot follow yourself",
            },
        )
    try:
        followed = await session.get(User, followed_id)
        if not followed:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail={
                    "result": False,
                    "error_type": HTTP_404_NOT_FOUND,
                    "error_message": f"User with id {followed_id} to follow not found",
                },
            )

        query = select(Follow).where(
            Follow.follower_id == follower_id,
            Follow.followed_id == followed_id,
        )
        result = await session.execute(query)
        if result.scalar():
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail={
                    "result": False,
                    "error_type": HTTP_400_BAD_REQUEST,
                    "error_message": "Already following this user",
                },
            )

        follow = Follow(follower_id=follower_id, followed_id=followed_id)
        session.add(follow)

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


async def unfollow_user_by_id(
    session: AsyncSession,
    follower_id: int,
    followed_id: int,
) -> bool:
    """
    Allow a user to unfollow another user by their user ID.

    :param session: The database session used for the query
    :param follower_id: The ID of the user who wants to unfollow another user
    :param followed_id: The ID of the user to be unfollowed
    :return: Bool
    """
    if followed_id == follower_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail={
                "result": False,
                "error_type": HTTP_400_BAD_REQUEST,
                "error_message": "Cannot unfollow yourself",
            },
        )

    try:
        query = select(Follow).where(
            Follow.follower_id == follower_id,
            Follow.followed_id == followed_id,
        )
        result = await session.execute(query)
        follow = result.scalar_one_or_none()

        if not follow:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail={
                    "result": False,
                    "error_type": HTTP_400_BAD_REQUEST,
                    "error_message": "Not following this user",
                },
            )
        await session.delete(follow)
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
