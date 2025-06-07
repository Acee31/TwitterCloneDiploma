"""This module contains the main FastAPI application and routes configuration."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.db_settings import db_session
from app.routes import api_medias as am
from app.routes import api_tweets as at
from app.routes import api_users as au
from app.routes.crud.insert_data import create_tables, insert_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize the database and creates tables at the start.

    Cleans up resources and disposes of the database connection at the end.
    """
    await create_tables()
    async with db_session.async_session() as session:
        await insert_data(session)
    yield
    await db_session.engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(au.users_routes)
app.include_router(at.tweets_routes)
app.include_router(am.medias_routes)
