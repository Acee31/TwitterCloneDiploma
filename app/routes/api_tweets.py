from typing import Annotated, Any, Dict

from fastapi import APIRouter, Depends, Header, Path
from sqlalchemy.ext.asyncio import AsyncSession

from .crud.crud_tweets import (
    add_like_to_tweet,
    create_tweet,
    delete_like_from_tweet,
    delete_tweet_db,
    get_all_tweets,
)
from app.db.db_settings import db_session
from app.db.schemas.error_schemas import ErrorOut
from app.db.schemas.tweet_schemas import TweetCreate, TweetCreateSchema, TweetOut
from app.db.schemas.user_schemas import ResponseSchema
from .crud.crud_users import get_user


tweets_routes = APIRouter(prefix="/api/tweets", tags=["Operation with tweets"])


@tweets_routes.get(
    "",
    response_model=TweetOut,
    responses={
        500: {"model": ErrorOut},
    },
    summary="Get all tweets",
    description="Endpoint for getting all tweets",
)
async def list_all_tweets(
    api_key: Annotated[str, Header(description="User API key")],
    session: AsyncSession = Depends(db_session.get_session),
) -> Dict[str, Any]:
    tweets = await get_all_tweets(session)

    result = []
    for tweet in tweets:
        result.append(
            {
                "id": tweet.id,
                "content": tweet.tweet_text,
                "attachments": [image.path for image in tweet.images],
                "author": {"id": tweet.user.id, "name": tweet.user.name},
                "likes": [{"user_id": like.user_id} for like in tweet.likes],
            }
        )

    return {"result": True, "tweets": result}


@tweets_routes.post(
    "/{id}/likes",
    response_model=ResponseSchema,
    responses={
        400: {"model": ErrorOut},
        404: {"model": ErrorOut},
        500: {"model": ErrorOut},
    },
    summary="Add a like to a tweet",
    description="Endpoint for adding a like to a tweet",
)
async def like_tweet(
    api_key: Annotated[str, Header(description="User API key")],
    id: int = Path(..., description="Tweet ID"),
    session: AsyncSession = Depends(db_session.get_session),
) -> Dict[str, bool]:
    user = await get_user(session=session, api_key_or_id=api_key)

    result = await add_like_to_tweet(session=session, user_id=user.id, tweet_id=id)

    return {"result": result}


@tweets_routes.delete(
    "/{id}/likes",
    response_model=ResponseSchema,
    responses={
        404: {"model": ErrorOut},
        500: {"model": ErrorOut},
    },
    summary="Remove a like from a tweet",
    description="Endpoint for removing a like from a tweet",
)
async def delete_like(
    api_key: Annotated[str, Header(description="User API key")],
    id: int = Path(..., description="Tweet ID"),
    session: AsyncSession = Depends(db_session.get_session),
) -> Dict[str, bool]:
    user = await get_user(session=session, api_key_or_id=api_key)

    result = await delete_like_from_tweet(session=session, user_id=user.id, tweet_id=id)

    return {"result": result}


@tweets_routes.post(
    "",
    response_model=TweetCreateSchema,
    responses={
        404: {"model": ErrorOut},
        500: {"model": ErrorOut},
    },
    summary="Create a tweet",
    description="Endpoint for creating a new tweet",
)
async def create_tweet_route(
    body: TweetCreate,
    api_key: Annotated[str, Header(description="User API key")],
    session: AsyncSession = Depends(db_session.get_session),
) -> Dict[str, Any]:
    user = await get_user(session=session, api_key_or_id=api_key)

    result, tweet_id = await create_tweet(
        session=session,
        user_id=user.id,
        tweet_text=body.tweet_data,
        image_ids=body.tweet_media_ids,
    )
    return {"result": result, "tweet_id": tweet_id}


@tweets_routes.delete(
    "/{id}",
    response_model=ResponseSchema,
    responses={
        403: {"model": ErrorOut},
        404: {"model": ErrorOut},
        500: {"model": ErrorOut},
    },
    summary="Delete a tweet",
    description="Endpoint for deleting a tweet",
)
async def delete_tweet(
    api_key: Annotated[str, Header(description="User API key")],
    id: int = Path(..., description="Tweet ID"),
    session: AsyncSession = Depends(db_session.get_session),
) -> Dict[str, bool]:
    user = await get_user(session=session, api_key_or_id=api_key)

    result = await delete_tweet_db(session=session, tweet_id=id, user_id=user.id)

    return {"result": result}
