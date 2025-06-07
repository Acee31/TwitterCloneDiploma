"""This module contains database settings."""

import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class DBSettings:
    """
    Database settings.

    Class responsible for setting up the database engine
    and session management for asynchronous interactions with the database.
    """

    def __init__(self, url):
        self.engine = create_async_engine(url=url, echo=True)
        self.async_session = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def get_session(self):
        """Yield a new asynchronous session."""
        async with self.async_session() as session:
            yield session


load_dotenv()


db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")


db_creds = f"{db_user}:{db_password}"
db_location = f"{db_host}:{db_port}"
db_url = f"postgresql+asyncpg://{db_creds}@{db_location}/{db_name}"

db_session = DBSettings(url=db_url)
