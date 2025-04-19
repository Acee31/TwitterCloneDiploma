"""This module contains API-functions for user."""

from typing import Annotated, Any, Dict

from fastapi import APIRouter, Depends, Header, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_settings import db_session
from app.db.schemas.error_schemas import ErrorOut
from app.db.schemas.user_schemas import ResponseSchema, UserOut
from app.routes.crud.crud_users import follow_user_by_id, get_user, unfollow_user_by_id

users_routes = APIRouter(prefix="/api/users", tags=["Operation with users"])


@users_routes.get(
    "/me",
    response_model=UserOut,
    responses={
        400: {"model": ErrorOut},
        404: {"model": ErrorOut},
        500: {"model": ErrorOut},
    },
    summary="Get the currently authenticated user by API key",
    description="Returns a dictionary containing the user's data",
)
async def get_user_me(
    api_key: Annotated[str, Header(description="User API key")],
    session: Annotated[AsyncSession, Depends(db_session.get_session)],
) -> Dict[str, Any]:
    """Get user by API key."""
    user = await get_user(session=session, api_key_or_id=api_key)
    return {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [
                {"id": user.id, "name": user.name} for user in user.followers
            ],
            "following": [
                {"id": user.id, "name": user.name} for user in user.following
            ],
        },
    }


@users_routes.get(
    "/{user_id}",
    response_model=UserOut,
    responses={
        400: {"model": ErrorOut},
        404: {"model": ErrorOut},
        500: {"model": ErrorOut},
    },
    summary="Get the currently user for his ID in database",
    description="Returns a dictionary containing the user's data",
)
async def get_user_with_id(
    session: Annotated[AsyncSession, Depends(db_session.get_session)],
    user_id: Annotated[int, Path(..., description="User ID")],
) -> Dict[str, Any]:
    """Get user for his ID."""
    user = await get_user(session=session, api_key_or_id=user_id)

    return {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [
                {"id": user.id, "name": user.name} for user in user.followers
            ],
            "following": [
                {"id": user.id, "name": user.name} for user in user.following
            ],
        },
    }


@users_routes.post(
    "/{user_id}/follow",
    response_model=ResponseSchema,
    responses={
        400: {"model": ErrorOut},
        404: {"model": ErrorOut},
        500: {"model": ErrorOut},
    },
    summary="Follow a user by their ID",
    description="Allows the authenticated user to follow another user by specifying their user ID",
)
async def follow_user(
    api_key: Annotated[str, Header(description="User API key")],
    session: Annotated[AsyncSession, Depends(db_session.get_session)],
    user_id: Annotated[int, Path(..., description="User ID to follow")],
) -> Dict[str, bool]:
    """Follow a user by their ID."""
    follower = await get_user(session=session, api_key_or_id=api_key)

    result = await follow_user_by_id(
        session=session,
        follower_id=follower.id,
        followed_id=user_id,
    )

    return {"result": result}


@users_routes.delete(
    "/{user_id}/follow",
    response_model=ResponseSchema,
    responses={
        400: {"model": ErrorOut},
        404: {"model": ErrorOut},
        500: {"model": ErrorOut},
    },
    summary="Unfollow a user by their ID",
    description="Allows the authenticated user to unfollow another user by specifying their user ID",
)
async def unfollow_user(
    session: Annotated[AsyncSession, Depends(db_session.get_session)],
    api_key: Annotated[str, Header(description="User API key")],
    user_id: Annotated[int, Path(..., description="User ID to unfollow")],
) -> Dict[str, bool]:
    """Unfollow a user by their ID."""
    follower = await get_user(session=session, api_key_or_id=api_key)
    await get_user(session=session, api_key_or_id=user_id)

    result = await unfollow_user_by_id(
        session=session,
        follower_id=follower.id,
        followed_id=user_id,
    )

    return {"result": result}
