from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.db_settings import db_session
from app.routes.crud.insert_data import create_tables, insert_data
from .routes import api_users as au, api_tweets as at, api_medias as am


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    async with db_session.async_session() as session:
        await insert_data(session)
    yield
    await db_session.engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(au.users_routes)
app.include_router(at.tweets_routes)
app.include_router(am.medias_routes)
