from typing import Annotated, Any, Dict

from fastapi import APIRouter, Depends, Header, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_settings import db_session
from .crud.crud_users import follow_user_by_id, get_user, unfollow_user_by_id
from app.db.schemas.error_schemas import ErrorOut
from app.db.schemas.user_schemas import UserOut, ResponseSchema


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
    description="Return a dictionary containing the user's data, including their followers and following lists",
)
async def get_user_me(
    api_key: Annotated[str, Header(description="User API key")],
    session: AsyncSession = Depends(db_session.get_session),
) -> Dict[str, Any]:
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
    "/{id}",
    response_model=UserOut,
    responses={
        400: {"model": ErrorOut},
        404: {"model": ErrorOut},
        500: {"model": ErrorOut},
    },
    summary="Get the currently user for his ID in database",
    description="Return a dictionary containing the user's data, including their followers and following lists",
)
async def get_user_with_id(
    id: int = Path(..., description="User ID"),
    session: AsyncSession = Depends(db_session.get_session),
) -> Dict[str, Any]:
    user = await get_user(session=session, api_key_or_id=id)

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
    "/{id}/follow",
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
    id: int = Path(..., description="User ID to follow"),
    session: AsyncSession = Depends(db_session.get_session),
) -> Dict[str, bool]:
    follower = await get_user(session=session, api_key_or_id=api_key)

    result = await follow_user_by_id(
        session=session, follower_id=follower.id, followed_id=id
    )

    return {"result": result}


@users_routes.delete(
    "/{id}/follow",
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
    api_key: Annotated[str, Header(description="User API key")],
    id: int = Path(..., description="User ID to unfollow"),
    session: AsyncSession = Depends(db_session.get_session),
) -> Dict[str, bool]:
    follower = await get_user(session=session, api_key_or_id=api_key)

    result = await unfollow_user_by_id(
        session=session, follower_id=follower.id, followed_id=id
    )

    return {"result": result}
